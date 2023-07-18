# Import the example classes
from mylab.simulators.intersection_simulator import IntersectionSimulator
from mylab.rewards.intersection_reward import IntersectionReward
from mylab.spaces.intersection_spaces import IntersectionSpaces


# Import the AST classes
from mylab.envs.ast_env import ASTEnv
import mylab.mcts.AdaptiveStressTestingAS as AST_AS
import mylab.mcts.AST_MCTS as AST_MCTS
import mylab.mcts.ASTSim as ASTSim


# Useful imports
from example_save_trials import *
import matplotlib.pyplot as plt
import threading
import copy
import pickle
import os
import errno
import random

np.random.seed(0)

max_path_length = 100 #max number of actions in a sequence
top_k = 50            #number of trajectories to return
num_iter = 20000      #number of iterations for each tree
num_trees = 300
2

#Object creation for initial MCTS 
reward_function = IntersectionReward(num_agents=2)
spaces = IntersectionSpaces(num_agents=2, nv_range=[-0.1,0.1], np_range=[-0.35,0.35])
sim = IntersectionSimulator(min_sep=0.75, 
                            initial_states=[[-0.75,3],[-0.75,3]])
env = ASTEnv(action_only=True,
             open_loop=False,
             fixed_init_state=True,
             simulator=sim,
             reward_function=reward_function,
             spaces=spaces
             )
ast_params = AST_AS.ASTParams(max_path_length)
ast = AST_AS.AdaptiveStressTestAS(ast_params, env)


for i in range(num_trees):
    result, trajectories, actions = AST_MCTS.stress_test_intersection(ast, top_k, num_iter, max_path_length, 5.0)
    filepath = 'forest_data/F2/'+str(i)+'.pkl'
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filepath, 'wb+') as f:  
        pickle.dump([result, trajectories, actions], f)












