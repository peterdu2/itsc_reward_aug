import math
import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import csv

plt.rcParams["font.family"] = "Times New Roman"

top_k = 25
for i in range(top_k):
    loaded_data = pickle.load(open( 't1_no_discount/pickles/data'+str(i)+'.pkl', "rb" ))
    car_x = loaded_data[2]
    car_y = loaded_data[3]
    car2_x = loaded_data[4]
    car2_y = loaded_data[5]
    ped1_x = loaded_data[6]
    ped1_y = loaded_data[7]
    ped2_x = loaded_data[8]
    ped2_y = loaded_data[9]
    car1_line = plt.plot(car_x,car_y, color='xkcd:lightblue',marker='.',alpha=0.35)
    car2_line = plt.plot(car2_x,car2_y, color='xkcd:darkblue',marker='.',alpha=0.35)

    dist = (car_x[len(car_x)-1]-car2_x[len(car2_x)-1])
    #print(dist)

    if (car_x[len(car_x)-1]-car2_x[len(car2_x)-1]) < 2**0.5:
        #print(car_x[len(car_x)-1])
        plt.plot(0.5*(car_x[len(car_x)-1]+car2_x[len(car2_x)-1]),car_y[len(car_x)-1], marker='x', markersize=18, color='red', mew=3, ms=10, linestyle = 'None')


    ped_1_dist = ((ped1_x[len(ped1_x)-1]-car_x[len(car_x)-1])**2 + (ped1_y[len(ped1_y)-1]-car_y[len(car_y)-1])**2)**0.5
    ped_2_dist = ((ped2_x[len(ped2_x)-1]-car_x[len(car_x)-1])**2 + (ped2_y[len(ped2_y)-1]-car_y[len(car_y)-1])**2)**0.5

    if ped_1_dist <= 2**0.5:
        if ped1_x[len(ped1_x)-1]<2.5 and ped1_x[len(ped1_x)-1]>-1 and ped1_y[len(ped1_y)-1]<1 and ped1_y[len(ped1_y)-1]>-1:
            plt.plot(ped1_x,ped1_y,color='magenta')
        else:
            plt.plot(ped1_x,ped1_y,color='orange', alpha=0.5)
    else:
       grey= plt.plot(ped1_x,ped1_y,color='grey', alpha=0.30)

    if ped_2_dist <= 2**0.5:
        if ped2_x[len(ped2_x)-1]<2.5 and ped2_x[len(ped2_x)-1]>-1 and ped2_y[len(ped2_y)-1]<1 and ped2_y[len(ped2_y)-1]>-1:
            plt.plot(ped2_x,ped2_y,color='magenta')
        else:
            ped2_orangered=plt.plot(ped2_x,ped2_y,color='xkcd:orangered', alpha=0.3)
    else:
       grey = plt.plot(ped2_x,ped2_y,color='grey', alpha=0.30)


    plt.ylim(-4, 6)
    plt.xlim(-12.5, 5)
    plt.tick_params(labeltop=False, labelright=False, labelsize=11)
    plt.grid(True, color='black')
    plt.grid(linestyle='dotted')
    plt.ylabel("Lateral Position (m)")
    plt.xlabel("Longitudinal Position (m)")
    ax = plt.gca()
    ax.set_xticks([-12.5,-8,-3.5,1,5.5])
    ax.tick_params(direction='in')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

leg = plt.legend([car1_line[0], car2_line[0], ped2_orangered[0], grey[0]], ['Lead Car', 'Following Car','Pedestrian2 Failure (Ped2. Induced)', 'No Failure'], loc="upper left", prop={'size': 9})
for lh in leg.legendHandles: 
    lh._legmarker.set_alpha(1)
leg.get_frame().set_linewidth(1.5)
leg.get_frame().set_edgecolor('black')




plt.title("Vehicle and Pedestrian Trajectories (Generic Reward)", y=1.01, fontsize=12)

plt.savefig('graphs/P_generic_reward.png', dpi=600)
plt.clf()


