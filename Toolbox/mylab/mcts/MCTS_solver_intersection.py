
import numpy as np
import mylab.mcts.mctstracker as MT
import mylab.mcts.BoundedPriorityQueues as PQueue
import copy
import os
import errno
import pickle



class StateActionStateNode:
	def __init__(self):
		self.n = 0
		self.r = 0.0


class StateActionNode:
	def __init__(self):
		self.s = {}
		self.n = 0
		self.q = 0.0


class StateNode:
	def __init__(self):
		self.a = {}
		self.n = 0


class MCTS_intersection:
	def __init__(self, ast, model, action_generator, num_iter, num_paths, tree_depth=50, seed=1, DPW_c=0.5,
				 DPW_alpha=0.85, UCT_c=100, traj_sim_discount=0):

		# Parameters
		self.num_iter = num_iter
		self.DPW_c = DPW_c
		self.DPW_alpha = DPW_alpha
		self.UCT_c = UCT_c
		self.num_iter = num_iter
		self.random_state = np.random.RandomState(seed)
		self.tree_depth = tree_depth
		self.ast = ast
		self.simulator = ast.env.simulator
		self.traj_sim_discount = traj_sim_discount

		# AST model
		self.model = model  # AST Transition Model
		self.action_generator = action_generator  # AST action generator

		# Tree elements
		self.states = {}  # Dictionary of states
		self.tracker = MT.MCTSTrackerInit()  # Tree tracker (rewards, states, etc)
		self.best_paths = PQueue.BoundedPriorityQueueInit(num_paths)  # Queue of best paths

		# Initialze reward function object
		self.ast.env.reward_function.MCTS_obj = self

	def GeneratePaths(self, starting_state):

		print("Generating Paths using MCTS")
		for i in range(self.num_iter):
			if (i % 100 == 0):
				print(i, " out of ", self.num_iter)

			# Go to starting state
			self.model.goToState(starting_state)
			self.tracker.empty()
			self.tracker.append_actions([])
			self.tracker.append_q_values([])
			self.tracker.append_trajectories([])

			# Push initial state
			self.tracker.push_trajectory([copy.deepcopy(self.simulator._agent_states[0]), copy.deepcopy(self.simulator._agent_states[1])])

			# Build search Tree
			max_reward = self.ExpandTree(starting_state, self.tree_depth)

			#print(max_reward)
			# Check if goal has been reached, if so, set flag in tracker
			self.tracker.goal_reached = False
			if (self.simulator.is_goal()):
				self.tracker.goal_reached = True

			# Add best path to queue
			self.tracker.combine_q_values()
			self.best_paths.enqueue(self.tracker, max_reward, make_copy=True)


			#################################################################################
			#################################################################################
			# Record intermediate results at every 10 itr intervals (For plotting purposes)
			'''
			if (i % 10 == 0):
				filename = '/home/peter/Research/AST_RevC/TestCases/AV/failure_trend_data/'+str(i/10)+'.pkl'
				if not os.path.exists(os.path.dirname(filename)):
				    try:
				        os.makedirs(os.path.dirname(filename))
				    except OSError as exc: # Guard against race condition
				        if exc.errno != errno.EEXIST:
				            raise
				trajs = []
				is_goals = []
				rewards = []
				k = 0
				for (r, tr) in self.best_paths:
					rewards.append(r)
					trajs.append(tr.get_trajectory())
					is_goals.append(tr.goal_reached)
					k += 1
				with open(filename, 'wb+') as f:  
				    pickle.dump([trajs, is_goals, rewards], f)
			'''
			'''
			# Check if goal, if so, record number of iterations and end
			if self.tracker.goal_reached == True:
				filename = '/home/peter/Research/AST_RevC/TestCases/AV/failure_trend_data/AST/'+str(i)+'.pkl'
				if not os.path.exists(os.path.dirname(filename)):
				    try:
				        os.makedirs(os.path.dirname(filename))
				    except OSError as exc: # Guard against race condition
				        if exc.errno != errno.EEXIST:
				            raise
				trajs = []
				is_goals = []
				rewards = []
				k = 0
				for (r, tr) in self.best_paths:
					rewards.append(r)
					trajs.append(tr.get_trajectory())
					is_goals.append(tr.goal_reached)
					k += 1
				with open(filename, 'wb+') as f:  
				    pickle.dump([trajs, is_goals, rewards, i], f)

				print(i)

				break
			'''
			#################################################################################
			#################################################################################

	def ExpandTree(self, state, depth):

		if depth == 0 or self.model.isEndState(state):
			return 0.0
		if not (state in self.states):
			# Add state to tree
			self.states[state] = StateNode()
			# Simulate
			return self.Simulate(state, depth)

		# Else mark state as visited and use TreePolicy
		self.states[state].n += 1

		selected_state, action = self.TreePolicy(state)

		self.model.goToState(selected_state)
		r = self.states[state].a[action].s[selected_state].r
		self.states[state].a[action].s[selected_state].n += 1

		# Push state into trajectory
		self.tracker.push_trajectory([copy.deepcopy(self.simulator._agent_states[0]), copy.deepcopy(self.simulator._agent_states[1])])

		q = r + self.ExpandTree(selected_state, depth - 1)
		cA = self.states[state].a[action]
		cA.n += 1
		cA.q += (q - cA.q) / float(cA.n)

		return q

	def TreePolicy(self, state):

		# First progressive widening
		# If there are "k" actions available, choose the one with best reward
		# Else add and try a new action
		# Check condition for exploration
		selected_action = None
		if len(self.states[state].a) < self.DPW_c * self.states[state].n ** self.DPW_alpha:
			new_action = self.action_generator()
			if not (new_action in self.states[state].a):
				self.states[state].a[new_action] = StateActionNode()
			selected_action = new_action
		# Else continue down tree using UCT
		else:
			cur_max_UCT = float('-inf')
			cur_best_action = None
			for action in self.states[state].a:
				ANode = self.states[state].a[action]
				UCT = ANode.q + self.UCT_c * np.sqrt(np.log(self.states[state].n) / float(ANode.n))
				if UCT > cur_max_UCT:
					cur_max_UCT = UCT
					cur_best_action = action
			selected_action = cur_best_action

		# Push action and qval into tracker
		self.tracker.push_action(selected_action)
		self.tracker.push_q_value(self.states[state].a[selected_action].q)
		# Push current state into trajectory
		#self.tracker.push_trajectory([copy.deepcopy(self.simulator._agent_states[0]), copy.deepcopy(self.simulator._agent_states[1])])

		# Second progressive widening
		if len(self.states[state].a[
				   selected_action].s) < 1:  # self.DPW_c * self.states[state].a[selected_action].n**self.DPW_alpha:
			new_state, reward = self.model.getNextState(state, selected_action)
			if not (new_state in self.states[state].a[selected_action].s):
				self.states[state].a[selected_action].s[new_state] = StateActionStateNode()
				self.states[state].a[selected_action].s[new_state].r = reward
				self.states[state].a[selected_action].s[new_state].n = 1
			else:
				self.states[state].a[selected_action].s[new_state].n += 1
			return new_state, selected_action
		else:
			# Select next state from available ones based off of probability proportional to N
			cA = self.states[state].a[selected_action]
			SP = list(cA.s.keys())
			sp = np.random.choice(SP, p=[cA.s[sn].n for sn in SP] / np.sum([cA.s[sn].n for sn in SP]))
			return sp, selected_action

	def Simulate(self, state, depth):

		total_reward = 0.0

		while depth > 0 and self.model.isEndState(state) != True and self.simulator.is_goal() == False:
			rand_action = self.action_generator()
			self.tracker.push_action(rand_action)
			state, reward = self.model.getNextState(state, rand_action)
			self.tracker.push_q_value2(reward)
			total_reward += reward
			depth -= 1

			# Push state into trajectory
			self.tracker.push_trajectory([copy.deepcopy(self.simulator._agent_states[0]), copy.deepcopy(self.simulator._agent_states[1])])

		# Push final state into trajectory
		self.tracker.push_trajectory([copy.deepcopy(self.simulator._agent_states[0]), copy.deepcopy(self.simulator._agent_states[1])])

		return total_reward








