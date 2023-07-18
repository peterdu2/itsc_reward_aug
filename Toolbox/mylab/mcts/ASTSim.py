import mylab.mcts.MDP as MDP
import mylab.mcts.RNGWrapper as RNG

class SampleResults:
	def __init__(self,reward,action_seq):
		self.reward=reward
		self.action_seq=action_seq

class AcionSequence:
	def __init__(self,sequence,index=0):
		self.sequence = sequence
		self.index = index

def action_seq_policy_basic(action_seq):
	action = action_seq.sequence[action_seq.index]
	action_seq.index += 1
	return action

def action_seq_policy(action_seq,s):
	return action_seq_policy_basic(action_seq)

# def uniform_policy(ast_rsg,s):
# 	if type(ast_rsg)==AST.AdaptiveStressTest:
# 		return AST.random_action(ast_rsg.rsg)
# 	elif type(ast_rsg)==RNG.RSG:
# 		return AST.random_action(ast_rsg)

def uniform_policy(ast,s):
	return ast.random_action()

def sample(ast,verbose=True):
	reward, actions = MDP.simulate(ast.transition_model,ast,uniform_policy,verbose=verbose)
	return SampleResults(reward,actions)

def nsample(ast,nsamples,print_rate=1):
	results=[]
	for i in range(nsamples):
		if i%print_rate == 1:
			print("sample ",i," of ",nsamples)
		results.append(sample(ast,verbose=False))
	return results

def play_sequence(ast,actions,verbose=True,sleeptime=0.0):
	# print(len(actions))
	reward2,actions2 = MDP.simulate(ast.transition_model,AcionSequence(actions),action_seq_policy,verbose=verbose,sleeptime=sleeptime)
	assert actions == actions2
	return reward2,actions2


