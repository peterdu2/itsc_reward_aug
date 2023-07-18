import math
import numpy as np
import pickle
import matplotlib.pyplot as plt

top_k = 75

##################################
# OVERLAY WITH FADE 
##################################

for i in range(1):
    trajectory_list = pickle.load(open( 'failure_trend_data/'+str(36)+'.1.pkl', "rb" ))[0]
    is_goals = pickle.load(open( 'failure_trend_data/'+str(36)+'.1.pkl', "rb" ))[1]

    print(is_goals)

    counter = 0
    for tv in is_goals:
        if tv == True:
            counter += 1

    print(counter)
    '''
    #each entry in a trajectory is in format: [[[ped1, ped2]], [car1], [car2]]
    for i in range(top_k):
        traj = trajectory_list[i]
        car_x = []
        car_y = []
        car2_x = []
        car2_y = []
        ped1_x = []
        ped1_y = []
        ped2_x = []
        ped2_y = []
        
        end_state = traj[len(traj)-1]
        start_state = traj[0]
        plt.plot(end_state[1][2], end_state[1][3], marker="X", color='orange') #car1
        plt.plot(end_state[2][2], end_state[2][3], marker="*", color='orange')  #car2
        plt.plot(end_state[0][0][2], end_state[0][0][3], marker='+', color='red') #ped1
        plt.plot(end_state[0][1][2], end_state[0][1][3], marker='.', color='red') #ped2
        plt.plot(start_state[1][2], start_state[1][3], marker="X", color='green') 
        plt.plot(start_state[2][2], start_state[2][3], marker="*", color='green')
        plt.plot(start_state[0][0][2], start_state[0][0][3], marker='+', color='green')
        plt.plot(start_state[0][1][2], start_state[0][1][3], marker='.', color='green')
        
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


        plt.plot(car_x, car_y, color='black')
        plt.plot(car2_x, car2_y, color='orange')
        plt.plot(ped1_x, ped1_y, color='blue')
        plt.plot(ped2_x, ped2_y, color='magenta')
    filename = 'test2.png'
    plt.savefig(filename)
    plt.clf()

    '''