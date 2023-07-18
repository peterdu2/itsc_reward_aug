import math
import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import csv
import os
import errno


plt.rcParams["font.family"] = "Times New Roman"

top_k = 50
num_trees = 128
folder_path = 'F1/'
param_type = 'ny'
idp_var = []
dp_var = []

if param_type == 'ax':
    ax_list = []
    avg_x_dev_list = []
    avg_x_spread_list = []
    avg_y_dev_list = []
    avg_y_spread_list = []
    ped_id = 1
    for param_id in range(num_trees):
        print(param_id)
        #AS_params are [[ax_min, ax_max], [ay_min, ay_max], [nvx_min, nvx_max],...,[ny_min,ny_max]]
        AS_params = (pickle.load(open(folder_path+str(param_id)+'.pkl', "rb" )))[2]
        ax_list.append(AS_params[0][1])

        max_x = -99999
        min_x = 99999
        avg_x_dev = 0
        avg_x_spread = 0
        max_y = -99999
        min_y = 99999
        avg_y_dev = 0
        avg_y_spread = 0
        for i in range(top_k):
            traj = (pickle.load(open(folder_path+str(param_id)+'.pkl', "rb" )))[0][i]
            start_x = traj[0][0][ped_id][2]
            end_x = traj[len(traj)-1][0][ped_id][2]
            x_dev = end_x-start_x
            avg_x_dev += x_dev
            if end_x > max_x:
                max_x = end_x
            if end_x < min_x:
                min_x = end_x

            start_y = traj[0][0][ped_id][3]
            end_y = traj[len(traj)-1][0][ped_id][3]
            y_dev = end_y-start_y
            avg_y_dev += y_dev
            if end_y > max_y:
                max_y = end_y
            if end_y < min_y:
                min_y = end_y

            x_spread = max_x-min_x
            avg_x_spread += x_spread
            y_spread = max_y-min_y
            avg_y_spread += y_spread

        avg_x_dev_list.append(avg_x_dev/top_k)
        avg_x_spread_list.append(avg_x_spread/top_k)
        avg_y_dev_list.append(avg_y_dev/top_k)
        avg_y_spread_list.append(avg_y_spread/top_k)

    filepath = folder_path+param_type+'.pkl'
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filepath, 'wb+') as f:  
        pickle.dump([ax_list, avg_x_dev_list, avg_x_spread_list, avg_y_dev_list, avg_y_spread_list], f)

    plotting_data = (pickle.load(open(filepath, "rb" )))
    plt.scatter(plotting_data[0], plotting_data[2])
    plt.savefig(folder_path+param_type+'_spread_x.png')
    plt.clf()
    plt.scatter(plotting_data[0], plotting_data[1])
    plt.savefig(folder_path+param_type+'_dev_x.png')
    plt.clf()
    plt.scatter(plotting_data[0], plotting_data[4])
    plt.savefig(folder_path+param_type+'_spread_y.png')
    plt.clf()
    plt.scatter(plotting_data[0], plotting_data[3])
    plt.savefig(folder_path+param_type+'_dev_y.png')
    plt.clf()

