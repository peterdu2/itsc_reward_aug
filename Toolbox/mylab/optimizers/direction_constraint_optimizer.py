from garage.misc import ext
from garage.misc import krylov
from garage.misc import logger
from garage.core.serializable import Serializable
# from garage.misc.ext import flatten_tensor_variables
import itertools
import numpy as np
import tensorflow as tf
from garage.tf.misc import tensor_utils
from garage.misc.ext import sliced_fun


class PerlmutterHvp(object):
    def __init__(self, num_slices=1):
        self.target = None
        self.reg_coeff = None
        self.opt_fun = None
        self._num_slices = num_slices

    def update_opt(self, f, target, inputs, reg_coeff):
        self.target = target
        self.reg_coeff = reg_coeff
        params = target.get_params(trainable=True)

        constraint_grads = tf.gradients(f, xs=params)
        for idx, (grad, param) in enumerate(zip(constraint_grads, params)):
            if grad is None:
                constraint_grads[idx] = tf.zeros_like(param)

        xs = tuple([tensor_utils.new_tensor_like(p.name.split(":")[0], p) for p in params])

        def Hx_plain():
            Hx_plain_splits = tf.gradients(
                tf.reduce_sum(
                    tf.stack([tf.reduce_sum(g * x) for g, x in zip(constraint_grads, xs)])
                ),
                params
            )
            for idx, (Hx, param) in enumerate(zip(Hx_plain_splits, params)):
                if Hx is None:
                    Hx_plain_splits[idx] = tf.zeros_like(param)
            return tensor_utils.flatten_tensor_variables(Hx_plain_splits)

        self.opt_fun = ext.LazyDict(
            f_Hx_plain=lambda: tensor_utils.compile_function(
                inputs=inputs + xs,
                outputs=Hx_plain(),
                log_name="f_Hx_plain",
            ),
        )

    def build_eval(self, inputs):
        def eval(x):
            xs = tuple(self.target.flat_to_params(x, trainable=True))
            ret = sliced_fun(self.opt_fun["f_Hx_plain"], self._num_slices)(inputs, xs) + self.reg_coeff * x
            return ret

        return eval


class FiniteDifferenceHvp(object):
    def __init__(self, base_eps=1e-8, symmetric=True, grad_clip=None, num_slices=1):
        self.base_eps = base_eps
        self.symmetric = symmetric
        self.grad_clip = grad_clip
        self._num_slices = num_slices

    def update_opt(self, f, target, inputs, reg_coeff):
        self.target = target
        self.reg_coeff = reg_coeff

        params = target.get_params(trainable=True)

        constraint_grads = tf.gradients(f, xs=params)
        for idx, (grad, param) in enumerate(zip(constraint_grads, params)):
            if grad is None:
                constraint_grads[idx] = tf.zeros_like(param)

        flat_grad = tensor_utils.flatten_tensor_variables(constraint_grads)

        def f_Hx_plain(*args):
            inputs_ = args[:len(inputs)]
            xs = args[len(inputs):]
            flat_xs = np.concatenate([np.reshape(x, (-1,)) for x in xs])
            param_val = self.target.get_param_values(trainable=True)
            eps = np.cast['float32'](self.base_eps / (np.linalg.norm(param_val) + 1e-8))
            self.target.set_param_values(param_val + eps * flat_xs, trainable=True)
            flat_grad_dvplus = self.opt_fun["f_grad"](*inputs_)
            self.target.set_param_values(param_val, trainable=True)
            if self.symmetric:
                self.target.set_param_values(param_val - eps * flat_xs, trainable=True)
                flat_grad_dvminus = self.opt_fun["f_grad"](*inputs_)
                hx = (flat_grad_dvplus - flat_grad_dvminus) / (2 * eps)
                self.target.set_param_values(param_val, trainable=True)
            else:
                flat_grad = self.opt_fun["f_grad"](*inputs_)
                hx = (flat_grad_dvplus - flat_grad) / eps
            return hx

        self.opt_fun = ext.LazyDict(
            f_grad=lambda: tensor_utils.compile_function(
                inputs=inputs,
                outputs=flat_grad,
                log_name="f_grad",
            ),
            f_Hx_plain=lambda: f_Hx_plain,
        )

    def build_eval(self, inputs):
        def eval(x):
            xs = tuple(self.target.flat_to_params(x, trainable=True))
            ret = sliced_fun(self.opt_fun["f_Hx_plain"], self._num_slices)(inputs,xs) + self.reg_coeff * x
            return ret

        return eval


