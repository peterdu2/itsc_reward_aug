from mylab.simulators.ast_simulator import ASTSimulator
from mylab.simulators.turtlebotEnv.turtlebot.turtlebot_env import TurtlebotEnv
import numpy as np

class turtlebot_simulator(ASTSimulator):

	def __init__(self):
		print("Initialzing turtlebot simulator")
		self.turtlebotEnv = TurtlebotEnv()
	def simulate(self, actions, s_0):
		return -1
	def step(self, action):
		self.turtlebotEnv.step(action)
		return -1
	def reset(self, s_0):
		self.turtlebotEnv.reset()
		return -1
	def get_reward_info(self):
		return -1
	def is_goal(self):
		return -1