if param_type == 'ay':
    ay_list = []
    avg_x_dev_list = []
    avg_x_spread_list = []
    avg_y_dev_list = []
    avg_y_spread_list = []
    ped_id = 1
    for param_id in range(num_trees):
        print(param_id)
        #AS_params are [[ax_min, ax_max], [ay_min, ay_max], [nvx_min, nvx_max],...,[ny_min,ny_max]]
        AS_params = (pickle.load(open(folder_path+str(param_id)+'.pkl', "rb" )))[2]
        ay_list.append(AS_params[1][1])

        max_x = -99999
        min_x = 99999
        avg_x_dev = 0
        avg_x_spread = 0
        max_y = -99999
        min_y = 99999
        avg_y_dev = 0
        avg_y_spread = 0
        for i in range(top_k):
            traj = (pickle.load(open(folder_path+str(param_id)+'.pkl', "rb" )))[0][i]
            start_x = traj[0][0][ped_id][2]
            end_x = traj[len(traj)-1][0][ped_id][2]
            x_dev = end_x-start_x
            avg_x_dev += x_dev
            if end_x > max_x:
                max_x = end_x
            if end_x < min_x:
                min_x = end_x

            start_y = traj[0][0][ped_id][3]
            end_y = traj[len(traj)-1][0][ped_id][3]
            y_dev = end_y-start_y
            avg_y_dev += y_dev
            if end_y > max_y:
                max_y = end_y
            if end_y < min_y:
                min_y = end_y

            x_spread = max_x-min_x
            avg_x_spread += x_spread
            y_spread = max_y-min_y
            avg_y_spread += y_spread

        avg_x_dev_list.append(avg_x_dev/top_k)
        avg_x_spread_list.append(avg_x_spread/top_k)
        avg_y_dev_list.append(avg_y_dev/top_k)
        avg_y_spread_list.append(avg_y_spread/top_k)

    filepath = folder_path+param_type+'.pkl'
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filepath, 'wb+') as f:  
        pickle.dump([ay_list, avg_x_dev_list, avg_x_spread_list, avg_y_dev_list, avg_y_spread_list], f)

    plotting_data = (pickle.load(open(filepath, "rb" )))
    plt.scatter(plotting_data[0], plotting_data[2])
    plt.savefig(folder_path+param_type+'_spread_x.png')
    plt.clf()
    plt.scatter(plotting_data[0], plotting_data[1])
    plt.savefig(folder_path+param_type+'_dev_x.png')
    plt.clf()
    plt.scatter(plotting_data[0], plotting_data[4])
    plt.savefig(folder_path+param_type+'_spread_y.png')
    plt.clf()
    plt.scatter(plotting_data[0], plotting_data[3])
    plt.savefig(folder_path+param_type+'_dev_y.png')
    plt.clf()

if param_type == 'nx':
    nx_list = []
    avg_x_dev_list = [] #deviation (positive) from pedestrian starting x
    ped_id = 1

    for param_id in range(num_trees):
        print(param_id)
        #AS_params are [[ax_min, ax_max], [ay_min, ay_max], [nvx_min, nvx_max],...,[ny_min,ny_max]]
        AS_params = (pickle.load(open(folder_path+str(param_id)+'.pkl', "rb" )))[2]
        nx_list.append(AS_params[4][1])

        avg_x_dev = 0
        for i in range(top_k):
            traj = (pickle.load(open(folder_path+str(param_id)+'.pkl', "rb" )))[0][i]
            start_x = traj[0][0][ped_id][2]
            end_x = traj[len(traj)-1][0][ped_id][2] 
            avg_x_dev += abs(start_x-end_x)

        avg_x_dev_list.append(avg_x_dev/top_k)

    filepath = folder_path+param_type+'.pkl'
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filepath, 'wb+') as f:  
        pickle.dump([nx_list, avg_x_dev_list], f)

    plotting_data = (pickle.load(open(filepath, "rb" )))
    plt.scatter(plotting_data[0], plotting_data[1])
    plt.savefig(folder_path+param_type+'_dev_x.png')
    plt.clf()

if param_type == 'ny':
    ny_list = []
    avg_x_dev_list = [] #deviation (positive) from pedestrian starting x
    ped_id = 1

    for param_id in range(num_trees):
        print(param_id)
        #AS_params are [[ax_min, ax_max], [ay_min, ay_max], [nvx_min, nvx_max],...,[ny_min,ny_max]]
        AS_params = (pickle.load(open(folder_path+str(param_id)+'.pkl', "rb" )))[2]
        ny_list.append(AS_params[4][1])

        avg_x_dev = 0
        for i in range(top_k):
            traj = (pickle.load(open(folder_path+str(param_id)+'.pkl', "rb" )))[0][i]
            start_x = traj[0][0][ped_id][2]
            end_x = traj[len(traj)-1][0][ped_id][2] 
            avg_x_dev += abs(start_x-end_x)

        avg_x_dev_list.append(avg_x_dev/top_k)

    filepath = folder_path+param_type+'.pkl'
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filepath, 'wb+') as f:  
        pickle.dump([ny_list, avg_x_dev_list], f)

    plotting_data = (pickle.load(open(filepath, "rb" )))
    plt.scatter(plotting_data[0], plotting_data[1])
    plt.savefig(folder_path+param_type+'_dev_x.png')
    plt.clf()
'''
filepath = folder_path+param_type+'.pkl'
plotting_data = (pickle.load(open(filepath, "rb" )))
plt.scatter(plotting_data[0], plotting_data[2])
plt.show()
'''