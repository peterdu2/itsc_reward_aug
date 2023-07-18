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

c1_failure_centres = []
c1_ax_list = []
c1_ay_list = []
c1_nvx_list = []
c1_nvy_list = []
c1_nx_list = []
c1_ny_list = []

c2_failure_centres = []
c2_ax_list = []
c2_ay_list = []
c2_nvx_list = []
c2_nvy_list = []
c2_nx_list = []
c2_ny_list = []

single_cluster_idxs = []

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
    kmeans_single = KMeans(n_clusters=1, random_state=0).fit(cluster_data)
    kmeans_double = KMeans(n_clusters=2, random_state=0).fit(cluster_data)
    
    #Find single cluster trees 
    if kmeans_single.inertia_ < 20:
        c1_failure_centres.append(kmeans_single.cluster_centers_[0])
        c1_ax_list.append(AS_params[0])
        c1_ay_list.append(AS_params[1])
        c1_nvx_list.append(AS_params[2])
        c1_nvy_list.append(AS_params[3])
        c1_nx_list.append(AS_params[4])
        c1_ny_list.append(AS_params[5])
    #Double cluster trees
    else:
        c2_failure_centres.append(kmeans_double.cluster_centers_[0])
        c2_failure_centres.append(kmeans_double.cluster_centers_[1])
        c2_ax_list.append(AS_params[0])
        c2_ay_list.append(AS_params[1])
        c2_nvx_list.append(AS_params[2])
        c2_nvy_list.append(AS_params[3])
        c2_nx_list.append(AS_params[4])
        c2_ny_list.append(AS_params[5])

    #failure_centres.append(cluster_centre)

x_low, x_high = zip(*c2_ax_list)
y_low, y_high = zip(*c2_ay_list)

print("Average ax_high: "+ str(np.average(x_high)))
print("Std ax_high: "+ str(np.std(x_high)))
print("Average ay_high: "+ str(np.average(y_high)))
print("Std ay_high: "+ str(np.std(y_high)))

plt.scatter(*zip(*c2_failure_centres))
plt.show()

# histogram_data = []
# #Plot parameter interval visualization
# for param in c2_nvy_list:
#     plt.hlines(0,param[0],param[1],'red',alpha=0.05, lw=20)

#     #Create histogram using discretized frequencies
#     low = round(param[0], 2)
#     high = round(param[1], 2)
#     dp = low
#     while(dp <= high):
#         dp = round(dp, 2)
#         histogram_data.append(dp)
#         dp += 0.01

# plt.hist(histogram_data, bins='auto')
# plt.savefig('F3/graphs/double_cluster_nvy_hist.png')


# plt.show()
# plt.clf()
# plt.scatter(*zip(*c2_failure_centres))
# plt.show()
