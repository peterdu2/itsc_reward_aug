import numpy as np
import pickle
import math
import matplotlib.pyplot as plt
import os
import errno




def traj_similarity(trajectories, num_segments, comp_traj_idx):

    ped1 = trajectories[comp_traj_idx]
    similarity_idx = 0

    for j in range(len(trajectories)):
        cur_sim = 0
        if j != comp_traj_idx:
            ped2 = trajectories[j]

            ped1_seg_len = len(ped1)//num_segments  #Floor division 
            ped2_seg_len = len(ped2)//num_segments

            #Compare segments 
            for i in range(num_segments):
                if(i == num_segments-1):
                    cur_ped1_seg = [ped1[i*ped1_seg_len], ped1[len(ped1)-1]]
                    cur_ped2_seg = [ped2[i*ped2_seg_len], ped2[len(ped2)-1]]
                else:
                    cur_ped1_seg = [ped1[i*ped1_seg_len], ped1[(i+1)*ped1_seg_len-1]]
                    cur_ped2_seg = [ped2[i*ped2_seg_len], ped2[(i+1)*ped2_seg_len-1]]

                #Compare segment centroids
                centroid1 = np.add(cur_ped1_seg[0], cur_ped1_seg[1])/2
                centroid2 = np.add(cur_ped2_seg[0], cur_ped2_seg[1])/2
                dist = np.linalg.norm(centroid1-centroid2)
                cur_sim = dist + cur_sim

            '''
            xs = [x[0] for x in test_graph]
            ys = [x[1] for x in test_graph]
            plt.plot(xs, ys)
            plt.show()
            '''

        similarity_idx = similarity_idx + cur_sim

    return similarity_idx




print(" ")
num_peds = 3;
num_paths = 20;


##################################################################
##################################################################
### TWO PEDS ####
##################################################################
##################################################################
print("NO DISCOUNT")
open('three_peds/t1_no_discount/similarities.txt', 'w').close()
total = 0
for cur_ped in range(num_peds):
    trajectories = []
    for i in range(num_paths):
        pickle_path  = 'three_peds/t1_no_discount/pickles/data'+str(i)+'.pkl'
        loaded_data = pickle.load(open(pickle_path, "rb" ))
        ped_x = loaded_data[4+2*cur_ped]
        ped_y = loaded_data[5+2*cur_ped]
        cur_traj = [list(pair) for pair in zip(ped_x, ped_y)]
        trajectories.append(cur_traj)

    sum = 0
    for cur_idx in range(num_paths):
        similarity = traj_similarity(trajectories, 20, cur_idx)
        sum = sum + similarity
        print("Ped", cur_ped+1, " path", cur_idx, " similarity is: ", similarity, file=open('three_peds/t1_no_discount/similarities.txt', 'a'))
        print("Ped", cur_ped+1, " path", cur_idx, " similarity is: ", similarity)
    total = total + sum
    print("Ped", cur_ped+1, " overall similarity is: ", sum, file=open('three_peds/t1_no_discount/similarities.txt', 'a'))
    print("Ped", cur_ped+1, " overall similarity is: ", sum)
    print(" ", file=open('three_peds/t1_no_discount/similarities.txt', 'a'))
    print(" ")
print("AVERAGE: ", total/num_peds, file=open('three_peds/t1_no_discount/similarities.txt', 'a'))




print("WITH DISCOUNT")
open('three_peds/t1_w_discount/traj_050_state_0/similarities.txt', 'w').close()
total = 0
for cur_ped in range(num_peds):
    trajectories = []
    for i in range(num_paths):
        pickle_path  = 'three_peds/t1_w_discount/traj_050_state_0/pickles/data'+str(i)+'.pkl'
        loaded_data = pickle.load(open(pickle_path, "rb" ))
        ped_x = loaded_data[3+2*cur_ped]
        ped_y = loaded_data[4+2*cur_ped]
        cur_traj = [list(pair) for pair in zip(ped_x, ped_y)]
        trajectories.append(cur_traj)

    sum = 0
    for cur_idx in range(num_paths):
        similarity = traj_similarity(trajectories, 20, cur_idx)
        sum = sum + similarity
        print("Ped", cur_ped+1, " path", cur_idx, " similarity is: ", similarity, file=open('three_peds/t1_w_discount/traj_050_state_0/similarities.txt', 'a'))
        print("Ped", cur_ped+1, " path", cur_idx, " similarity is: ", similarity)
    total = total + sum
    print("Ped", cur_ped+1, " overall similarity is: ", sum, file=open('three_peds/t1_w_discount/traj_050_state_0/similarities.txt', 'a'))
    print("Ped", cur_ped+1, " overall similarity is: ", sum)
    print(" ", file=open('three_peds/t1_w_discount/traj_050_state_0/similarities.txt', 'a'))
    print(" ")
