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
from mylab.simulators.multi_car_simulator import multi_car_simulator
from mylab.spaces.example_av_spaces import ExampleAVSpaces

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


top_k = 20
bg_ped_paths = []#[2,5,8,10]


trajs = pickle.load(open( 'high_exp/high_exp.pkl', "rb" ))[0]

for i in range(top_k):
    print(i)

    car_x = []
    car_y = []
    car2_x = []
    car2_y = []
    ped1_x = []
    ped1_y = []
    ped2_x = []
    ped2_y = []

    for pos in trajs[i]:
        car_x.append(pos[1][2])
        car_y.append(pos[1][3])
        car2_x.append(pos[2][2])
        car2_y.append(pos[2][3])
        ped2_x.append(pos[0][0][2])
        ped2_y.append(pos[0][0][3])
        ped1_x.append(pos[0][1][2])
        ped1_y.append(pos[0][1][3])
    

    #adjustment so everything shows up in frame without overlap
    car2_x = np.array(car2_x) - 6
    ped1_x = np.array(ped1_x) + 3.5
    ped2_x = np.array(ped2_x) + 3.5 

    for frame in range(len(car_x)):

        car1_image_path = get_sample_data('/home/peter/Research/AST_RevC/TestCases/AV/animations/car1.png')
        car2_image_path = get_sample_data('/home/peter/Research/AST_RevC/TestCases/AV/animations/car2.png')
        ped_image_path = get_sample_data('/home/peter/Research/AST_RevC/TestCases/AV/animations/person.png')

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

        filepath = 'animations/high_exp/T'+str(i)+'/'+str(frame)+'.jpeg'
        if not os.path.exists(os.path.dirname(filepath)):
            try:
                os.makedirs(os.path.dirname(filepath))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        plt.savefig(filepath, dpi=600)
        plt.close()
  
