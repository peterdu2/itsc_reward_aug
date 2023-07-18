import math
import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import csv
import os
import errno
from sklearn.cluster import KMeans

folder_path = 'F3/'
num_trees = 128
top_k = 50

failure_centres = []
ax_list = []
ay_list = []
nvx_list = []
nvy_list = []
nx_list = []
ny_list = []

#Generate clusters for each tree
for param_id in range(num_trees):
    cluster_data = []

    #Import parameters
    AS_params = (pickle.load(open(folder_path+str(param_id)+'.pkl', 'rb')))[2]
    #Import trajectories and assemble array of end points 
    traj_list = (pickle.load(open(folder_path+str(param_id)+'.pkl', 'rb')))[0]
    for i in range(top_k):
        cur_traj = traj_list[i]
        end_state = cur_traj[len(cur_traj)-1]

        #Using pedestrian 2 (ped idx = 1)
        ped_end_state = [end_state[0][1][2],end_state[0][1][3]]
        cluster_data.append(ped_end_state)


    cluster_data = np.array(cluster_data)
    kmeans = KMeans(n_clusters=1, random_state=0).fit(cluster_data)
    
    #find single cluster trees 
    if kmeans.inertia_ < 20:
        cluster_centre = kmeans.cluster_centers_[0]
        ax_list.append(AS_params[0])
        ay_list.append(AS_params[1])
        nvx_list.append(AS_params[2])
        nvy_list.append(AS_params[3])
        nx_list.append(AS_params[4])
        ny_list.append(AS_params[5])
    #else:
        #cluster_centre = np.array([-999,-999])

    failure_centres.append(cluster_centre)

x_low, x_high = zip(*ax_list)
y_low, y_high = zip(*ay_list)

print("Average ax_high: "+ str(np.average(x_high)))
print("Std ax_high: "+ str(np.std(x_high)))
print("Average ay_high: "+ str(np.average(y_high)))
print("Std ay_high: "+ str(np.std(y_high)))

#plot parameter interval visualization
for param in ax_list:
    plt.hlines(0,param[0],param[1],'red',alpha=0.09, lw=20)

plt.show()
plt.clf()
plt.scatter(*zip(*failure_centres))
plt.show()