print("AVERAGE: ", total/num_peds, file=open('three_peds/t1_w_discount/traj_050_state_0/similarities.txt', 'a'))




open('three_peds/t1_w_discount/traj_100_state_0/similarities.txt', 'w').close()
total = 0
for cur_ped in range(num_peds):
    trajectories = []
    for i in range(num_paths):
        pickle_path  = 'three_peds/t1_w_discount/traj_100_state_0/pickles/data'+str(i)+'.pkl'
        loaded_data = pickle.load(open(pickle_path, "rb" ))
        ped_x = loaded_data[3+2*cur_ped]
        ped_y = loaded_data[4+2*cur_ped]
        cur_traj = [list(pair) for pair in zip(ped_x, ped_y)]
        trajectories.append(cur_traj)

    sum = 0
    for cur_idx in range(num_paths):
        similarity = traj_similarity(trajectories, 20, cur_idx)
        sum = sum + similarity
        print("Ped", cur_ped+1, " path", cur_idx, " similarity is: ", similarity, file=open('three_peds/t1_w_discount/traj_100_state_0/similarities.txt', 'a'))
        print("Ped", cur_ped+1, " path", cur_idx, " similarity is: ", similarity)
    total = total + sum
    print("Ped", cur_ped+1, " overall similarity is: ", sum, file=open('three_peds/t1_w_discount/traj_100_state_0/similarities.txt', 'a'))
    print("Ped", cur_ped+1, " overall similarity is: ", sum)
    print(" ", file=open('three_peds/t1_w_discount/traj_100_state_0/similarities.txt', 'a'))
    print(" ")
print("AVERAGE: ", total/num_peds, file=open('three_peds/t1_w_discount/traj_100_state_0/similarities.txt', 'a'))




open('three_peds/t1_w_discount/traj_150_state_0/similarities.txt', 'w').close()
total = 0
for cur_ped in range(num_peds):
    trajectories = []
    for i in range(num_paths):
        pickle_path  = 'three_peds/t1_w_discount/traj_150_state_0/pickles/data'+str(i)+'.pkl'
        loaded_data = pickle.load(open(pickle_path, "rb" ))
        ped_x = loaded_data[3+2*cur_ped]
        ped_y = loaded_data[4+2*cur_ped]
        cur_traj = [list(pair) for pair in zip(ped_x, ped_y)]
        trajectories.append(cur_traj)

    sum = 0
    for cur_idx in range(num_paths):
        similarity = traj_similarity(trajectories, 20, cur_idx)
        sum = sum + similarity
        print("Ped", cur_ped+1, " path", cur_idx, " similarity is: ", similarity, file=open('three_peds/t1_w_discount/traj_150_state_0/similarities.txt', 'a'))
        print("Ped", cur_ped+1, " path", cur_idx, " similarity is: ", similarity)
    total = total + sum
    print("Ped", cur_ped+1, " overall similarity is: ", sum, file=open('three_peds/t1_w_discount/traj_150_state_0/similarities.txt', 'a'))
    print("Ped", cur_ped+1, " overall similarity is: ", sum)
    print(" ", file=open('three_peds/t1_w_discount/traj_150_state_0/similarities.txt', 'a'))
    print(" ")
print("AVERAGE: ", total/num_peds, file=open('three_peds/t1_w_discount/traj_150_state_0/similarities.txt', 'a'))


