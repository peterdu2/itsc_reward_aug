from mylab.rewards.ast_reward import ASTReward
import numpy as np


# Define the class, inherit from the base
class IntersectionReward(ASTReward):
    def __init__(self, num_agents):

        self._num_agents = num_agents
        self.MCTS_obj = None

    def give_reward(self, action, **kwargs):

        reward = 1

        info = kwargs['info']
        states = info['states']
        is_goal = info['is_goal']
        is_terminal = info['is_terminal']
        action = info['action']

        cur_traj = self.MCTS_obj.tracker.get_trajectory()

        if is_goal:
            sp_dist = 0
            counter = 0
            for (r, tr) in self.MCTS_obj.best_paths:
                #print(tr.get_trajectory()[len(tr.get_trajectory())-1])
                if (tr.goal_reached):
                    #Calculate spatial difference in end state
                    e1 = cur_traj[len(cur_traj)-1]
                    e2 = tr.get_trajectory()[len(tr.get_trajectory())-1]
                    sp_dist = (e1[0][1]**2 + e2[0][1]**2)**0.5 + (e1[1][1]**2 + e2[1][1]**2)**0.5  #distance between car1s and distance between car2s
                    counter += 1
            if counter != 0:
                sp_dist /= counter
            
            reward = sp_dist * self.MCTS_obj.traj_sim_discount


        elif is_terminal:
            reward  = -10000 - 1000 * (states[0][1]**2 + states[1][1]**2)**0.5

        else:
            cov_inv = np.linalg.inv([[1,0],[0,1]])
            mu = np.zeros(2)
            m_dist = 0

            for i in range(self._num_agents):
                a = [action[4*i], action[4*i+1]]
                a_minus_mu = a - mu
                left_term = np.dot(a_minus_mu, cov_inv)
                m_dist += np.dot(left_term, a_minus_mu.T)

            reward = -m_dist

        return reward