class DirectionConstraintOptimizer(Serializable):
    """
    Performs constrained optimization via line search.
    """

    def __init__(
            self,
            cg_iters=10,
            reg_coeff=1e-5,
            subsample_factor=1.,
            backtrack_ratio=0.8,
            max_backtracks=15,
            debug_nan=False,
            accept_violation=False,
            hvp_approach=None,
            num_slices=1):
        """

        :param cg_iters: The number of CG iterations used to calculate A^-1 g
        :param reg_coeff: A small value so that A -> A + reg*I
        :param subsample_factor: Subsampling factor to reduce samples when using "conjugate gradient. Since the
        computation time for the descent direction dominates, this can greatly reduce the overall computation time.
        :param debug_nan: if set to True, NanGuard will be added to the compilation, and ipdb will be invoked when
        nan is detected
        :param accept_violation: whether to accept the descent step if it violates the line search condition after
        exhausting all backtracking budgets
        :return:
        """
        Serializable.quick_init(self, locals())
        self._cg_iters = cg_iters
        self._reg_coeff = reg_coeff
        self._subsample_factor = subsample_factor
        self._backtrack_ratio = backtrack_ratio
        self._max_backtracks = max_backtracks
        self._num_slices = num_slices

        self._opt_fun = None
        self._target = None
        self._max_constraint_val = None
        self._constraint_name = None
        self._debug_nan = debug_nan
        self._accept_violation = accept_violation
        if hvp_approach is None:
            hvp_approach = PerlmutterHvp(num_slices)
        self._hvp_approach = hvp_approach

    def update_opt(self, target, leq_constraint, inputs, extra_inputs=None, constraint_name="constraint", *args,
                   **kwargs):
        """
        :param target: A parameterized object to optimize over. It should implement methods of the
        :class:`garage.core.paramerized.Parameterized` class.
        :param leq_constraint: A constraint provided as a tuple (f, epsilon), of the form f(*inputs) <= epsilon.
        :param inputs: A list of symbolic variables as inputs, which could be subsampled if needed. It is assumed
        that the first dimension of these inputs should correspond to the number of data points
        :param extra_inputs: A list of symbolic variables as extra inputs which should not be subsampled
        :return: No return value.
        """

        inputs = tuple(inputs)
        if extra_inputs is None:
            extra_inputs = tuple()
        else:
            extra_inputs = tuple(extra_inputs)

        # constraint_term, constraint_value = leq_constraint
        constraint_term = leq_constraint

        params = target.get_params(trainable=True)

        self._hvp_approach.update_opt(f=constraint_term, target=target, inputs=inputs + extra_inputs,
                                      reg_coeff=self._reg_coeff)

        self._target = target
        # self._max_constraint_val = constraint_value
        self._max_constraint_val = np.inf
        self._constraint_name = constraint_name

        self._opt_fun = ext.LazyDict(
            f_constraint=lambda: tensor_utils.compile_function(
                inputs=inputs + extra_inputs,
                outputs=constraint_term,
                log_name="constraint",
            ),
        )

    def constraint_val(self, inputs, extra_inputs=None):
        inputs = tuple(inputs)
        if extra_inputs is None:
            extra_inputs = tuple()
        return sliced_fun(self._opt_fun["f_constraint"], self._num_slices)(inputs, extra_inputs)

    def get_magnitude(self, direction, inputs, max_constraint_val=None,extra_inputs=None, subsample_grouped_inputs=None):
        if max_constraint_val is not None:
            self._max_constraint_val = max_constraint_val
        prev_param = np.copy(self._target.get_param_values(trainable=True))
        inputs = tuple(inputs)
        if extra_inputs is None:
            extra_inputs = tuple()

        if self._subsample_factor < 1:
            if subsample_grouped_inputs is None:
                subsample_grouped_inputs = [inputs]
            subsample_inputs = tuple()
            for inputs_grouped in subsample_grouped_inputs:
                n_samples = len(inputs_grouped[0])
                inds = np.random.choice(
                    n_samples, int(n_samples * self._subsample_factor), replace=False)
                subsample_inputs += tuple([x[inds] for x in inputs_grouped])
        else:
            subsample_inputs = inputs

        Hx = self._hvp_approach.build_eval(subsample_inputs + extra_inputs)

        descent_direction = direction

        initial_step_size = np.sqrt(
            2.0 * self._max_constraint_val * (1. / (descent_direction.dot(Hx(descent_direction)) + 1e-8))
        )
        if np.isnan(initial_step_size):
            initial_step_size = 1.
        flat_descent_step = initial_step_size * descent_direction

        n_iter = 0
        for n_iter, ratio in enumerate(self._backtrack_ratio ** np.arange(self._max_backtracks)):
            cur_step = ratio * flat_descent_step
            cur_param = prev_param - cur_step
            self._target.set_param_values(cur_param, trainable=True)
            constraint_val = sliced_fun(self._opt_fun["f_constraint"], self._num_slices)(inputs,extra_inputs)
            if self._debug_nan and np.isnan(constraint_val):
                import ipdb;
                ipdb.set_trace()
            if constraint_val <= self._max_constraint_val:
                break
        if (np.isnan(constraint_val) or constraint_val >= self._max_constraint_val) and not self._accept_violation:
            logger.log("Line search condition violated. Rejecting the step!")
            if np.isnan(constraint_val):
                logger.log("Violated because constraint %s is NaN" % self._constraint_name)
            if constraint_val >= self._max_constraint_val:
                logger.log("Violated because constraint %s is violated" % self._constraint_name)
            self._target.set_param_values(prev_param, trainable=True)
        # logger.log("backtrack iters: %d" % n_iter)
        # logger.log("final magnitude: " + str(-ratio*initial_step_size))
        logger.log("final kl: " + str(constraint_val))
        # logger.log("optimization finished")
        return -ratio*initial_step_size, constraint_val

    def get_magnitudes(self, directions, inputs, max_constraint_val=None,extra_inputs=None, subsample_grouped_inputs=None):
        if max_constraint_val is not None:
            self._max_constraint_val = max_constraint_val
        prev_param = np.copy(self._target.get_param_values(trainable=True))
        inputs = tuple(inputs)
        if extra_inputs is None:
            extra_inputs = tuple()

        if self._subsample_factor < 1:
            if subsample_grouped_inputs is None:
                subsample_grouped_inputs = [inputs]
            subsample_inputs = tuple()
            for inputs_grouped in subsample_grouped_inputs:
                n_samples = len(inputs_grouped[0])
                inds = np.random.choice(
                    n_samples, int(n_samples * self._subsample_factor), replace=False)
                subsample_inputs += tuple([x[inds] for x in inputs_grouped])
        else:
            subsample_inputs = inputs

        Hx = self._hvp_approach.build_eval(subsample_inputs + extra_inputs)

        magnitudes = []
        constraint_vals = []
        for descent_direction in directions:
            initial_step_size = np.sqrt(
                2.0 * self._max_constraint_val * (1. / (descent_direction.dot(Hx(descent_direction)) + 1e-8))
            )
            if np.isnan(initial_step_size):
                initial_step_size = 1.
            flat_descent_step = initial_step_size * descent_direction

            n_iter = 0
            for n_iter, ratio in enumerate(self._backtrack_ratio ** np.arange(self._max_backtracks)):
                cur_step = ratio * flat_descent_step
                cur_param = prev_param - cur_step
                self._target.set_param_values(cur_param, trainable=True)
                constraint_val = sliced_fun(self._opt_fun["f_constraint"], self._num_slices)(inputs,extra_inputs)
                if self._debug_nan and np.isnan(constraint_val):
                    import ipdb;
                    ipdb.set_trace()
                if constraint_val <= self._max_constraint_val:
                    break
            if (np.isnan(constraint_val) or constraint_val >= self._max_constraint_val) and not self._accept_violation:
                logger.log("Line search condition violated. Rejecting the step!")
                if np.isnan(constraint_val):
                    logger.log("Violated because constraint %s is NaN" % self._constraint_name)
                if constraint_val >= self._max_constraint_val:
                    logger.log("Violated because constraint %s is violated" % self._constraint_name)
                self._target.set_param_values(prev_param, trainable=True)
            # logger.log("backtrack iters: %d" % n_iter)
            # logger.log("final magnitude: " + str(-ratio*initial_step_size))
            logger.log("final kl: " + str(constraint_val))
            # logger.log("optimization finished")
            magnitudes.append(-ratio*initial_step_size)
            constraint_vals.append(constraint_val)
        return magnitudes, constraint_vals
