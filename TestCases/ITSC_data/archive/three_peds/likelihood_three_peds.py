import numpy as np
import pickle
from scipy.stats import multivariate_normal

num_pedestrians = 3
num_paths = 20
AL_idx_no_discount = 1
AL_idx_w_discount = 0

cov = np.diag([0.5, 0.5, 0.5, 0.5, 0.5, 0.5]) #cov_x, cov_y, cov_sensor(vx, vy, dx, dy)

output_file = 'three_peds/loglh_t1.txt'


#NO DISCOUNT
open(output_file, 'w').close()
print("No discount loglikelihoods:", file=open(output_file, 'a'))
average1 = 0
average2 = 0 
average3 = 0  
for i in range(num_paths):
    pickle_path  = 'three_peds/t1_no_discount/pickles/data'+str(i)+'.pkl'
    loaded_data = pickle.load(open(pickle_path, "rb" ))
    action_list = loaded_data[AL_idx_no_discount]

    for j in range(num_pedestrians):
        likelihood = 1
        #print(cov_1)
        for action in action_list:
            cur_action = action[6*j:6*j+6]
            likelihood *= multivariate_normal.pdf(cur_action, mean=[0,0,0,0,0,0], cov=cov)

        loglh = np.log(likelihood)
        normalised_loglh = loglh/len(action_list)
        if(j==0):
            average1 += normalised_loglh
        elif(j==1):
            average2 += normalised_loglh
        else:
            average3 += normalised_loglh
        print("Trajectory ", i, " Pedestrian ", j, " normalised_loglh: ", normalised_loglh, file=open(output_file,'a'))
        print(normalised_loglh)
print("AVERAGE1: ", average1/(num_paths), file=open(output_file,'a'))
print("AVERAGE2: ", average2/(num_paths), file=open(output_file,'a'))
print("AVERAGE3: ", average3/(num_paths), file=open(output_file,'a'))
print(" ", file=open(output_file,'a'))
print(" ", file=open(output_file,'a'))

#WITH DISCOUNT
print("With discount loglikelihoods:", file=open(output_file, 'a'))
for tests in range(3):
    average1 = 0
    average2 = 0 
    average3 = 0 
    discount_param = None
    if tests == 0:
        discount_param = '050'
    elif tests == 1:
        discount_param = '100'
    else:
        discount_param = '150'

    print("PARAM: ", discount_param, ":", file=open(output_file, 'a'))

    for i in range(num_paths):
        pickle_path  = 'three_peds/t1_w_discount/traj_'+discount_param+'_state_0/pickles/data'+str(i)+'.pkl'
        loaded_data = pickle.load(open(pickle_path, "rb" ))
        action_list = loaded_data[AL_idx_w_discount]

        for j in range(num_pedestrians):
            likelihood = 1
            #print(cov_1)
            for action in action_list:
                cur_action = action[6*j:6*j+6]
                likelihood *= multivariate_normal.pdf(cur_action, mean=[0,0,0,0,0,0], cov=cov)

            loglh = np.log(likelihood)
            normalised_loglh = loglh/len(action_list)
            if(j==0):
                average1 += normalised_loglh
            elif(j==1):
                average2 += normalised_loglh
            else:
                average3 += normalised_loglh
            print("Trajectory ", i, " Pedestrian ", j, " normalised_loglh: ", normalised_loglh, file=open(output_file,'a'))
            print(normalised_loglh)

    print("AVERAGE1: ", average1/(num_paths), file=open(output_file,'a'))
    print("AVERAGE2: ", average2/(num_paths), file=open(output_file,'a'))
    print("AVERAGE3: ", average3/(num_paths), file=open(output_file,'a'))
    print(" ", file=open(output_file,'a'))
    print(" ", file=open(output_file,'a'))