for i in range(top_k):
    loaded_data = pickle.load(open( 't1_w_discount/pickles/data'+str(i)+'.pkl', "rb" ))
    car_x = loaded_data[2]
    car_y = loaded_data[3]
    car2_x = loaded_data[4]
    car2_y = loaded_data[5]
    ped1_x = loaded_data[6]
    ped1_y = loaded_data[7]
    ped2_x = loaded_data[8]
    ped2_y = loaded_data[9]
    car1_line = plt.plot(car_x,car_y, color='xkcd:lightblue',marker='.',alpha=0.35)
    car2_line = plt.plot(car2_x,car2_y, color='xkcd:darkblue',marker='.',alpha=0.35)

    dist = (car_x[len(car_x)-1]-car2_x[len(car2_x)-1])
    #print(dist)

    if (car_x[len(car_x)-1]-car2_x[len(car2_x)-1]) < 2**0.5:
        car_red = plt.plot(0.5*(car_x[len(car_x)-1]+car2_x[len(car2_x)-1]),car_y[len(car_x)-1], marker='x', markersize=12, color='xkcd:red', mew=2, ms=10, linestyle = 'None')


    ped_1_dist = ((ped1_x[len(ped1_x)-1]-car_x[len(car_x)-1])**2 + (ped1_y[len(ped1_y)-1]-car_y[len(car_y)-1])**2)**0.5
    ped_2_dist = ((ped2_x[len(ped2_x)-1]-car_x[len(car_x)-1])**2 + (ped2_y[len(ped2_y)-1]-car_y[len(car_y)-1])**2)**0.5

    if ped_1_dist <= 2**0.5:
        if ped1_x[len(ped1_x)-1]<2.5 and ped1_x[len(ped1_x)-1]>-1 and ped1_y[len(ped1_y)-1]<1 and ped1_y[len(ped1_y)-1]>-1:
            ped1_green = plt.plot(ped1_x,ped1_y,color='xkcd:green')
        else:
             ped1_purple = plt.plot(ped1_x,ped1_y,color='xkcd:purple', alpha=0.5)
    else:
        ped1_grey = plt.plot(ped1_x,ped1_y,color='grey', alpha=0.30)

    if ped_2_dist <= 2**0.5:
        if ped2_x[len(ped2_x)-1]<2.5 and ped2_x[len(ped2_x)-1]>-1 and ped2_y[len(ped2_y)-1]<1 and ped2_y[len(ped2_y)-1]>-1:
            ped2_green=plt.plot(ped2_x,ped2_y,color='xkcd:green')
            #print(i)
        else:
            ped2_orangered = plt.plot(ped2_x,ped2_y,color='xkcd:orangered' , alpha=0.5)
    else:
        grey=plt.plot(ped2_x,ped2_y,color='grey', alpha=0.30)


    plt.ylim(-4, 6)
    plt.xlim(-12.5, 5)
    plt.tick_params(labeltop=False, labelright=False, labelsize=11)
    plt.grid(True, color='black')
    plt.grid(linestyle='dotted')
    plt.ylabel("Lateral Position (m)")
    plt.xlabel("Longitudinal Position (m)")
    ax = plt.gca()
    ax.set_xticks([-12.5,-8,-3.5,1,5.5])
    ax.tick_params(direction='in')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

leg = plt.legend([car1_line[0], car2_line[0], ped1_purple[0], ped2_orangered[0], ped2_green[0], car_red[0], grey[0]], ['Lead Car', 'Following Car', 'Pedestrian1 Failure (Ped1. Induced)', 'Pedestrian2 Failure (Ped2. Induced)', 'Pedestrian2 Failure (Car Induced)', 'Car/Car Failure', 'No Failure'],  prop={'size': 9})
for lh in leg.legendHandles: 
    lh._legmarker.set_alpha(1)
leg.get_frame().set_linewidth(1.5)
leg.get_frame().set_edgecolor('black')



plt.title("Vehicle and Pedestrian Trajectories (TD Reward)", y=1.01, fontsize=12)

plt.savefig('graphs/P_td_reward.png', dpi=600)
plt.clf()





##################################
# OVERLAY WITH FADE 
##################################

