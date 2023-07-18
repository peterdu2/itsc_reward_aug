import math
import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import csv

plt.rcParams["font.family"] = "Times New Roman"

top_k = 50
num_trees = 495
folder_path = 'F4/'
for param_id in range(num_trees):
    print(param_id)
    indicator = False
    for i in range(top_k):
        traj = (pickle.load(open(folder_path+str(param_id)+'.pkl', "rb" )))[0][i]
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

        if abs(end_state[1][2]-end_state[0][1][2]) <= 0.5 and abs(end_state[1][3]-end_state[0][1][3]) <= 0.5:
            plt.plot(end_state[1][2], end_state[1][3], marker="X", color='blue', alpha=0.3)
            plt.plot(end_state[0][1][2], end_state[0][1][3], marker='X', color='magenta', alpha=0.3)
            indicator = True
        else:
            plt.plot(end_state[1][2], end_state[1][3], marker="X", color='blue', alpha=0.3)
            plt.plot(end_state[0][1][2], end_state[0][1][3], marker='X', color='magenta', alpha=0.3)

        plt.plot(end_state[2][2], end_state[2][3], marker="X", color='orange', alpha=0.3)
        #plt.plot(end_state[0][0][2], end_state[0][0][3], marker='X', color='green', alpha=0.3)

        plt.plot(start_state[1][2], start_state[1][3], marker="*", color='blue', alpha=0.3)
        plt.plot(start_state[2][2], start_state[2][3], marker="*", color='orange', alpha=0.3)
        #plt.plot(start_state[0][0][2], start_state[0][0][3], marker='*', color='green', alpha=0.3)
        plt.plot(start_state[0][1][2], start_state[0][1][3], marker='*', color='magenta', alpha=0.3)
        
        
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

        plt.plot(car_x, car_y, color='blue')
        plt.plot(car2_x, car2_y, color='orange')
        #plt.plot(ped1_x, ped1_y, color='green')
        plt.plot(ped2_x, ped2_y, color='magenta')

    filename = 'F4_all_tree_overlay/'+str(param_id)+'.png'
    #filename = folder_path+str(param_id)+'.png'
    plt.savefig(filename)
    #plt.clf()