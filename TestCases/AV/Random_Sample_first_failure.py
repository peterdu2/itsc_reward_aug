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


num_iter = 1000000
max_path_length = 75
pedestrian_init_state = [[0,-0.5,0,3],[0,0.5,0,-3]]
num_peds = 2

spaces = ExampleAVSpaces(num_peds=3) #Set to 3, last action used by car2
sim = multi_car_simulator(num_peds=2,use_seed=False,spaces=spaces, max_path_length=max_path_length, car_init_x=-30, v_des=10.0, min_dist_x=0.1, min_dist_y=0.1, car_init_x2=-45, v_des2=12.0, ped_initial_states=pedestrian_init_state)


goal_flag = False
for cur_iter in range(num_iter):
    
    if cur_iter%100==0 :
        print(cur_iter, " out of ", num_iter)
    
    sim.reset([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    action_list = []

    for i in range(max_path_length):
        if(sim.is_goal() == True):
            goal_flag = True
            break
        #Generate a random action:
        action = []
        for j in range(num_peds+1):
           action.append(np.random.uniform(-1,1))
           action.append(np.random.uniform(-1,1))
           action.append(np.random.uniform(0,1))
           action.append(np.random.uniform(0,1))
           action.append(np.random.uniform(0,1))
           action.append(np.random.uniform(0,1))
        
        action = np.array(action)
        action_list.append(action)
        #Simulate:
        sim.step(action)
 

    if goal_flag:
        break

print(cur_iter)
print(len(action_list))
print(sim._peds)
print(sim._car)


filename = '/home/peter/Research/AST_RevC/TestCases/AV/failure_trend_data/Random/'+str(cur_iter)+'.pkl'
if not os.path.exists(os.path.dirname(filename)):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
with open(filename, 'wb+') as f:  
    pickle.dump([action_list, cur_iter], f)
            
    


