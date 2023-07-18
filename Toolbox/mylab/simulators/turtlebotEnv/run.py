#Note: the settings for the environment is in turtlebot/turtlebot_env 
import gym
from turtlebot.turtlebot_env import TurtlebotEnv
import numpy as np
# env = gym.make('Turtlebot-v0')
# for i_episode in range(20):
#     observation = env.reset()
#     for t in range(100):
       
#         action = np.random.uniform(low=-1,high=1,size=2)
#         observation, reward, done, info = env.step(action)
#         if done:
#             print("Episode finished after {} timesteps".format(t+1))
#             break
# env.close()

sim = TurtlebotEnv()
sim.reset()
while(True):
	action = np.random.uniform(low=-1,high=1,size=2)
	print("ACTION: ")
	print(action)
	print(sim.robot.get_position())
	print(sim.config['control'])
	print(" ")
	print(" ")
	sim.step([-10,0])
# sim.robot.load_model()
# action = np.random.uniform(low=-1,high=1,size=2)
