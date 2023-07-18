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
from queue import PriorityQueue
import mylab.mcts.BoundedPriorityQueues as PQueue
import mylab.mcts.mctstracker as MT



def mahalanobis_d(action, num_peds):
    # Mean action is 0
    mean = np.zeros((6 * num_peds, 1))
    # Assemble the diagonal covariance matrix
    cov = np.zeros((num_peds, 6))
    cov[:, 0:6] = np.array([0.1, 0.01,
                            0.1, 0.1,
                            0.1, 0.1])
    big_cov = np.diagflat(cov)

    # subtract the mean from our actions
    dif = np.copy(action)
    dif[::2] -= mean[0, 0]
    dif[1::2] -= mean[1, 0]

    # calculate the Mahalanobis distance
    dist = np.dot(np.dot(dif.T, np.linalg.inv(big_cov)), dif)

    return np.sqrt(dist)


class PQ(PriorityQueue):
    def __init__(self):
        PriorityQueue.__init__(self)
        self.counter = 0

    def put(self, item, priority):
        PriorityQueue.put(self, (priority, self.counter, item))
        self.counter = 1

    def get(self, *args, **kwargs):
        _, _, item = PriorityQueue.get(self, *args, **kwargs)
        return item


num_iter = 85000
search_depth = 100
num_paths = 20
num_peds = 2
top_paths = PQ()
pedestrian_init_state = [[0,-0.5,0,3],[0,0.5,0,-3]]


spaces = ExampleAVSpaces(num_peds=3) #Set to 3, last action used by car2
sim = multi_car_simulator(num_peds=2,use_seed=False,spaces=spaces, max_path_length=100, car_init_x=-20, v_des=11.1, min_dist_x=0.5, min_dist_y=0.5, car_init_x2=-37, v_des2=12.5, ped_initial_states=pedestrian_init_state)



for cur_iter in range(num_iter):
    
    if cur_iter%100==0 :
        print(cur_iter, " out of ", num_iter)
    
    sim.reset([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    action_list = []
    reward = 0


    for i in range(search_depth):
        if(sim.is_goal() == True):
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

        #Calculate its reward:
        if(sim.is_goal() == False):
            reward = reward + mahalanobis_d(action, num_peds+1)
 
            
    #Final positions of car and ped:
    car_x=sim._car[2]
    car_y=sim._car[3]
    ped_x=sim._peds[0][2]
    ped_y=sim._peds[0][3]
    
    #Check if goal and give reward:
    if sim.is_goal() == False:
        reward = reward + (-10000 - 1000*(np.sqrt((car_x-ped_x)**2 + (car_y-ped_y)**2)))

    #Push current path to priority queue
    top_paths.put(copy.deepcopy(action_list), -reward)




failures = []
for i in range(num_paths):
    cur_path = top_paths.get()
    failures.append(cur_path)

filename = 'multi_car_random_sample_data/random_sample.pkl'
if not os.path.exists(os.path.dirname(filename)):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
with open(filename, 'wb+') as f:  
    pickle.dump([failures], f)


