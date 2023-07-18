import math
import numpy as np
import pickle
import matplotlib.pyplot as plt
import scipy.stats
from matplotlib.patches import Rectangle
import csv
import os
import errno
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture



############################## PLOTTING FUNCTIONS #############################################
from matplotlib.patches import Ellipse

def draw_ellipse(position, covariance, ax=None, **kwargs):
    """Draw an ellipse with a given position and covariance"""
    ax = ax or plt.gca()
    
    # Convert covariance to principal axes
    if covariance.shape == (2, 2):
        U, s, Vt = np.linalg.svd(covariance)
        angle = np.degrees(np.arctan2(U[1, 0], U[0, 0]))
        width, height = 2 * np.sqrt(s)
    else:
        angle = 0
        width, height = 2 * np.sqrt(covariance)
    
    # Draw the Ellipse
    for nsig in range(1, 4):
        ax.add_patch(Ellipse(position, nsig * width, nsig * height,
                             angle, **kwargs))
        
def plot_gmm(labels, gmm, X, label=True, ax=None):
    #ax = ax or plt.gca()
    #labels = gmm.fit(X).predict(X)

    fig, ax = plt.subplots()
    label=0
    for color in ['red', 'green', 'blue', 'orange', 'purple']:
        plot_data_x = []
        plot_data_y = []
        for i in range(len(X)):
            if labels[i] == label:
                plot_data_x.append(X[i][0])
                plot_data_y.append(X[i][1])
        ax.scatter(plot_data_x, plot_data_y, c=color, label='C'+str(label))
        label+=1
    
    w_factor = 0.2 / gmm.weights_.max()
    for pos, covar, w in zip(gmm.means_, gmm.covariances_, gmm.weights_):
        draw_ellipse(pos, covar, alpha=w * w_factor)

    #plt.title('GMM Clusters', fontsize=16)
    ax.legend()
    plt.show()


def normal_plotter(mean, var):
    mean = mean
    std = var**0.5

    x_min = mean+0.6
    x_max = mean-0.6

    x = np.linspace(x_min, x_max, 100)
    y = scipy.stats.norm.pdf(x,mean,std)

    plt.plot(x,y, color='coral')
    plt.grid()
    plt.xlim(x_min,x_max)
    plt.ylim(0,6)
    plt.xlabel('x')
    plt.ylabel('Normal Distribution')

    plt.show()

def normal_plotter_multi(mean, var, col_obj, row_cnt, col_cnt, raw_data=None):
    std = var**0.5
    mean = mean

    x_min = mean+0.6
    x_max = mean-0.6

    x = np.linspace(x_min, x_max, 100)
    y = scipy.stats.norm.pdf(x,mean,std)

    if col_cnt == 0:
        color = 'red'
    elif col_cnt == 1:
        color = 'green'
    elif col_cnt == 2:
        color = 'blue'
    elif col_cnt == 3:
        color = 'orange'
    else:
        color = 'purple'

    col_obj.plot(x,y, color=color)
    #col_obj.hist(raw_data, bins=10)
    col_obj.set_xlim([-1,1])
    col_obj.set_ylim([0,6])
    col_obj.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

    if row_cnt == 5:
        col_obj.set_xlabel('C'+str(col_cnt))

    if col_cnt == 0:
        if row_cnt == 0:
            col_obj.set_ylabel('AX')
        elif row_cnt == 1:
            col_obj.set_ylabel('AY')
        elif row_cnt == 2:
            col_obj.set_ylabel('NVX')
        elif row_cnt == 3:
            col_obj.set_ylabel('NVY')
        elif row_cnt == 4:
            col_obj.set_ylabel('NX')
        else:
            col_obj.set_ylabel('NY')




# folder_path = 'F4/'
# num_trees = 495
# top_k = 50

# cluster_failure_centres = []
# param_list = []
# tree_id_list = []

# #Generate clusters for each tree
# for param_id in range(num_trees):
#     cluster_data = []

#     #Import parameters
#     AS_params = (pickle.load(open(folder_path+str(param_id)+'.pkl', 'rb')))[2]
#     #Import trajectories and assemble array of end points 
#     traj_list = (pickle.load(open(folder_path+str(param_id)+'.pkl', 'rb')))[0]

#     failure_indicator = False

#     for i in range(top_k):
#         cur_traj = traj_list[i]
#         end_state = cur_traj[len(cur_traj)-1]

