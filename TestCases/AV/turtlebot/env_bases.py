import gym
import numpy as np
import pybullet
from pybullet_envs.bullet import bullet_client


class BaseEnv(gym.Env):
	"""
	Base class for Bullet physics simulation environments in a Scene.
	These environments create single-player scenes and behave like normal Gym environments, if
	you don't use multiplayer.
	"""


	def __init__(self, robot, config):

		# Pybullet related
		self.scene = None
		self.physicsClientId = -1 # at the first run, we do not own physics client
		self.ownsPhysicsClient = False
		self._p=None
		self.config=config

		# setup GUI camera
		self.debugCam_dist=config['debugCam_dist']
		self.debugCam_yaw=config['debugCam_yaw']
		self.debugCam_pitch=config['debugCam_pitch']


		# robot related

		self.isRender = config['render']
		self.robot = robot
		self.action_space = robot.action_space
		self.observation_space = robot.observation_space



		#episode related
		self.episodeCounter=0
		self.envStepCounter=0
		self.done = 0
		self.reward = 0
		self.terminated = False

		self.np_random = None
		self.seed()

		# Debug
		self.combinedSound=np.array([],dtype=np.int16)
		self.logID = None


	def create_single_player_scene(self, p):
		raise NotImplementedError

	def seed(self, seed=None):
		# use a random seed if seed is None
		self.np_random, seed = gym.utils.seeding.np_random(seed)
		self.robot.np_random = self.np_random  # use the same np_randomizer for robot as for env
		return [seed]

	def reset(self):
		if self.physicsClientId < 0:
			self.ownsPhysicsClient = True

			if self.isRender:
				self._p = bullet_client.BulletClient(connection_mode=pybullet.GUI)
			else:
				self._p = bullet_client.BulletClient()

			self.physicsClientId = self._p._client
			self._p.configureDebugVisualizer(pybullet.COV_ENABLE_GUI,0)
			self._p.resetDebugVisualizerCamera(cameraDistance=self.debugCam_dist, cameraYaw=self.debugCam_yaw,
												cameraPitch=self.debugCam_pitch, cameraTargetPosition=[0, 0, 0])
			assert self._p.isNumpyEnabled() == 1

		# if it is the first run, build scene and setup simulation physics
		if self.scene is None:
			self.scene = self.create_single_player_scene(self._p)


		# if it is not the first run
		if self.ownsPhysicsClient:
			self.scene.episode_restart()
		# reset counters
		self.done = 0
		self.reward = 0
		self.terminated = False
		self.envStepCounter = 0

		s = self.robot.reset(self._p)


		self.episodeCounter = self.episodeCounter + 1


		s_plus=self.prepareObservations(s)

		return s_plus



	def prepareObservations(self,s):
		raise NotImplementedError


	def _render(self, mode, close=False):
		# no need to implement this function
		raise NotImplementedError


	def close(self):
		if self.ownsPhysicsClient:
			if self.physicsClientId >= 0:
				self._p.disconnect()
		self.physicsClientId = -1


