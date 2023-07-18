import math
import numpy as np
import pickle
import matplotlib.pyplot as plt

top_k = 50


##################################
# OVERLAY ALL PATHS 
##################################

for i in range(top_k):
    loaded_data = pickle.load(open( 't2_no_discount/pickles/data'+str(i)+'.pkl', "rb" ))
    car_x = loaded_data[2]
    car_y = loaded_data[3]
    ped1_x = loaded_data[4]
    ped1_y = loaded_data[5]
    ped2_x = loaded_data[6]
    ped2_y = loaded_data[7]
    ped3_x = loaded_data[8]
    ped3_y = loaded_data[9]
    plt.plot(car_x,car_y, color='black')
    plt.plot(ped1_x,ped1_y,color='blue')
    plt.plot(ped2_x,ped2_y,color='orange')
    plt.plot(ped3_x,ped3_y,color='red')
    plt.ylim(-12, 15)
    plt.xlim(-20, 15)
    plt.tick_params(labeltop=True, labelright=True)
    plt.grid(True)
    plt.legend(["Car", "Pedestrian 1", "Pedestrian 2", "Pedestrian 3"], loc='upper left')
    plt.title("Discount Factor = 0", y=1.08)

plt.savefig('graphs/t2_no_discount/all_traj_overlay.png')
plt.clf()

for i in range(top_k):
    loaded_data = pickle.load(open( 't2_w_discount/traj_100_state_0/pickles/data'+str(i)+'.pkl', "rb" ))
    car_x = loaded_data[1]
    car_y = loaded_data[2]
    ped1_x = loaded_data[3]
    ped1_y = loaded_data[4]
    ped2_x = loaded_data[5]
    ped2_y = loaded_data[6]
    ped3_x = loaded_data[7]
    ped3_y = loaded_data[8]
    plt.plot(car_x,car_y, color='black')
    plt.plot(ped1_x,ped1_y,color='blue')
    plt.plot(ped2_x,ped2_y,color='orange')
    plt.plot(ped3_x,ped3_y,color='red')
    plt.ylim(-12, 15)
    plt.xlim(-20, 15)
    plt.tick_params(labeltop=True, labelright=True)
    plt.grid(True)
    plt.legend(["Car", "Pedestrian 1", "Pedestrian 2", "Pedestrian 3"], loc='upper left')
    plt.title("Discount Factor = 1.00", y=1.08)
    #plt.savefig('graphs/t1_no_discount/'+str(i)+'.png')
plt.savefig('graphs/t2_w_discount/traj_100/all_traj_overlay.png')
plt.clf()




##################################
# OVERLAY WITH FADE 
##################################

for i in range(top_k):
    loaded_data = pickle.load(open( 't2_no_discount/pickles/data'+str(i)+'.pkl', "rb" ))
    car_x = loaded_data[2]
    car_y = loaded_data[3]
    ped1_x = loaded_data[4]
    ped1_y = loaded_data[5]
    ped2_x = loaded_data[6]
    ped2_y = loaded_data[7]
    ped3_x = loaded_data[8]
    ped3_y = loaded_data[9]

    plt.plot(car_x,car_y, color='black')

    ped_1_dist = ((ped1_x[len(ped1_x)-1]-car_x[len(car_x)-1])**2 + (ped1_y[len(ped1_y)-1]-car_y[len(car_y)-1])**2)**0.5
    ped_2_dist = ((ped2_x[len(ped2_x)-1]-car_x[len(car_x)-1])**2 + (ped2_y[len(ped2_y)-1]-car_y[len(car_y)-1])**2)**0.5
    ped_3_dist = ((ped3_x[len(ped3_x)-1]-car_x[len(car_x)-1])**2 + (ped3_y[len(ped3_y)-1]-car_y[len(car_y)-1])**2)**0.5

    if ped_1_dist <= 0.5:
        if ped1_x[len(ped1_x)-1]<2.5 and ped1_x[len(ped1_x)-1]>-1 and ped1_y[len(ped1_y)-1]<1 and ped1_y[len(ped1_y)-1]>-1:
            plt.plot(ped1_x,ped1_y,color='green',alpha=0.8)
        else:
            plt.plot(ped1_x,ped1_y,color='red',alpha=0.3)
    else:
        plt.plot(ped1_x,ped1_y,color='grey',alpha=0.3)

    if ped_2_dist <= 0.5:
        if ped2_x[len(ped2_x)-1]<2.5 and ped2_x[len(ped2_x)-1]>-1 and ped2_y[len(ped2_y)-1]<1 and ped2_y[len(ped2_y)-1]>-1:
            plt.plot(ped2_x,ped2_y,color='green',alpha=0.8)
        else:
            plt.plot(ped2_x,ped2_y,color='red',alpha=0.3)
    else:
        plt.plot(ped2_x,ped2_y,color='grey',alpha=0.3)

    if ped_3_dist <= 0.5:
        if ped3_x[len(ped3_x)-1]<2.5 and ped3_x[len(ped3_x)-1]>-1 and ped3_y[len(ped3_y)-1]<1 and ped3_y[len(ped3_y)-1]>-1:
            plt.plot(ped3_x,ped3_y,color='green',alpha=0.8)
        else:
            plt.plot(ped3_x,ped3_y,color='red',alpha=0.3)
    else:
        plt.plot(ped3_x,ped3_y,color='grey',alpha=0.3)

    plt.ylim(-6, 6)
    plt.xlim(-10, 6)
    plt.tick_params(labeltop=True, labelright=True)
    plt.grid(True)