#         #Get the goal states
#         if abs(end_state[1][2]-end_state[0][1][2]) <= 0.5 and abs(end_state[1][3]-end_state[0][1][3]) <= 0.5:
#             #Using pedestrian 2 (ped idx = 1)
#             ped_end_state = [end_state[0][1][2],end_state[0][1][3]]
#             cluster_data.append(ped_end_state)
#             failure_indicator = True

#     #If failure occurs in tree, generate cluster and append to failure list
#     if failure_indicator:
#         cluster_data = np.array(cluster_data)
#         kmeans_single = KMeans(n_clusters=1, random_state=0).fit(cluster_data)

#         #Filter out high inertia results                                            (TODO: handle multi cluster trees)
#         if(kmeans_single.inertia_ < 5):
#             cluster_failure_centres.append(kmeans_single.cluster_centers_[0].tolist())
#             param_list.append(AS_params)
#             tree_id_list.append(param_id)


# Determine optimal number of components
# n_components = np.arange(1, 21)
# models = [GaussianMixture(n, covariance_type='full', random_state=0).fit(np.array(cluster_failure_centres))
#           for n in n_components]

# plt.plot(n_components, [m.bic(np.array(cluster_failure_centres)) for m in models], label='BIC')
# plt.plot(n_components, [m.aic(np.array(cluster_failure_centres)) for m in models], label='AIC')
# plt.legend(loc='best')
# plt.xlabel('n_components');

# gmm = GaussianMixture(n_components=5).fit(cluster_failure_centres)
# labels = gmm.predict(cluster_failure_centres)
# plt.scatter(*zip(*cluster_failure_centres), c=labels, s=40, cmap='viridis');
# plt.show()

# filepath = 'temp_data.pkl'
# with open(filepath, 'wb+') as f:  
#     pickle.dump([cluster_failure_centres, param_list, tree_id_list, gmm], f)








#Process GaussianMM data from pickle
gmm = (pickle.load(open('temp_data.pkl', 'rb')))[3]
cluster_failure_centres = (pickle.load(open('temp_data.pkl', 'rb')))[0]
param_list = (pickle.load(open('temp_data.pkl', 'rb')))[1]
tree_id_list = (pickle.load(open('temp_data.pkl', 'rb')))[2]
labels = gmm.predict(cluster_failure_centres)


num_labels = 5
sorted_param_lists = [] #list will be: [[params for label 1], [params for label2],...]
for i in range(num_labels):
    sorted_param_lists.append([])

for idx in range(len(cluster_failure_centres)):
    cur_label = labels[idx]
    sorted_param_lists[cur_label].append(param_list[idx])



means = []
variances = []
raw_data = []

#calculate averages for means
for label in range(num_labels):
    ax_list = []
    ay_list = []
    nvx_list = []
    nvy_list = []
    nx_list = []
    ny_list = []
    for param in sorted_param_lists[label]:
        ax_list.append(param[0][0])   #params are [mean, var] var=0.2 for all examples
        ay_list.append(param[1][0])
        nvx_list.append(param[2][0])
        nvy_list.append(param[3][0])
        nx_list.append(param[4][0])
        ny_list.append(param[5][0])
    mean_avg = [np.mean(ax_list), np.mean(ay_list), np.mean(nvx_list), np.mean(nvy_list), np.mean(nx_list), np.mean(ny_list)]
    var_avg = [np.var(ax_list), np.var(ay_list), np.var(nvx_list), np.var(nvy_list), np.var(nx_list), np.var(ny_list)]
    print("The averaged means for cluster " + str(label) + " are: ")
    print(mean_avg)
    print("The vars for cluster " + str(label) + " are: ")
    print(var_avg)
    print(" ")

    means.append(mean_avg)
    variances.append(var_avg)
    raw_data.append([ax_list, ay_list, nvx_list, nvy_list, nx_list, ny_list])

    #plt.hist(ay_list, bins=10)
    #normal_plotter(mean_avg[1],var_avg[1])


fig, ax = plt.subplots(nrows=6, ncols=5)
row_cnt = 0
col_cnt = 0
for row in ax:
    for col in row:
        mean = means[col_cnt][row_cnt]
        var = variances[col_cnt][row_cnt]
        rd = raw_data[col_cnt][row_cnt]
        normal_plotter_multi(mean,var,col,row_cnt,col_cnt)
        col_cnt += 1
    row_cnt += 1
    col_cnt = 0
#fig.suptitle("Parameter Distributions", fontsize=16)
plt.show()

plot_gmm(labels, gmm, np.array(cluster_failure_centres))




