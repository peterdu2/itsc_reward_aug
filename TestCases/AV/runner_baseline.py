# Import the example classes
from mylab.simulators.multi_car_simulator import multi_car_simulator
from mylab.rewards.multi_car_reward import multi_car_reward
from mylab.spaces.example_av_spaces import ExampleAVSpaces


# Import the AST classes
from mylab.envs.ast_env import ASTEnv
import mylab.mcts.AdaptiveStressTestingAS as AST_AS
import mylab.mcts.AST_MCTS as AST_MCTS
import mylab.mcts.ASTSim as ASTSim
import mylab.mcts.testcase_gen_helpers as Helpers


# Useful imports
from example_save_trials import *
import matplotlib.pyplot as plt
import threading
import copy
import pickle
import os
import errno
import random

np.random.seed(1)

max_path_length = 75 #max number of actions in a sequence
top_k = 50            #number of trajectories to return

pedestrian_init_state = [[0,-0.5,0,3],[0,0.5,0,-3]]


#Object creation for initial MCTS 
reward_function = multi_car_reward(num_peds=2)
spaces = ExampleAVSpaces(num_peds=3) #Set to 3, last action used by car2
sim = multi_car_simulator(num_peds=2,use_seed=False,spaces=spaces, max_path_length=max_path_length, car_init_x=-30, v_des=10.0, min_dist_x=0.1, min_dist_y=0.1, car_init_x2=-45, v_des2=12.0, ped_initial_states=pedestrian_init_state)
env = ASTEnv(action_only=True,
             open_loop=False,
             fixed_init_state=True,
             simulator=sim,
             reward_function=reward_function,
             spaces=spaces
             )
ast_params = AST_AS.ASTParams(max_path_length)
ast = AST_AS.AdaptiveStressTestAS(ast_params, env)


#Initial MCTS run
result, initial_trajectories = AST_MCTS.stress_test_multi(ast, top_k, 100000, max_path_length, 0.0)


'''
filename = 'baseline_data/baseline_ast_w_6400.pkl'
if not os.path.exists(os.path.dirname(filename)):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
with open(filename, 'wb+') as f:  
    pickle.dump([initial_trajectories, result], f)
'''



