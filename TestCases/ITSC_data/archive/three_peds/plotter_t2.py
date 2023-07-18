import math
import numpy as np
import pickle
import matplotlib.pyplot as plt

top_k = 50

xmax = -999999
xmin = 999999
ymax = -999999
ymin = 999999
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

    if max(max(car_x), max(ped1_x), max(ped2_x), max(ped3_x)) > xmax:
        xmax = max(max(car_x), max(ped1_x), max(ped2_x), max(ped3_x))

    if min(min(car_x), min(ped1_x), min(ped2_x), min(ped3_x)) < xmin:
        xmin = min(min(car_x), min(ped1_x), min(ped2_x), min(ped3_x))

    if max(max(car_y), max(ped1_y), max(ped2_y), max(ped3_y)) > ymax:
        ymax = max(max(car_y), max(ped1_y), max(ped2_y), max(ped3_y)) 

    if min(min(car_y), min(ped1_y), min(ped2_y), min(ped3_y)) < ymin:
        ymin = min(min(car_y), min(ped1_y), min(ped2_y), min(ped3_y))

print(xmax, ymax, xmin, ymin)
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
    plt.scatter(car_x,car_y, s=50, marker="x")
    plt.scatter(ped1_x,ped1_y, s=50, marker="x")
    plt.scatter(ped2_x,ped2_y, s=50, marker="x")
    plt.scatter(ped3_x,ped3_y, s=50, marker="x")
    plt.plot(car_x,car_y)
    plt.plot(ped1_x,ped1_y)
    plt.plot(ped2_x,ped2_y)
    plt.plot(ped3_x,ped3_y)
    plt.ylim(ymin-0.5, ymax+0.5)
    plt.xlim(xmin-0.5, xmax+0.5)
    plt.tick_params(labeltop=True, labelright=True)
    plt.grid(True)
    plt.legend(["Car", "Pedestrian 1", "Pedestrian 2", "Pedstrian 3"], loc='upper left')
    plt.title("Discount Factor = 0", y=1.08)
    plt.savefig('graphs/t2_no_discount/'+str(i)+'.png')
    plt.clf()











xmax = -999999
xmin = 999999
ymax = -999999
ymin = 999999
for i in range(top_k):
    loaded_data = pickle.load(open('t2_w_discount/traj_050_state_0/pickles/data'+str(i)+'.pkl', "rb" ))
    car_x = loaded_data[1]
    car_y = loaded_data[2]
    ped1_x = loaded_data[3]
    ped1_y = loaded_data[4]
    ped2_x = loaded_data[5]
    ped2_y = loaded_data[6]
    ped3_x = loaded_data[7]
    ped3_y = loaded_data[8]

    if max(max(car_x), max(ped1_x), max(ped2_x), max(ped3_x)) > xmax:
        xmax = max(max(car_x), max(ped1_x), max(ped2_x), max(ped3_x))

    if min(min(car_x), min(ped1_x), min(ped2_x), min(ped3_x)) < xmin:
        xmin = min(min(car_x), min(ped1_x), min(ped2_x), min(ped3_x))

    if max(max(car_y), max(ped1_y), max(ped2_y), max(ped3_y)) > ymax:
        ymax = max(max(car_y), max(ped1_y), max(ped2_y), max(ped3_y)) 

    if min(min(car_y), min(ped1_y), min(ped2_y), min(ped3_y)) < ymin:
        ymin = min(min(car_y), min(ped1_y), min(ped2_y), min(ped3_y))

for i in range(top_k):
    loaded_data = pickle.load(open( 't2_w_discount/traj_050_state_0/pickles/data'+str(i)+'.pkl', "rb" ))
    car_x = loaded_data[1]
    car_y = loaded_data[2]
    ped1_x = loaded_data[3]
    ped1_y = loaded_data[4]
    ped2_x = loaded_data[5]
    ped2_y = loaded_data[6]
    ped3_x = loaded_data[7]
    ped3_y = loaded_data[8]
    plt.scatter(car_x,car_y, s=50, marker="x")
    plt.scatter(ped1_x,ped1_y, s=50, marker="x")
    plt.scatter(ped2_x,ped2_y, s=50, marker="x")
    plt.scatter(ped3_x,ped3_y, s=50, marker="x")
    plt.plot(car_x,car_y)
    plt.plot(ped1_x,ped1_y)
    plt.plot(ped2_x,ped2_y)
    plt.plot(ped3_x,ped3_y)
    plt.ylim(ymin-0.5, ymax+0.5)
    plt.xlim(xmin-0.5, xmax+0.5)
    plt.tick_params(labeltop=True, labelright=True)
    plt.grid(True)
    plt.legend(["Car", "Pedestrian 1", "Pedestrian 2", "Pedstrian 3"], loc='upper left')
    plt.title("Discount Factor = 0", y=1.08)
    plt.savefig('graphs/t2_w_discount/traj_050/'+str(i)+'.png')
    plt.clf()