plt.title("Discount Factor = 0", y=1.08)

plt.savefig('graphs/t2_no_discount/overlay_w_fade.png')
plt.clf()







for i in range(top_k):
    loaded_data = pickle.load(open( 't2_w_discount/traj_100_state_0/pickles/data'+str(i)+'.pkl', "rb" ))
    car_x = loaded_data[1]
    car_y = loaded_data[2]
    ped1_x = loaded_data[3]
    ped1_y = loaded_data[4]
    ped2_x = loaded_data[5]
    ped2_y = loaded_data[6]
    ped3_x = loaded_data[7]
    ped3_y = loaded_data[8]

    plt.plot(car_x,car_y, color='black')

    ped_1_dist = ((ped1_x[len(ped1_x)-1]-car_x[len(car_x)-1])**2 + (ped1_y[len(ped1_y)-1]-car_y[len(car_y)-1])**2)**0.5
    ped_2_dist = ((ped2_x[len(ped2_x)-1]-car_x[len(car_x)-1])**2 + (ped2_y[len(ped2_y)-1]-car_y[len(car_y)-1])**2)**0.5
    ped_3_dist = ((ped3_x[len(ped3_x)-1]-car_x[len(car_x)-1])**2 + (ped3_y[len(ped3_y)-1]-car_y[len(car_y)-1])**2)**0.5

    if ped_1_dist <= 0.5:
        if ped1_x[len(ped1_x)-1]<2.5 and ped1_x[len(ped1_x)-1]>-1.5 and ped1_y[len(ped1_y)-1]<2.5 and ped1_y[len(ped1_y)-1]>-2.5:
            plt.plot(ped1_x,ped1_y,color='green')
        else:
            plt.plot(ped1_x,ped1_y,color='red',alpha=0.5)
    else:
        plt.plot(ped1_x,ped1_y,color='grey',alpha=0.3)

    if ped_2_dist <= 0.5:
        if ped2_x[len(ped2_x)-1]<2.5 and ped2_x[len(ped2_x)-1]>-1.5 and ped2_y[len(ped2_y)-1]<2.5 and ped2_y[len(ped2_y)-1]>-2.5:
            plt.plot(ped2_x,ped2_y,color='green')
        else:
            plt.plot(ped2_x,ped2_y,color='red',alpha=0.5)
    else:
        plt.plot(ped2_x,ped2_y,color='grey',alpha=0.3)

    if ped_3_dist <= 0.5:
        if ped3_x[len(ped3_x)-1]<2.5 and ped3_x[len(ped3_x)-1]>-1.5 and ped3_y[len(ped3_y)-1]<2.5 and ped3_y[len(ped3_y)-1]>-2.5:
            plt.plot(ped3_x,ped3_y,color='green')
        else:
            plt.plot(ped3_x,ped3_y,color='red',alpha=0.5)
    else:
        plt.plot(ped3_x,ped3_y,color='grey',alpha=0.3)

    plt.ylim(-6, 6)
    plt.xlim(-10, 6)
    plt.tick_params(labeltop=True, labelright=True)
    plt.grid(True)


for i in range(top_k):
    loaded_data = pickle.load(open( 't2_w_discount/traj_100_state_0/pickles/data'+str(i)+'.pkl', "rb" ))
    car_x = loaded_data[1]
    car_y = loaded_data[2]
    ped1_x = loaded_data[3]
    ped1_y = loaded_data[4]
    ped2_x = loaded_data[5]
    ped2_y = loaded_data[6]
    ped3_x = loaded_data[7]
    ped3_y = loaded_data[8]

    ped_1_dist = ((ped1_x[len(ped1_x)-1]-car_x[len(car_x)-1])**2 + (ped1_y[len(ped1_y)-1]-car_y[len(car_y)-1])**2)**0.5
    ped_2_dist = ((ped2_x[len(ped2_x)-1]-car_x[len(car_x)-1])**2 + (ped2_y[len(ped2_y)-1]-car_y[len(car_y)-1])**2)**0.5
    ped_3_dist = ((ped3_x[len(ped3_x)-1]-car_x[len(car_x)-1])**2 + (ped3_y[len(ped3_y)-1]-car_y[len(car_y)-1])**2)**0.5

    if ped_1_dist <= 0.5:
        if ped1_x[len(ped1_x)-1]<2.5 and ped1_x[len(ped1_x)-1]>-1.5 and ped1_y[len(ped1_y)-1]<2.5 and ped1_y[len(ped1_y)-1]>-2.5:
            plt.plot(ped1_x,ped1_y,color='green')

    if ped_2_dist <= 0.5:
        if ped2_x[len(ped2_x)-1]<2.5 and ped2_x[len(ped2_x)-1]>-1.5 and ped2_y[len(ped2_y)-1]<2.5 and ped2_y[len(ped2_y)-1]>-2.5:
            plt.plot(ped2_x,ped2_y,color='green')

    if ped_3_dist <= 0.5:
        if ped3_x[len(ped3_x)-1]<2.5 and ped3_x[len(ped3_x)-1]>-1.5 and ped3_y[len(ped3_y)-1]<2.5 and ped3_y[len(ped3_y)-1]>-2.5:
            plt.plot(ped3_x,ped3_y,color='green')




plt.title("Discount Factor = 1.00", y=1.08)

plt.savefig('graphs/t2_w_discount/traj_100/overlay_w_fade.png')
plt.clf()


