from mylab.simulators.ast_simulator import ASTSimulator
import numpy as np
import copy

class IntersectionSimulator(ASTSimulator):

	def __init__(self,
			     num_agents=2,
				 initial_states=[[-5,25],[-5,25]], #vel=-5m/s, pos=25m
				 desired_sep=5,
				 v_max=10,
				 a_max=3,
				 dt=0.1,
				 min_sep=3,
				 **kwargs):

		print("Initialzing intersection simulator")

		self._num_agents = num_agents
		self._desired_sep = desired_sep
		self._dt = dt
		self._a_max = a_max
		self._v_max = v_max
		self._initial_states = initial_states
		self._min_sep = min_sep
		self._action = None

		# Individual agent states are [velocity, distance from intersection]
		self._agent_states = []
		for i in range(num_agents):
			self._agent_states.append(copy.deepcopy(initial_states[i]))

		self._prev_accels = np.zeros(num_agents)
		self._cur_accels = np.zeros(num_agents)

		super().__init__(**kwargs)


	def simulate(self, actions, s_0):
		return -1


	def step(self, action):
		
		# action = [nv, np, di, do...] (set of four values for each agent concatenated into single array)
		self._action = action

		# Calculate time to arrival at intersection (with noise)
		arrival_times = []
		noised_measurements = []

		for i in range(self._num_agents):
			noised_pos = self._agent_states[i][1] + action[4*i+1]
			noised_vel = self._agent_states[i][0] + action[4*i]


			#noised_pos = 0 if noised_pos < 0 else noised_pos
			#noised_vel = 0 if noised_vel < 0 else noised_vel

			arrival_times.append(abs(noised_pos/noised_vel))
			noised_measurements.append([noised_vel, noised_pos])

		first_to_arrive = arrival_times.index(min(arrival_times))
		
		# Calculate desired time to arrival of first vehicle assuming second vehicle stays at constant velocity
		for i in range(self._num_agents):
			if i != first_to_arrive:
				last_to_arrive = i;
				remaining_dist = abs(noised_measurements[i][1]-self._desired_sep)
				remaining_time = abs(remaining_dist/noised_measurements[i][0])	# Time when second vehicle will be desired_sep away from intersection

		
		# Calculate acceleration required to allow first vehicle to reach intersection in "remaining_time"
		# Using: dd = vt+ 1/2at^2 ---> a = 2(dd-vt)/t^2    where dd = delta d
		dd = 0 - noised_measurements[first_to_arrive][1]
		v = noised_measurements[first_to_arrive][0]
		a = 2*(dd-v*remaining_time)/(remaining_time**2)

		if abs(a) > self._a_max:
			a = self._a_max if a > 0 else 0

		# Record acceleration
		self._cur_accels[first_to_arrive] = a

		# Calculate accerleration required for second vehicle
		if abs(a) == self._a_max:
			# If acceleration was limited, calculate new time of arrival
			t = max(np.roots([0.5*a, v, -dd]))
			dd = self._desired_sep - noised_measurements[last_to_arrive][1]
			v = noised_measurements[last_to_arrive][0]
			a = 2*(dd-v*t)/(t**2)
			self._cur_accels[last_to_arrive] = a


		# Step agents
		for i in range(len(self._agent_states)):
			if action[4*i+2] != 1:
				self._agent_states[i][1] += self._agent_states[i][0] * self._dt			# Update position
				self._agent_states[i][0] += self._prev_accels[i] * self._dt				# Update velocity
					

		self._prev_accels = self._cur_accels
		self._cur_accels = np.zeros(self._num_agents)
		
		#print(self._agent_states)
		#print(first_to_arrive)
		return -1


	def reset(self, s_0):

		self._agent_states = []
		for i in range(self._num_agents):
			self._agent_states.append(copy.deepcopy(self._initial_states[i]))

		self._is_terminal = False

		return -1


	def get_reward_info(self):

		return {"states": self._agent_states,
                "is_goal": self.is_goal(),
                "is_terminal": self._is_terminal,
                "action": self._action}


	def is_goal(self):
		if (self._agent_states[0][1]**2 + self._agent_states[1][1]**2)**0.5 < self._min_sep:
			return True

		return False

	def isterminal(self):
		if self._agent_states[0][1] < -2 or self._agent_states[1][1] < -2:
			self._is_terminal = True
			return True

		return False