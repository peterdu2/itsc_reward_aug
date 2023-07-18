from mylab.simulators.turtlebot_simulator import turtlebot_simulator

sim = turtlebot_simulator()
sim.reset(1)
while True:
	sim.step([1,0])
	print(sim.turtlebotEnv.robot.get_position())
