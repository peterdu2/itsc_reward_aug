# Import the example classes
from mylab.simulators.multi_car_simulator import multi_car_simulator
from mylab.rewards.multi_car_reward import multi_car_reward
from mylab.spaces.example_av_spaces import ExampleAVSpaces
from mylab.spaces.gaussian_spaces import GaussianSpaces


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

np.random.seed(0)

max_path_length = 100 #max number of actions in a sequence
top_k = 50            #number of trajectories to return

pedestrian_init_state = [[0,-0.5,0,3],[0,0.5,0,-3]]


#Object creation for initial MCTS 
reward_function = multi_car_reward(num_peds=2)
spaces = ExampleAVSpaces(num_peds=3) #Set to 3, last action used by car2
sim = multi_car_simulator(num_peds=2,use_seed=False,spaces=spaces, max_path_length=max_path_length, car_init_x=-20, v_des=11.11, min_dist_x=0.5, min_dist_y=0.5, car_init_x2=-37, v_des2=12.5, ped_initial_states=pedestrian_init_state)
env = ASTEnv(action_only=True,
             open_loop=False,
             fixed_init_state=True,
             simulator=sim,
             reward_function=reward_function,
             spaces=spaces
             )
ast_params = AST_AS.ASTParams(max_path_length)
ast = AST_AS.AdaptiveStressTestAS(ast_params, env)

'''
#Initial MCTS run
result, initial_trajectories = AST_MCTS.stress_test_multi(ast, top_k, 200000, max_path_length, 1.0)
filename = 'initial_run_data/base_trajectories.pkl'
if not os.path.exists(os.path.dirname(filename)):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
with open('initial_run_data/base_trajectories.pkl', 'wb+') as f:  
    pickle.dump([initial_trajectories, result], f)

'''



initial_trajectories = (pickle.load(open( 'initial_run_data/base_trajectories.pkl', "rb" )))[0]

#Select Critical States:
crit_states = Helpers.get_critical_states(n_step_critical=30, trajectories=initial_trajectories)

'''
def MCTS_thread(top_k, iter_num, max_path_length, sim_reward, AS_params, filepath):
    #Object creation for MCTS forest
    reward_function = multi_car_reward(num_peds=2)
    spaces = ExampleAVSpaces(num_peds=3, n_vx_low=0.9, n_vx_high=1.0, n_vy_low=0.9, n_vy_high=1.0, n_x_low=0.9, n_x_high=1.0, n_y_low=0.9, n_y_high=1.0) #Set to 3, last action used by car2
    car1_x = crit_states[11][2][2]
    car1_v_des = crit_states[11][2][0]
    car2_x = crit_states[11][3][2]
    car2_v_des = crit_states[11][3][0]
    pedestrian_init_state = [crit_states[11][0], crit_states[11][1]]
    sim = multi_car_simulator(num_peds=2,use_seed=False,spaces=spaces,max_path_length=max_path_length, car_init_x=car1_x, v_des=car1_v_des, min_dist_x=0.5, min_dist_y=0.5, car_init_x2=car2_x, v_des2=car2_v_des, ped_initial_states=pedestrian_init_state)
    env = ASTEnv(action_only=True,
                 open_loop=False,
                 fixed_init_state=True,
                 simulator=sim,
                 reward_function=reward_function,
                 spaces=spaces
                 )
    ast = AST_AS.AdaptiveStressTestAS(ast_params, env)

    result, test_trajectory = AST_MCTS.stress_test_multi(ast, top_k, iter_num, max_path_length, sim_reward)

    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filepath, 'wb+') as f:  
        pickle.dump([initial_trajectories, result, AS_params], f)

num_threads = 2

for i in range(num_threads):

    #AS_params are [[ax_min, ax_max], [ay_min, ay_max], [nvx_min, nvx_max],...,[ny_min,ny_max]]
    AS_params = [[-1,1],[-1,1],[0,1],[0,1],[0,1],[i*0.1,(i+1)*0.1]]
    filepath = 'forest_data/'+str(i)+'.pkl'
    thread = threading.Thread(target=MCTS_thread, args=(5,100,50,1.0, AS_params, filepath))
    thread.start()
'''


num_trees = 2048
crit_state_idx = 21
for i in range(num_trees):
    print(i)
    ax_mean = random.uniform(-0.6,0.6)
    ax_sd = 0.2
    ay_mean = random.uniform(-0.6,0.6)
    ay_sd = 0.2
    nvx_mean = random.uniform(0,0.5)
    nvx_sd = 0.2
    nvy_mean = random.uniform(0,0.5)
    nvy_sd = 0.2
    nx_mean = random.uniform(0,0.5)
    nx_sd = 0.2
    ny_mean = random.uniform(0,0.5)
    ny_sd = 0.2

    AS_params = [[ax_mean,ax_sd],[ay_mean,ay_sd],[nvx_mean,nvx_sd],[nvy_mean,nvy_sd],[nx_mean,nx_sd],[ny_mean,ny_sd]]
    print(AS_params)
    #Object creation for MCTS forest
    reward_function = multi_car_reward(num_peds=2)
    spaces = GaussianSpaces(num_peds=3,    #Set to 3, last action used by car2
                            means=[ax_mean, ay_mean, nvx_mean, nvy_mean, nx_mean, ny_mean],
                            sds= [ax_sd, ay_sd, nvx_sd, nvy_sd, nx_sd, ny_sd]
                            )

    car1_x = crit_states[crit_state_idx][2][2]
    car1_v_des = crit_states[crit_state_idx][2][0]
    car2_x = crit_states[crit_state_idx][3][2]
    car2_v_des = crit_states[crit_state_idx][3][0]
    pedestrian_init_state = [crit_states[crit_state_idx][0], crit_states[crit_state_idx][1]]
    sim = multi_car_simulator(num_peds=2,
                            use_seed=False,
                            spaces=spaces,
                            max_path_length=max_path_length, 
                            car_init_x=car1_x, 
                            v_des=car1_v_des, 
                            min_dist_x=0.5, 
                            min_dist_y=0.5, 
                            car_init_x2=car2_x, 
                            v_des2=car2_v_des, 
                            ped_initial_states=pedestrian_init_state
                            )

    env = ASTEnv(action_only=True,
                 open_loop=False,
                 fixed_init_state=True,
                 simulator=sim,
                 reward_function=reward_function,
                 spaces=spaces
                 )

    ast = AST_AS.AdaptiveStressTestAS(ast_params, env)

    top_k = 50
    iter_num = 20000
    max_path_length = 50
    sim_reward = 1.0

    result, forest_trajectories = AST_MCTS.stress_test_multi(ast, top_k, iter_num, max_path_length, sim_reward)

    # CHANGE NAME EACH TIME
    filepath = 'forest_data/F4/'+str(i)+'.pkl'
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filepath, 'wb+') as f:  
        pickle.dump([forest_trajectories, result, AS_params], f)








