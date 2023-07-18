import math
import numpy as np
import pickle
import matplotlib.pyplot as plt

top_k = 75

##################################
# OVERLAY WITH FADE 
##################################

for i in range(32,35):
    trajectory_list = pickle.load(open('forest_data/F2/0.pkl', "rb"))[1]
    action_list = pickle.load(open('forest_data/F2/0.pkl', "rb"))[2]

    for j in range(50):
        tl = []
        for traj in trajectory_list[j]:
            tl.append(traj)

        car1 = [[],[]]
        car2 = [[],[]]
        for element in tl:
            car1[0].append(0)
            car1[1].append(element[0][1])
            car2[0].append(element[1][1])
            car2[1].append(0)


        print(car1[1][-1])
        print(car2[0][-1])

        plt.scatter(car1[0], car1[1], s=3)
        plt.scatter(car2[0], car2[1], s=3)
        plt.show()

        al = []
        for action in action_list[j]:
            al.append(action.action)

        print(al)