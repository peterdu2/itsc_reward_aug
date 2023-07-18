import math
import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data
from matplotlib.patches import Rectangle
import csv
import os
import errno

from matplotlib.patches import Rectangle


def imscatter(x, y, image, ax=None, zoom=1):
    if ax is None:
        ax = plt.gca()
    try:
        image = plt.imread(image)
    except TypeError:
        pass
    im = OffsetImage(image, zoom=zoom)
    x, y = np.atleast_1d(x, y)
    artists = []
    for x0, y0 in zip(x, y):
        ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
        artists.append(ax.add_artist(ab))
    ax.update_datalim(np.column_stack([x, y]))
    ax.autoscale()
    return artists


top_k = 50
bg_ped_paths = []#[2,5,8,10]



for i in range(top_k):
    print(i)
    loaded_data = pickle.load(open( 't1_w_discount/pickles/data'+str(i)+'.pkl', "rb" ))
    car_x = loaded_data[2]
    car_y = loaded_data[3]
    car2_x = loaded_data[4]
    car2_y = loaded_data[5]
    ped1_x = loaded_data[6]
    ped1_y = loaded_data[7]
    ped2_x = loaded_data[8]
    ped2_y = loaded_data[9]

    car2_x = np.array(car2_x) - 6
    ped1_x = np.array(ped1_x) + 3.5
    ped2_x = np.array(ped2_x) + 3.5 
    
    for frame in range(len(car_x)):

        car1_image_path = get_sample_data('/home/peter/Research/AST_RevC/TestCases/ITSC_data/multi_car/two_peds/car1.png')
        car2_image_path = get_sample_data('/home/peter/Research/AST_RevC/TestCases/ITSC_data/multi_car/two_peds/car2.png')
        ped_image_path = get_sample_data('/home/peter/Research/AST_RevC/TestCases/ITSC_data/multi_car/two_peds/person.png')

        fig, ax = plt.subplots()

        currentAxis = plt.gca()
        currentAxis.add_patch(Rectangle((-50, -0.7), 100, 1.4, facecolor='grey', fill=True, alpha=0.7))
        currentAxis.add_patch(Rectangle((-50, 0.7), 100, 50, facecolor='green', fill=True, alpha=0.8))
        currentAxis.add_patch(Rectangle((-50, -20), 100, 19.3, facecolor='green', fill=True, alpha=0.8))

        car1_img_x = [car_x[frame:frame+1][0]]
        car1_img_y = [car_y[frame:frame+1][0]]
        car2_img_x = [car2_x[frame:frame+1][0]]
        car2_img_y = [car2_y[frame:frame+1][0]]
        peds_x = [ped1_x[frame:frame+1][0], ped2_x[frame:frame+1][0]]
        peds_y = [ped1_y[frame:frame+1][0], ped2_y[frame:frame+1][0]]

        imscatter(car1_img_x, car1_img_y, car1_image_path, zoom=0.45, ax=ax)
        imscatter(car2_img_x, car2_img_y, car2_image_path, zoom=0.45, ax=ax)
        imscatter(peds_x, peds_y, ped_image_path, zoom=0.50, ax=ax)
        #ax.scatter(cars_x, cars_y, s=1)

        plt.ylim(-4, 4)
        plt.xlim(-48, 7)

        plt.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

        plt.plot(car_x[:frame+1], car_y[:frame+1], color='xkcd:blue')
        plt.plot(car2_x[:frame+1], car2_y[:frame+1], color='xkcd:red')
        plt.plot(ped1_x[:frame+1], ped1_y[:frame+1], color='xkcd:purple')
        plt.plot(ped2_x[:frame+1], ped2_y[:frame+1], color='xkcd:orange')

        plt.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)


        #Plot background pedestrian paths
        for path_idx in bg_ped_paths:
            loaded_data = pickle.load(open( 't1_w_discount/pickles/data'+str(path_idx)+'.pkl', "rb" ))
            ped1_x = loaded_data[6]
            ped1_y = loaded_data[7]
            ped2_x = loaded_data[8]
            ped2_y = loaded_data[9]

            plt.plot(ped1_x[:frame+1], ped1_y[:frame+1], color='xkcd:grey', alpha=0.6)
            plt.plot(ped2_x[:frame+1], ped2_y[:frame+1], color='xkcd:grey', alpha=0.6)

        filepath = 'animation/T'+str(i)+'/'+str(frame)+'.jpeg'
        if not os.path.exists(os.path.dirname(filepath)):
            try:
                os.makedirs(os.path.dirname(filepath))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        plt.savefig(filepath, dpi=600)
        plt.close()

    '''
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
    ax = plt.gca()
    ax.set_xticks([-12.5,-8,-3.5,1,5.5])
    ax.tick_params(direction='in')

    plt.savefig('failures/'+str(i)+'.png', dpi=600)
    plt.clf()
    

    '''