###############################################################################
###############################################################################
##################### Generate graphs for testing #############################
###############################################################################
###############################################################################

'''
traj = (pickle.load(open( 'initial_run_data/base_trajectories.pkl', "rb" )))[0]
traj = traj[21]
car_x = []
car_y = []
car2_x = []
car2_y = []
ped1_x = []
ped1_y = []
ped2_x = []
ped2_y = []
end_state = traj[len(traj)-1]
crit_state = crit_states[21]
print(crit_state)
plt.plot(end_state[1][2], end_state[1][3], marker="X", color='red')
plt.plot(end_state[2][2], end_state[2][3], marker="*", color='red')
plt.plot(end_state[0][0][2], end_state[0][0][3], marker='+', color='red')
plt.plot(end_state[0][1][2], end_state[0][1][3], marker='.', color='red')
plt.plot(crit_state[1][2], crit_state[1][3], marker="X", color='green')
plt.plot(crit_state[2][2], crit_state[2][3], marker="*", color='green')
plt.plot(crit_state[3][2], crit_state[3][3], marker='+', color='green')
plt.plot(crit_state[0][2], crit_state[0][3], marker='.', color='green')
for state in traj:

    #STATE FORMAT: [ [[PED1],[PED2]] , [CAR1] , [CAR2] ]

    car_x.append(state[1][2])
    car_y.append(state[1][3])
    car2_x.append(state[2][2])
    car2_y.append(state[2][3])
    ped1_x.append(state[0][0][2])
    ped1_y.append(state[0][0][3])
    ped2_x.append(state[0][1][2])
    ped2_y.append(state[0][1][3])


plt.plot(car_x, car_y)
plt.plot(car2_x, car2_y)
plt.plot(ped1_x, ped1_y)
plt.plot(ped2_x, ped2_y)
filename = 'graphs/T3_forest.png'
plt.savefig(filename)
plt.clf()
'''

'''
counter = 0
for traj in initial_trajectories:
    car_x = []
    car_y = []
    car2_x = []
    car2_y = []
    ped1_x = []
    ped1_y = []
    ped2_x = []
    ped2_y = []
    end_state = traj[len(traj)-1]
    plt.plot(end_state[1][2], end_state[1][3], marker="X")
    plt.plot(end_state[2][2], end_state[2][3], marker="*")
    plt.plot(end_state[0][0][2], end_state[0][0][3], marker='+')
    plt.plot(end_state[0][1][2], end_state[0][1][3], marker='.')
    for state in traj:

        #STATE FORMAT: [ [[PED1],[PED2]] , [CAR1] , [CAR2] ]

        car_x.append(state[1][2])
        car_y.append(state[1][3])
        car2_x.append(state[2][2])
        car2_y.append(state[2][3])
        ped1_x.append(state[0][0][2])
        ped1_y.append(state[0][0][3])
        ped2_x.append(state[0][1][2])
        ped2_y.append(state[0][1][3])

    
    plt.plot(car_x, car_y)
    plt.plot(car2_x, car2_y)
    plt.plot(ped1_x, ped1_y)
    plt.plot(ped2_x, ped2_y)
    filename = 'graphs/1'+str(counter)+'.png'
    plt.savefig(filename)
    plt.clf()
    counter+=1

counter = 0


for traj in test_traj2[0]:
    car_x = []
    car_y = []
    car2_x = []
    car2_y = []
    ped1_x = []
    ped1_y = []
    ped2_x = []
    ped2_y = []
    starting_state = traj[0]
    plt.plot(starting_state[1][2], starting_state[1][3], marker="X")
    plt.plot(starting_state[2][2], starting_state[2][3], marker="*")
    for state in traj:

        #STATE FORMAT: [ [[PED1],[PED2]] , [CAR1] , [CAR2] ]

        car_x.append(state[1][2])
        car_y.append(state[1][3])
        car2_x.append(state[2][2])
        car2_y.append(state[2][3])
        ped1_x.append(state[0][0][2])
        ped1_y.append(state[0][0][3])
        ped2_x.append(state[0][1][2])
        ped2_y.append(state[0][1][3])

    
    plt.plot(car_x, car_y)
    plt.plot(car2_x, car2_y)
    plt.plot(ped1_x, ped1_y)
    plt.plot(ped2_x, ped2_y)
    filename = '2'+str(counter)+'.png'
    plt.savefig(filename)
    plt.clf()
    counter+=1
    

'''




