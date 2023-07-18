from mylab.spaces.ast_spaces import ASTSpaces
from gym.spaces.box import Box
import numpy as np
import random

class IntersectionAS:
    def __init__(self, num_agents, nv_range=[-0.5,0.5], np_range=[-0.5,0.5]):

        self._num_agents = num_agents
        self._nv_range = nv_range
        self._np_range = np_range

    def sample(self):
        
        #Each action consists of [nv, np, di, do] where:
        # nv = noise on velocity measurement
        # np = noise on position measurement
        # di = drop incoming packet
        # do = drop outgoing packet

        #Overall action vector is a concatentation of actions for each agent

        action = []
        for i in range(self._num_agents):
            action.append(random.uniform(self._nv_range[0],self._nv_range[1]))
            action.append(random.uniform(self._np_range[0],self._np_range[1]))
            action.append(random.randint(0,1))
            action.append(random.randint(0,1))
        return np.array(action)


class IntersectionSpaces(ASTSpaces):
    def __init__(self,
                 num_agents,
                 nv_range,
                 np_range
                 ):

        # Constant hyper-params -- set by user
        self.num_agents = num_agents
        self.nv_range = nv_range
        self.np_range = np_range
        super().__init__()

    @property
    def action_space(self):
        return IntersectionAS(num_agents=self.num_agents, nv_range=self.nv_range, np_range=self.np_range)

    @property
    def observation_space(self):
        return IntersectionAS(num_agents=self.num_agents, nv_range=self.nv_range, np_range=self.np_range)