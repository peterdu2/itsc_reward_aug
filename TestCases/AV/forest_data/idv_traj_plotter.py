import math
import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import csv

plt.rcParams["font.family"] = "Times New Roman"

top_k = 50
num_trees = 2048
tree_idx = 41
folder_path = 'F4/'
for param_id in range(tree_idx,tree_idx+1):
    AS_params = (pickle.load(open(folder_path+str(param_id)+'.pkl', "rb" )))[2]
    print(AS_params)
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
            plt.plot(end_state[1][2], end_state[1][3], marker="X", color='blue')
            plt.plot(end_state[0][1][2], end_state[0][1][3], marker='X', color='magenta')
            indicator = True
        else:
            plt.plot(end_state[1][2], end_state[1][3], marker="X", color='blue')
            plt.plot(end_state[0][1][2], end_state[0][1][3], marker='X', color='blue')

        plt.plot(end_state[2][2], end_state[2][3], marker="X", color='orange')
        #plt.plot(end_state[0][0][2], end_state[0][0][3], marker='.', color='orange')

        plt.plot(start_state[1][2], start_state[1][3], marker="*", color='blue')
        plt.plot(start_state[2][2], start_state[2][3], marker="*", color='orange')
        #plt.plot(start_state[0][0][2], start_state[0][0][3], marker='+', color='green')
        plt.plot(start_state[0][1][2], start_state[0][1][3], marker='*', color='magenta')
        
        # plt.annotate(str(AS_params[5]), xy=(0, 0), xycoords='axes fraction')
        # plt.annotate(str(AS_params[4]), xy=(0, 0.05), xycoords='axes fraction')
        # plt.annotate(str(AS_params[3]), xy=(0, 0.1), xycoords='axes fraction')
        # plt.annotate(str(AS_params[2]), xy=(0, 0.15), xycoords='axes fraction')
        # plt.annotate(str(AS_params[1]), xy=(0, 0.2), xycoords='axes fraction')
        # plt.annotate(str(AS_params[0]), xy=(0, 0.25), xycoords='axes fraction')
        # if indicator:
        #     plt.annotate("FAILURES FOUND", xy=(0, 0.30), xycoords='axes fraction')
        # else:
        #     plt.annotate("NONE FOUND", xy=(0, 0.30), xycoords='axes fraction')
        
        for state in traj:
            #STATE FORMAT: [ [[PED1],[PED2]] , [CAR1] , [CAR2] ]
            car_x.append(state[1][2])
            car_y.append(state[1][3])
            car2_x.append(state[2][2])
            car2_y.append(state[2][3])
            #ped1_x.append(state[0][0][2])
            #ped1_y.append(state[0][0][3])
            ped2_x.append(state[0][1][2])
            ped2_y.append(state[0][1][3])

        plt.plot(car_x, car_y, color='blue')
        plt.plot(car2_x, car2_y, color='orange')
        plt.plot(ped1_x, ped1_y, color='blue')
        plt.plot(ped2_x, ped2_y, color='magenta')

        plt.ylim(-1.5,1)
        plt.xlim(-9,1)
        plt.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

        filename = 'F4_idv_trees/'+str(tree_idx)+'/'+str(i)+'.png'
        #filename = folder_path+str(param_id)+'.png'
        plt.savefig(filename)
        plt.clf()