from gym.envs.registration import register

register(
	id='Turtlebot-v0',
	entry_point='turtlebot.turtlebot_env:TurtlebotEnv',
	timestep_limit=100,
	reward_threshold=5.0,
)
