import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"    #just use CPU

# from garage.tf.algos.trpo import TRPO
from garage.baselines.zero_baseline import ZeroBaseline
from mylab.envs.tfenv import TfEnv
from garage.tf.policies.deterministic_mlp_policy import DeterministicMLPPolicy
from garage.misc import logger

from mylab.rewards.ast_reward_standard import ASTRewardS
from mylab.envs.ast_env import ASTEnv
from CartPole.cartpole_simulator import CartpoleSimulator

from mylab.algos.ga import GA

import os.path as osp
import argparse
import tensorflow as tf
import joblib
import math
import numpy as np

# Logger Params
parser = argparse.ArgumentParser()
parser.add_argument('--exp_name', type=str, default='cartpole_exp')
parser.add_argument('--tabular_log_file', type=str, default='progress.csv')
parser.add_argument('--text_log_file', type=str, default='tex.txt')
parser.add_argument('--params_log_file', type=str, default='args.txt')
parser.add_argument('--snapshot_mode', type=str, default="none")
parser.add_argument('--snapshot_gap', type=int, default=10)
parser.add_argument('--log_tabular_only', type=bool, default=False)
parser.add_argument('--log_dir', type=str, default='./Data/AST/GA/Test')
parser.add_argument('--args_data', type=str, default=None)
args = parser.parse_args()

# Create the logger
log_dir = args.log_dir

tabular_log_file = osp.join(log_dir, args.tabular_log_file)
text_log_file = osp.join(log_dir, args.text_log_file)
params_log_file = osp.join(log_dir, args.params_log_file)

logger.log_parameters_lite(params_log_file, args)
# logger.add_text_output(text_log_file)
logger.add_tabular_output(tabular_log_file)
prev_snapshot_dir = logger.get_snapshot_dir()
prev_mode = logger.get_snapshot_mode()
logger.set_snapshot_dir(log_dir)
logger.set_snapshot_mode(args.snapshot_mode)
logger.set_snapshot_gap(args.snapshot_gap)
logger.set_log_tabular_only(args.log_tabular_only)
logger.push_prefix("[%s] " % args.exp_name)

seed = 0
top_k = 10
max_path_length = 100

import mylab.mcts.BoundedPriorityQueues as BPQ
top_paths = BPQ.BoundedPriorityQueue(top_k)

np.random.seed(seed)
tf.set_random_seed(seed)
with tf.Session() as sess:
	# Create env
	
	data = joblib.load("../CartPole/ControlPolicy/itr_5.pkl")
	sut = data['policy']
	reward_function = ASTRewardS()

	simulator = CartpoleSimulator(sut=sut,max_path_length=100,use_seed=False)
	env = ASTEnv(open_loop=False,
								 simulator=simulator,
								 fixed_init_state=True,
								 s_0=[0.0, 0.0, 0.0 * math.pi / 180, 0.0],
								 reward_function=reward_function,
								 )
	env = TfEnv(env)
	# Create policy
	policy = DeterministicMLPPolicy(
		name='ast_agent',
		env_spec=env.spec,
		hidden_sizes=(64, 32),
		output_nonlinearity=tf.nn.tanh,
	)

	params = policy.get_params()
	sess.run(tf.variables_initializer(params))

	# Instantiate the garage objects
	baseline = ZeroBaseline(env_spec=env.spec)
	# optimizer = ConjugateGradientOptimizer(hvp_approach=FiniteDifferenceHvp(base_eps=1e-5))

	algo = GA(
		env=env,
		policy=policy,
		baseline=baseline,
		batch_size= 100,
		pop_size = 5,
		elites = 3,
		keep_best = 1,
		step_size=0.01,
		n_itr=2,
		store_paths=False,
		# optimizer= optimizer,
		max_path_length=max_path_length,
		top_paths=top_paths,
		plot=False,
		)

	algo.train(sess=sess, init_var=False)

	