for i in range(10,11):
    loaded_data = pickle.load(open( 't1_no_discount/pickles/data'+str(i)+'.pkl', "rb" ))
    car_x = loaded_data[2]
    car_y = loaded_data[3]
    car2_x = loaded_data[4]
    car2_y = loaded_data[5]
    ped1_x = loaded_data[6]
    ped1_y = loaded_data[7]
    ped2_x = loaded_data[8]
    ped2_y = loaded_data[9]
    ped1_x = np.delete(ped1_x, np.arange(0, len(ped1_x), 2))
    ped1_y = np.delete(ped1_y, np.arange(0, len(ped1_y), 2))
    ped2_x = np.delete(ped2_x, np.arange(0, len(ped2_x), 2))
    ped2_y = np.delete(ped2_y, np.arange(0, len(ped2_y), 2))
    plt.plot(car_x,car_y, color='blue', linewidth=3)
    plt.plot(car2_x,car2_y, color='green', linewidth=3)

    currentAxis = plt.gca()
    currentAxis.add_patch(Rectangle((car_x[len(car_x)-1] - .5, car_y[len(car_y)-1] - .5), 1, 1, facecolor='black', fill=False))
    currentAxis.set_aspect(0.90)
    dist = (car_x[len(car_x)-1]-car2_x[len(car2_x)-1])
    #print(dist)



    if (car_x[len(car_x)-1]-car2_x[len(car2_x)-1]) < 2**0.5:
        #print(car_x[len(car_x)-1])
        plt.plot(0.5*(car_x[len(car_x)-1]+car2_x[len(car2_x)-1]),car_y[len(car_x)-1], marker='x', markersize=18, color='red', mew=3, ms=10)


    ped_1_dist = ((ped1_x[len(ped1_x)-1]-car_x[len(car_x)-1])**2 + (ped1_y[len(ped1_y)-1]-car_y[len(car_y)-1])**2)**0.5
    ped_2_dist = ((ped2_x[len(ped2_x)-1]-car_x[len(car_x)-1])**2 + (ped2_y[len(ped2_y)-1]-car_y[len(car_y)-1])**2)**0.5

    if ped_1_dist <= 2**0.5:
        if ped1_x[len(ped1_x)-1]<2.5 and ped1_x[len(ped1_x)-1]>-1 and ped1_y[len(ped1_y)-1]<1 and ped1_y[len(ped1_y)-1]>-1:
            plt.plot(ped1_x,ped1_y,color='cyan', marker='x')
        else:
            plt.plot(ped1_x,ped1_y,color='orange', marker='x')
    else:
        plt.plot(ped1_x,ped1_y,color='grey', marker='x')

    if ped_2_dist <= 2**0.5:
        if ped2_x[len(ped2_x)-1]<2.5 and ped2_x[len(ped2_x)-1]>-1 and ped2_y[len(ped2_y)-1]<1 and ped2_y[len(ped2_y)-1]>-1:
            plt.plot(ped2_x,ped2_y,color='cyan',marker='.')
        else:
            plt.plot(ped2_x,ped2_y,color='orange', marker='.')
    else:
        plt.plot(ped2_x,ped2_y,color='grey', marker='.')


    plt.ylim(-3.5, 3.5)
    plt.xlim(-12.5, 3)
    plt.xlabel('Longitudinal Position (m)', fontsize=15)
    plt.ylabel('Lateral Position (m)', fontsize=15)
    plt.legend(["Car1", "Car2", "Ped1", "Ped2"], loc='upper left')
    #ax.set_aspect(0.75)
    plt.tick_params(labeltop=True, labelright=True, labelsize=15)
    plt.grid(True)



plt.title("Vehicle and Pedestrian Response", y=1.20, fontsize=16)

