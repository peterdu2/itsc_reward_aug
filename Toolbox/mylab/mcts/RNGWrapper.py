import numpy as np
import copy
import mylab.mcts.seeding as seeding

class RSG:
	def __init__(self,state):
		self.state = state
	def __eq__(self,other):
		return np.array_equal(self.state,other.state)
	def __hash__(self):
		return hash(tuple(self.state))
	def length(self):
		return len(self.state)
	def next1(self):
		self.state = np.array(list(map(seeding.hash_seed,self.state)),dtype=np.uint32)
	def next(self):
		rsg1 = copy.deepcopy(self)
		rsg1.next1()
		return rsg1
	def set_from_seed(self, length, seed):
		self.state = seed_to_state_itr(length,seed)

def RSGInit(state_length=1,seed=0):
	return RSG(seed_to_state_itr(state_length,seed))

def seed_to_state_itr(state_length,seed):
	state = []
	seedi = seed
	for i in range(state_length):
		# print(seedi)
		state.append(seedi)
		seedi = seeding.hash_seed(seedi)
	return np.array(state,dtype=np.uint32)



