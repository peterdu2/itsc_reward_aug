import math
import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import csv

plt.rcParams["font.family"] = "Times New Roman"

top_k = 50
num_trees = 2048
folder_path = 'F4/'
for param_id in range(num_trees):
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
            plt.plot(end_state[1][2], end_state[1][3], marker="X", color='orange')
            plt.plot(end_state[0][1][2], end_state[0][1][3], marker='+', color='red')
            indicator = True
        else:
            plt.plot(end_state[1][2], end_state[1][3], marker="X", color='blue')
            plt.plot(end_state[0][1][2], end_state[0][1][3], marker='+', color='blue')

        plt.plot(end_state[2][2], end_state[2][3], marker="*", color='orange')
        plt.plot(end_state[0][0][2], end_state[0][0][3], marker='.', color='orange')

        plt.plot(start_state[1][2], start_state[1][3], marker="X", color='green')
        plt.plot(start_state[2][2], start_state[2][3], marker="*", color='green')
        plt.plot(start_state[0][0][2], start_state[0][0][3], marker='+', color='green')
        plt.plot(start_state[0][1][2], start_state[0][1][3], marker='.', color='green')
        
        plt.annotate(str(AS_params[5]), xy=(0, 0), xycoords='axes fraction')
        plt.annotate(str(AS_params[4]), xy=(0, 0.05), xycoords='axes fraction')
        plt.annotate(str(AS_params[3]), xy=(0, 0.1), xycoords='axes fraction')
        plt.annotate(str(AS_params[2]), xy=(0, 0.15), xycoords='axes fraction')
        plt.annotate(str(AS_params[1]), xy=(0, 0.2), xycoords='axes fraction')
        plt.annotate(str(AS_params[0]), xy=(0, 0.25), xycoords='axes fraction')
        if indicator:
            plt.annotate("FAILURES FOUND", xy=(0, 0.30), xycoords='axes fraction')
        else:
            plt.annotate("NONE FOUND", xy=(0, 0.30), xycoords='axes fraction')
        
    filename = folder_path+str(param_id)+'_idv.png'
    #filename = folder_path+str(param_id)+'.png'
    plt.savefig(filename)
    plt.clf()