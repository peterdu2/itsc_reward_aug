import numpy as np
import mylab.mcts.MCTSdpw as MCTSdpw
import mylab.mcts.MDP as MDP
from mylab.mcts.MCTS_solver import MCTS_multi
from mylab.mcts.MCTS_solver_intersection import MCTS_intersection

class StressTestResults:
	def __init__(self,rewards,action_seqs,q_values):
		self.rewards = rewards
		self.action_seqs = action_seqs
		self.q_values = q_values

def StressTestResultsInit(k):
	rewards = np.zeros(k)
	action_seqs = [None]*k
	q_values = [None]*k
	return StressTestResults(rewards,action_seqs,q_values)

def rollout_getAction(ast):
	def rollout_policy(s,tree):
		return ast.random_action()
	return rollout_policy

def explore_getAction(ast):
	def explore_policy(s,tree):
		return ast.explore_action(s,tree)
	return explore_policy

def action_gen(ast):
	def wrapper():
		return ast.random_action()
	return wrapper

def stress_test(ast,mcts_params,top_paths,verbose=True,return_tree=False):
	# dpw_model = MCTSdpw.DPWModel(ast.transition_model,uniform_getAction(ast.rsg),uniform_getAction(ast.rsg))
	# dpw_model = MCTSdpw.DPWModel(ast.transition_model,uniform_getAction(ast),uniform_getAction(ast))
	dpw_model = MCTSdpw.DPWModel(ast.transition_model,rollout_getAction(ast),explore_getAction(ast))
	dpw = MCTSdpw.DPW(mcts_params,dpw_model,top_paths)
	(mcts_reward,action_seq) = MDP.simulate(dpw.f.model,dpw,MCTSdpw.selectAction,verbose=verbose)
	results = StressTestResultsInit(top_paths.N)
	#results = StressTestResultsInit(dpw.top_paths.length())
	#print(dpw.top_paths.length())

	# k = 0
	# for (r,tr) in dpw.top_paths:
	# 	results.rewards[k] = r
	# 	results.action_seqs[k] = tr.get_actions()
	# 	results.q_values[k] = tr.get_q_values()
	# 	k += 1

	# if mcts_reward >= results.rewards[0]:
	# 	print("mcts_reward = ",mcts_reward," top reward = ",results.rewards[0])
	results = ast.top_paths
	if return_tree:
		return results,dpw.s
	else:
		return results

def stress_test2(ast,mcts_params,top_paths,verbose=True,return_tree=False):
	mcts_params.clear_nodes = False
	mcts_params.n *= ast.params.max_steps

	dpw_model = MCTSdpw.DPWModel(ast.transition_model,rollout_getAction(ast),explore_getAction(ast))
	dpw = MCTSdpw.DPW(mcts_params,dpw_model,top_paths)

	s = dpw.f.model.getInitialState()
	MCTSdpw.selectAction(dpw,s,verbose=verbose)
	# results = StressTestResultsInit(top_paths.N)
	# k = 0
	# for (r,tr) in dpw.top_paths:
	# 	results.rewards[k] = r
	# 	results.action_seqs[k] = tr.get_actions()
	# 	results.q_values[k] = tr.get_q_values()
	# 	k += 1
	results = ast.top_paths
	if return_tree:
		return results,dpw.s
	else:
		return results


def stress_test_multi(ast, num_paths, num_iter, tree_depth, traj_discount):
	print("Running stress test: two vehicles")
	test = MCTS_multi(traj_sim_discount=traj_discount, ast=ast, tree_depth=tree_depth,
					  num_iter=num_iter, num_paths=num_paths, model=ast.transition_model,
					  action_generator=action_gen(ast))

	starting_state = ast.transition_model.getInitialState()

	test.GeneratePaths(starting_state)
	results = StressTestResultsInit(num_paths)
	trajectory_test = [0] * num_paths
	k = 0
	for (r, tr) in test.best_paths:
		results.rewards[k] = r
		results.action_seqs[k] = tr.get_actions()
		results.q_values[k] = tr.get_q_values()

		trajectory_test[k] = tr.get_trajectory()
		k += 1

	return results, trajectory_test


def stress_test_intersection(ast, num_paths, num_iter, tree_depth, traj_discount):
	print("Running stress test: intersection")
	test = MCTS_intersection(traj_sim_discount=traj_discount, ast=ast, tree_depth=tree_depth,
					  num_iter=num_iter, num_paths=num_paths, model=ast.transition_model,
					  action_generator=action_gen(ast))

	starting_state = ast.transition_model.getInitialState()

	test.GeneratePaths(starting_state)
	results = StressTestResultsInit(num_paths)
	trajectory_test = [0] * num_paths
	action_list = [0] * num_paths
	k = 0
	for (r, tr) in test.best_paths:
		results.rewards[k] = r
		results.action_seqs[k] = tr.get_actions()
		results.q_values[k] = tr.get_q_values()

		trajectory_test[k] = tr.get_trajectory()
		action_list[k] = tr.get_actions()
		k += 1

	return results, trajectory_test, action_list
