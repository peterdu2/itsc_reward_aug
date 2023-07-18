"""
Classic cart-pole system implemented by Rich Sutton et al.
Copied from http://incompleteideas.net/sutton/book/code/pole.c
permalink: https://perma.cc/C9ZM-652R
"""

import math
import numpy as np
from scipy.stats import norm
import gym
from gym import logger
from gym.utils import seeding
from garage.core import Serializable
from garage.envs import Step
from garage.misc.overrides import overrides

class CartPoleEnv(gym.Env, Serializable):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : 50
    }

    def __init__(self, use_seed=False, nd=1, *args, **kwargs):
        self.use_seed = use_seed
        self.nd = nd

        self.gravity = 9.8
        self.masscart = 1.0
        self.masspole = 0.1
        self.total_mass = (self.masspole + self.masscart)
        self.length = 0.5 # actually half the pole's length
        self.polemass_length = (self.masspole * self.length)
        self.force_mag = 10.0
        self.tau = 0.02  # seconds between state updates

        self.theta_threshold_radians = 12 * 2 * math.pi / 360
        self.x_threshold = 2.4

        self.seed()
        self.viewer = None
        self.state = None

        self.wind_force_mag = 0.8*self.force_mag #0.6

        self.ast_action_seq = []
        # self.log_trajectory_pdf = 0.0

        self.steps_beyond_done = None
        Serializable.quick_init(self, locals())

    @property
    def observation_space(self):
        high = np.array([
            self.x_threshold * 2,
            np.finfo(np.float32).max,
            self.theta_threshold_radians * 2,
            np.finfo(np.float32).max])
        return gym.spaces.Box(-high, high, dtype=np.float32)

    @property
    def action_space(self):
        return gym.spaces.Discrete(2)

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        state = self.state
        x, x_dot, theta, theta_dot = state
        force = self.force_mag if action==1 else -self.force_mag
        costheta = math.cos(theta)
        sintheta = math.sin(theta)
        temp = (force + self.polemass_length * theta_dot * theta_dot * sintheta) / self.total_mass
        thetaacc = (self.gravity * sintheta - costheta* temp) / (self.length * (4.0/3.0 - self.masspole * costheta * costheta / self.total_mass))
        xacc  = temp - self.polemass_length * thetaacc * costheta / self.total_mass
        x  = x + self.tau * x_dot
        x_dot = x_dot + self.tau * xacc
        theta = theta + self.tau * theta_dot
        theta_dot = theta_dot + self.tau * thetaacc
        self.state = (x,x_dot,theta,theta_dot)
        done =  x < -self.x_threshold \
                or x > self.x_threshold \
                or theta < -self.theta_threshold_radians \
                or theta > self.theta_threshold_radians
        done = bool(done)

        if not done:
            reward = 1.0
        elif self.steps_beyond_done is None:
            # Pole just fell!
            self.steps_beyond_done = 0
            reward = 1.0
        else:
            if self.steps_beyond_done == 0:
                logger.warn("You are calling 'step()' even though this environment has already returned done = True. You should always call 'reset()' once you receive 'done = True' -- any further steps are undefined behavior.")
            self.steps_beyond_done += 1
            reward = 0.0

        return np.array(self.state), reward, done, {}

    def reset(self):
        self.state = self.np_random.uniform(low=-0.05, high=0.05, size=(4,))
        self.steps_beyond_done = None
        return np.array(self.state)

    def render(self, mode='human'):
        screen_width = 600
        screen_height = 400

        world_width = self.x_threshold*2
        scale = screen_width/world_width
        carty = 100 # TOP OF CART
        polewidth = 10.0
        polelen = scale * 1.0
        cartwidth = 50.0
        cartheight = 30.0

        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height)
            l,r,t,b = -cartwidth/2, cartwidth/2, cartheight/2, -cartheight/2
            axleoffset =cartheight/4.0
            cart = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
            self.carttrans = rendering.Transform()
            cart.add_attr(self.carttrans)
            self.viewer.add_geom(cart)
            l,r,t,b = -polewidth/2,polewidth/2,polelen-polewidth/2,-polewidth/2
            pole = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
            pole.set_color(.8,.6,.4)
            self.poletrans = rendering.Transform(translation=(0, axleoffset))
            pole.add_attr(self.poletrans)
            pole.add_attr(self.carttrans)
            self.viewer.add_geom(pole)
            self.axle = rendering.make_circle(polewidth/2)
            self.axle.add_attr(self.poletrans)
            self.axle.add_attr(self.carttrans)
            self.axle.set_color(.5,.5,.8)
            self.viewer.add_geom(self.axle)
            self.track = rendering.Line((0,carty), (screen_width,carty))
            self.track.set_color(0,0,0)
            self.viewer.add_geom(self.track)

        if self.state is None: return None

        x = self.state
        cartx = x[0]*scale+screen_width/2.0 # MIDDLE OF CART
        self.carttrans.set_translation(cartx, carty)
        self.poletrans.set_rotation(-x[2])

        return self.viewer.render(return_rgb_array = mode=='rgb_array')

    def close(self):
        if self.viewer: self.viewer.close()

    #special functions for ast
    def get_observation(self):
        return np.array(self.state)
        
    @property
    def ast_observation_space(self):
        high = np.array([
            self.x_threshold * 2,
            np.finfo(np.float32).max,
            self.theta_threshold_radians * 2,
            np.finfo(np.float32).max])
        return gym.spaces.Box(-high, high, dtype=np.float32)

    @property
    def ast_action_space(self):
        # high = np.array([1.0 for i in range(self.nd)])
        high = np.array([self.wind_force_mag for i in range(self.nd)])
        return gym.spaces.Box(-high,high,dtype=np.float32)

    def ast_get_observation(self):
        return np.array(self.state)

    def ast_reset(self, s_0):
        self.state = np.copy(s_0)
        self.steps_beyond_done = None
        self.ast_action_seq = []
        # self.log_trajectory_pdf = 0.0
        # assert self.state == s_0
        return self.ast_get_observation(), self.get_observation()

    def ast_step(self, action, ast_action):
        if self.use_seed:
            gym.spaces.np_random.seed(ast_action)
            ast_action = self.ast_action_space.sample()
        ast_action = np.mean(ast_action)
        # ast_action = np.clip(ast_action,-1.0,1.0)
        ast_action = np.clip(ast_action,-self.wind_force_mag,self.wind_force_mag)
        # print(ast_action)
        # wind_force = ast_action*self.wind_force_mag
        wind_force = ast_action

        self.ast_action = wind_force
        self.ast_action_seq.append(wind_force)

        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        state = self.state
        x, x_dot, theta, theta_dot = state
        force = self.force_mag if action==1 else -self.force_mag
        force += wind_force

        costheta = math.cos(theta)
        sintheta = math.sin(theta)
        temp = (force + self.polemass_length * theta_dot * theta_dot * sintheta) / self.total_mass
        thetaacc = (self.gravity * sintheta - costheta* temp) / (self.length * (4.0/3.0 - self.masspole * costheta * costheta / self.total_mass))
        xacc  = temp - self.polemass_length * thetaacc * costheta / self.total_mass
        x  = x + self.tau * x_dot
        x_dot = x_dot + self.tau * xacc
        theta = theta + self.tau * theta_dot
        theta_dot = theta_dot + self.tau * thetaacc
        self.state = (x,x_dot,theta,theta_dot)
        done =  x < -self.x_threshold \
                or x > self.x_threshold \
                or theta < -self.theta_threshold_radians \
                or theta > self.theta_threshold_radians
        done = bool(done)

        if not done:
            reward = 1.0
        elif self.steps_beyond_done is None:
            # Pole just fell!
            self.steps_beyond_done = 0
            reward = 1.0
        else:
            if self.steps_beyond_done == 0:
                logger.warn("You are calling 'step()' even though this environment has already returned done = True. You should always call 'reset()' once you receive 'done = True' -- any further steps are undefined behavior.")
            self.steps_beyond_done += 1
            reward = 0.0

        return self.ast_get_observation(), self.get_observation(), done

    def ast_is_goal(self):
        state = self.state
        x, x_dot, theta, theta_dot = state
        done =  x < -self.x_threshold \
                or x > self.x_threshold \
                or theta < -self.theta_threshold_radians \
                or theta > self.theta_threshold_radians
        done = bool(done)
        return done

    def ast_get_reward_info(self):
        is_goal = self.ast_is_goal()
        state = self.state
        x, x_dot, theta, theta_dot = state
        if is_goal:
            dist = 0.0
        else:
            dist = np.min([
                            np.min([np.abs(x-(-self.x_threshold)),np.abs(x-self.x_threshold)])/self.x_threshold,
                            np.min([np.abs(theta-(-self.theta_threshold_radians)),np.abs(theta-self.theta_threshold_radians)])/self.theta_threshold_radians
                            ])
        # prob = norm.pdf(self.ast_action)
        prob = norm.pdf(self.ast_action/self.wind_force_mag)
        # prob = np.abs(self.ast_action/self.wind_force_mag)
        # prob = -np.abs(self.ast_action)+1.0
        # self.log_trajectory_pdf += np.log(prob)
        # print("log_t_pdf: ",self.log_trajectory_pdf)
        return dict(
            is_goal = is_goal,
            dist = dist,
            prob = prob,
            # ast_action_seq = self.ast_action_seq,
            # log_trajectory_pdf = self.log_trajectory_pdf,
            )