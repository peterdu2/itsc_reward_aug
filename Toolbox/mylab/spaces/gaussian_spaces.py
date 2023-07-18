from mylab.spaces.ast_spaces import ASTSpaces
from gym.spaces.box import Box
import numpy as np

class GaussianAS:
    def __init__(self, mean_arr, sd_arr, num_agents):
        self.mean_arr = mean_arr
        self.sd_arr = sd_arr
        self.num_agents = num_agents

    def sample(self):
        action = []
        for i in range(self.num_agents):

            #manually take care of noise params for now (noise shouldn't be negative)
            for component in range(len(self.mean_arr)):
                if component == 0 or 1:
                    action.append(np.random.normal(self.mean_arr[component], self.sd_arr[component]))  #sample action component from gaussian defined by mean/sd
                else:
                    noise = np.random.normal(self.mean_arr[component], self.sd_arr[component])
                    if noise < 0:
                        noise = 0
                    action.append(noise)

        return np.array(action)

class GaussianSpaces(ASTSpaces):
    def __init__(self,
                 num_peds,
                 means,
                 sds
                 ):

        # Constant hyper-params -- set by user
        self.c_num_peds = num_peds
        self.c_means = means
        self.c_sds = sds
        super().__init__()

    @property
    def action_space(self):
        return GaussianAS(self.c_means, self.c_sds, self.c_num_peds)

    @property
    def observation_space(self):
        return GaussianAS(self.c_means, self.c_sds, self.c_num_peds)
