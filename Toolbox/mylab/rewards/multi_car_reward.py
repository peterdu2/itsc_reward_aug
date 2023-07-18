# import base class
from mylab.rewards.ast_reward import ASTReward

# useful packages for math and debugging
import numpy as np
import pdb
import matplotlib.pyplot as plt

from operator import add

from scipy.stats import multivariate_normal


# Define the class, inherit from the base
class multi_car_reward(ASTReward):
    def __init__(self,
                 num_peds=1,
                 cov_x=0.1,
                 cov_y=0.01,
                 cov_sensor_noise=0.1):

        self.c_num_peds = num_peds
        self.c_cov_x = cov_x
        self.c_cov_y = cov_y
        self.c_cov_sensor_noise = cov_sensor_noise

        # allows reward function to access
        # current best paths, will be set by instance of MCTS
        self.MCTS_obj = None

        super().__init__()

    def give_reward(self, action, **kwargs):
        # get the info from the simulator
        info = kwargs['info']
        peds = info["peds"]
        car = info["car"]
        is_goal = info["is_goal"]
        is_terminal = info["is_terminal"]
        action = info["action"]
        dist = peds[:, 2:4] - car[2:4]

        # update reward and done bool

        cur_traj = self.MCTS_obj.tracker.get_trajectory()

        traj_difference = 0

        if (is_goal):  # We found a crash
            # Compare current trajectory with existing trajectories and discount
            # reward based off similarity measure
            for (r, tr) in self.MCTS_obj.best_paths:
                if (tr.goal_reached):
                    # Call similarity function
                    traj_difference += self.traj_similarity(cur_traj, tr.get_trajectory())
            if self.MCTS_obj.best_paths.length() != 0:
                traj_difference / self.MCTS_obj.best_paths.length()
            reward = 0 + traj_difference * self.MCTS_obj.traj_sim_discount

        elif (is_terminal):
            reward = -10000 - 1000 * np.min(np.linalg.norm(dist, axis=1))  # We reached
            # the horizon with no crash
        else:
            reward = -np.log(1 + self.mahalanobis_d(action))  # No crash or horizon yet

        return reward

    def end_state_similarity(self, traj1, traj2):

        end_state_similarity = 0

        for cur_ped in range(self.c_num_peds):
            ped1_end = [traj1[len(traj1) - 1][0][cur_ped][2], traj1[len(traj1) - 1][0][cur_ped][3]]
            ped2_end = [traj2[len(traj2) - 1][0][cur_ped][2], traj2[len(traj2) - 1][0][cur_ped][3]]

            car1_end = [traj1[len(traj1) - 1][1][2], traj1[len(traj1) - 1][1][3]]
            car2_end = [traj2[len(traj2) - 1][1][2], traj2[len(traj2) - 1][1][3]]

            # Only considering pedestrian for now
            end_state_similarity += np.linalg.norm(np.array(ped1_end) - np.array(ped2_end))

        return end_state_similarity / self.c_num_peds

    def traj_similarity(self, traj1, traj2, num_segments=10):
        similarity_idx = 0

        for cur_ped in range(self.c_num_peds):
            ped1 = []
            car1 = []
            ped2 = []
            car2 = []
            # Parse out paths
            # NOTE: traj data points are [[ped data],[car data]]
            for dp in traj1:
                ped1.append([dp[0][cur_ped][2], dp[0][cur_ped][3]])
                car1.append([dp[1][2], dp[1][3]])

            for dp in traj2:
                ped2.append([dp[0][cur_ped][2], dp[0][cur_ped][3]])
                car2.append([dp[1][2], dp[1][3]])

            ped1_seg_len = len(ped1) // num_segments  # Floor division
            ped2_seg_len = len(ped2) // num_segments

            # Compare segments (only for pedestrians right now)
            for i in range(num_segments):
                if (i == num_segments - 1):
                    cur_ped1_seg = [ped1[i * ped1_seg_len], ped1[len(ped1) - 1]]
                    cur_ped2_seg = [ped2[i * ped2_seg_len], ped2[len(ped2) - 1]]
                else:
                    cur_ped1_seg = [ped1[i * ped1_seg_len], ped1[(i + 1) * ped1_seg_len - 1]]
                    cur_ped2_seg = [ped2[i * ped2_seg_len], ped2[(i + 1) * ped2_seg_len - 1]]

                # Compare segment centroids
                centroid1 = np.add(cur_ped1_seg[0], cur_ped1_seg[1]) / 2
                centroid2 = np.add(cur_ped2_seg[0], cur_ped2_seg[1]) / 2
                dist = np.linalg.norm(centroid1 - centroid2)
                similarity_idx = dist + similarity_idx

        return similarity_idx / self.c_num_peds

    def mahalanobis_d(self, action):
        # Mean action is 0
        mean = np.zeros((6 * self.c_num_peds, 1))
        # Assemble the diagonal covariance matrix
        cov = np.zeros((self.c_num_peds, 6))
        cov[:, 0:6] = np.array([self.c_cov_x, self.c_cov_y,
                                self.c_cov_sensor_noise, self.c_cov_sensor_noise,
                                self.c_cov_sensor_noise, self.c_cov_sensor_noise])
        big_cov = np.diagflat(cov)

        # subtract the mean from our actions
        dif = np.copy(action)
        dif[::2] -= mean[0, 0]
        dif[1::2] -= mean[1, 0]

        # calculate the Mahalanobis distance
        dist = np.dot(np.dot(dif.T, np.linalg.inv(big_cov)), dif)

        return np.sqrt(dist)

    def loglh(self, action_list):
        # Mainly for testing atm

        # Covariance for first pedestrian
        # Assemble the diagonal covariance matrix
        cov = np.zeros((self.c_num_peds, 6))
        cov[:, 0:6] = np.array([self.c_cov_x, self.c_cov_y,
                                self.c_cov_sensor_noise, self.c_cov_sensor_noise,
                                self.c_cov_sensor_noise, self.c_cov_sensor_noise])
        big_cov = np.diagflat(cov)

        cov_1 = big_cov[0]

        likelihood = 1
        for action in action_list:
            likelihood *= multivariate_normal.pdf(action, mean=np.zeros(self.c_num_peds * 6), cov=cov_1,
                                                  allow_singular=True)

        return np.log(likelihood)