# CSV DUMP (FOR ANTHONY)
with open('no_discount_single'+str(i)+'.csv', 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(car_x)
     wr.writerow(car_y)
     wr.writerow(car2_x)
     wr.writerow(car2_y)
     wr.writerow(ped1_x)
     wr.writerow(ped1_y)
     wr.writerow(ped2_x)
     wr.writerow(ped2_y)

print(len(ped1_x))
print(len(car_x))


plt.savefig('graphs/no_discount'+str(i)+'.png', dpi=600)
plt.clf()


#Using IDX 2,3,11

for i in range(11,12):
    loaded_data = pickle.load(open( 't1_w_discount/pickles/data'+str(i)+'.pkl', "rb" ))
    car_x = loaded_data[2]
    car_y = loaded_data[3]
    car2_x = loaded_data[4]
    car2_y = loaded_data[5]
    ped1_x = loaded_data[6]
    ped1_y = loaded_data[7]
    ped2_x = loaded_data[8]
    ped2_y = loaded_data[9]
    ped1_x = np.delete(ped1_x, np.arange(0, len(ped1_x), 2))
    ped1_y = np.delete(ped1_y, np.arange(0, len(ped1_y), 2))
    ped2_x = np.delete(ped2_x, np.arange(0, len(ped2_x), 8))
    ped2_y = np.delete(ped2_y, np.arange(0, len(ped2_y), 8))
    plt.plot(car_x,car_y, color='blue', linewidth=3)
    plt.plot(car2_x,car2_y, color='green', linewidth=3)

    currentAxis = plt.gca()
    currentAxis.add_patch(Rectangle((car_x[len(car_x)-1] - .5, car_y[len(car_y)-1] - .5), 1, 1, facecolor='black', fill=False))
    currentAxis.set_aspect(0.90)
    dist = (car_x[len(car_x)-1]-car2_x[len(car2_x)-1])
    #print(dist)



    ped_1_dist = ((ped1_x[len(ped1_x)-1]-car_x[len(car_x)-1])**2 + (ped1_y[len(ped1_y)-1]-car_y[len(car_y)-1])**2)**0.5
    ped_2_dist = ((ped2_x[len(ped2_x)-1]-car_x[len(car_x)-1])**2 + (ped2_y[len(ped2_y)-1]-car_y[len(car_y)-1])**2)**0.5

    if ped_1_dist <= 2**0.5:
        if ped1_x[len(ped1_x)-1]<2.5 and ped1_x[len(ped1_x)-1]>-1 and ped1_y[len(ped1_y)-1]<1 and ped1_y[len(ped1_y)-1]>-1:
            plt.plot(ped1_x,ped1_y,color='orange', marker='x')
        else:
            plt.plot(ped1_x,ped1_y,color='orange', marker='x')
    else:
        plt.plot(ped1_x,ped1_y,color='grey', marker='x')

    if ped_2_dist <= 2**0.5:
        if ped2_x[len(ped2_x)-1]<2.5 and ped2_x[len(ped2_x)-1]>-1 and ped2_y[len(ped2_y)-1]<1 and ped2_y[len(ped2_y)-1]>-1:
            plt.plot(ped2_x,ped2_y,color='orange',marker='.')
        else:
            plt.plot(ped2_x,ped2_y,color='orange', marker='.')
    else:
        plt.plot(ped2_x,ped2_y,color='grey', marker='.')

    if (car_x[len(car_x)-1]-car2_x[len(car2_x)-1]) < 0.5**0.5:
        print(car_x[len(car_x)-1])
        plt.plot(car2_x[len(car2_x)-1],car_y[len(car_x)-1], marker='x', markersize=18, color='red', mew=3, ms=10)


    plt.ylim(-3.5, 3.5)
    plt.xlim(-12.5, 3)
    plt.xlabel('Longitudinal Position (m)', fontsize=15)
    plt.ylabel('Lateral Position (m)', fontsize=15)
    plt.legend(["Car1", "Car2", "Ped1", "Ped2"], loc='upper left')
    #ax.set_aspect(0.75)
    plt.tick_params(labeltop=True, labelright=True, labelsize=15)
    plt.grid(True)



plt.title("Vehicle and Pedestrian Response (TD)", y=1.20, fontsize=16)

# CSV DUMP (FOR ANTHONY)
with open('w_discount_single'+str(i)+'.csv', 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(car_x)
     wr.writerow(car_y)
     wr.writerow(car2_x)
     wr.writerow(car2_y)
     wr.writerow(ped1_x)
     wr.writerow(ped1_y)
     wr.writerow(ped2_x)
     wr.writerow(ped2_y)

print(len(ped1_x))
print(len(car_x))

plt.savefig('graphs/w_discount'+str(i)+'.png', dpi=600)
plt.clf()



'''


for i in range(top_k):
    loaded_data = pickle.load(open( 't1_w_discount/traj_100_state_0/pickles/data'+str(i)+'.pkl', "rb" ))
    car_x = loaded_data[1]
    car_y = loaded_data[2]
    ped1_x = loaded_data[3]
    ped1_y = loaded_data[4]
    ped2_x = loaded_data[5]
    ped2_y = loaded_data[6]

    plt.plot(car_x,car_y, color='black')

    ped_1_dist = ((ped1_x[len(ped1_x)-1]-car_x[len(car_x)-1])**2 + (ped1_y[len(ped1_y)-1]-car_y[len(car_y)-1])**2)**0.5
    ped_2_dist = ((ped2_x[len(ped2_x)-1]-car_x[len(car_x)-1])**2 + (ped2_y[len(ped2_y)-1]-car_y[len(car_y)-1])**2)**0.5

    if ped_1_dist <= 2**0.5:
        if ped1_x[len(ped1_x)-1]<2.5 and ped1_x[len(ped1_x)-1]>-1.5 and ped1_y[len(ped1_y)-1]<2.5 and ped1_y[len(ped1_y)-1]>-2.5:
            plt.plot(ped1_x,ped1_y,color='cyan',alpha=0.5)
        else:
            plt.plot(ped1_x,ped1_y,color='orange')
    else:
        plt.plot(ped1_x,ped1_y,color='grey',alpha=0.8)

    if ped_2_dist <= 2**0.5:
        if ped2_x[len(ped2_x)-1]<2.5 and ped2_x[len(ped2_x)-1]>-1.5 and ped2_y[len(ped2_y)-1]<2.5 and ped2_y[len(ped2_y)-1]>-2.5:
            plt.plot(ped2_x,ped2_y,color='cyan',alpha=0.5)
        else:
            plt.plot(ped2_x,ped2_y,color='orange')
    else:
        plt.plot(ped2_x,ped2_y,color='grey',alpha=0.8)

    plt.ylim(-5, 5)
    plt.xlim(-10, 7)
    plt.tick_params(labeltop=True, labelright=True, labelsize=15)
    plt.grid(True)


for i in range(top_k):
    loaded_data = pickle.load(open( 't1_w_discount/traj_100_state_0/pickles/data'+str(i)+'.pkl', "rb" ))
    car_x = loaded_data[1]
    car_y = loaded_data[2]
    ped1_x = loaded_data[3]
    ped1_y = loaded_data[4]
    ped2_x = loaded_data[5]
    ped2_y = loaded_data[6]

    ped_1_dist = ((ped1_x[len(ped1_x)-1]-car_x[len(car_x)-1])**2 + (ped1_y[len(ped1_y)-1]-car_y[len(car_y)-1])**2)**0.5
    ped_2_dist = ((ped2_x[len(ped2_x)-1]-car_x[len(car_x)-1])**2 + (ped2_y[len(ped2_y)-1]-car_y[len(car_y)-1])**2)**0.5

    if ped_1_dist <= 2**0.5:
        if ped1_x[len(ped1_x)-1]<2.5 and ped1_x[len(ped1_x)-1]>-1.5 and ped1_y[len(ped1_y)-1]<2.5 and ped1_y[len(ped1_y)-1]>-2.5:
            plt.plot(ped1_x,ped1_y,color='cyan',alpha=0.5)

    if ped_2_dist <= 2**0.5:
        if ped2_x[len(ped2_x)-1]<2.5 and ped2_x[len(ped2_x)-1]>-1.5 and ped2_y[len(ped2_y)-1]<2.5 and ped2_y[len(ped2_y)-1]>-2.5:
            plt.plot(ped2_x,ped2_y,color='cyan',alpha=0.5)




plt.title("AST w/ Reward Augmentation (Two Peds)", y=1.08, fontsize=18)

plt.savefig('graphs/t1_w_discount/traj_100/augmented_double.png')
plt.clf()
'''