xmax = -999999
xmin = 999999
ymax = -999999
ymin = 999999
for i in range(top_k):
    loaded_data = pickle.load(open('t2_w_discount/traj_100_state_0/pickles/data'+str(i)+'.pkl', "rb" ))
    car_x = loaded_data[1]
    car_y = loaded_data[2]
    ped1_x = loaded_data[3]
    ped1_y = loaded_data[4]
    ped2_x = loaded_data[5]
    ped2_y = loaded_data[6]
    ped3_x = loaded_data[7]
    ped3_y = loaded_data[8]


    if max(max(car_x), max(ped1_x), max(ped2_x), max(ped3_x)) > xmax:
        xmax = max(max(car_x), max(ped1_x), max(ped2_x), max(ped3_x))

    if min(min(car_x), min(ped1_x), min(ped2_x), min(ped3_x)) < xmin:
        xmin = min(min(car_x), min(ped1_x), min(ped2_x), min(ped3_x))

    if max(max(car_y), max(ped1_y), max(ped2_y), max(ped3_y)) > ymax:
        ymax = max(max(car_y), max(ped1_y), max(ped2_y), max(ped3_y)) 

    if min(min(car_y), min(ped1_y), min(ped2_y), min(ped3_y)) < ymin:
        ymin = min(min(car_y), min(ped1_y), min(ped2_y), min(ped3_y))

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
    plt.scatter(car_x,car_y, s=50, marker="x")
    plt.scatter(ped1_x,ped1_y, s=50, marker="x")
    plt.scatter(ped2_x,ped2_y, s=50, marker="x")
    plt.scatter(ped3_x,ped3_y, s=50, marker="x")
    plt.plot(car_x,car_y)
    plt.plot(ped1_x,ped1_y)
    plt.plot(ped2_x,ped2_y)
    plt.plot(ped3_x,ped3_y)
    plt.ylim(ymin-0.5, ymax+0.5)
    plt.xlim(xmin-0.5, xmax+0.5)
    plt.tick_params(labeltop=True, labelright=True)
    plt.grid(True)
    plt.legend(["Car", "Pedestrian 1", "Pedestrian 2", "Pedstrian 3"], loc='upper left')
    plt.title("Discount Factor = 0", y=1.08)
    plt.savefig('graphs/t2_w_discount/traj_100/'+str(i)+'.png')
    plt.clf()










xmax = -999999
xmin = 999999
ymax = -999999
ymin = 999999
for i in range(top_k):
    loaded_data = pickle.load(open('t2_w_discount/traj_150_state_0/pickles/data'+str(i)+'.pkl', "rb" ))
    car_x = loaded_data[1]
    car_y = loaded_data[2]
    ped1_x = loaded_data[3]
    ped1_y = loaded_data[4]
    ped2_x = loaded_data[5]
    ped2_y = loaded_data[6]
    ped3_x = loaded_data[7]
    ped3_y = loaded_data[8]

    if max(max(car_x), max(ped1_x), max(ped2_x), max(ped3_x)) > xmax:
        xmax = max(max(car_x), max(ped1_x), max(ped2_x), max(ped3_x))

    if min(min(car_x), min(ped1_x), min(ped2_x), min(ped3_x)) < xmin:
        xmin = min(min(car_x), min(ped1_x), min(ped2_x), min(ped3_x))

    if max(max(car_y), max(ped1_y), max(ped2_y), max(ped3_y)) > ymax:
        ymax = max(max(car_y), max(ped1_y), max(ped2_y), max(ped3_y)) 

    if min(min(car_y), min(ped1_y), min(ped2_y), min(ped3_y)) < ymin:
        ymin = min(min(car_y), min(ped1_y), min(ped2_y), min(ped3_y))

for i in range(top_k):
    loaded_data = pickle.load(open( 't2_w_discount/traj_150_state_0/pickles/data'+str(i)+'.pkl', "rb" ))
    car_x = loaded_data[1]
    car_y = loaded_data[2]
    ped1_x = loaded_data[3]
    ped1_y = loaded_data[4]
    ped2_x = loaded_data[5]
    ped2_y = loaded_data[6]
    ped3_x = loaded_data[7]
    ped3_y = loaded_data[8]
    plt.scatter(car_x,car_y, s=50, marker="x")
    plt.scatter(ped1_x,ped1_y, s=50, marker="x")
    plt.scatter(ped2_x,ped2_y, s=50, marker="x")
    plt.scatter(ped3_x,ped3_y, s=50, marker="x")
    plt.plot(car_x,car_y)
    plt.plot(ped1_x,ped1_y)
    plt.plot(ped2_x,ped2_y)
    plt.plot(ped3_x,ped3_y)
    plt.ylim(ymin-0.5, ymax+0.5)
    plt.xlim(xmin-0.5, xmax+0.5)
    plt.tick_params(labeltop=True, labelright=True)
    plt.grid(True)
    plt.legend(["Car", "Pedestrian 1", "Pedestrian 2", "Pedstrian 3"], loc='upper left')
    plt.title("Discount Factor = 0", y=1.08)
    plt.savefig('graphs/t2_w_discount/traj_150/'+str(i)+'.png')
    plt.clf()



    
