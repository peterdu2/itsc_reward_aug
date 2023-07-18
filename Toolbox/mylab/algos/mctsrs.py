import mylab.mcts.AdaptiveStressTestingRandomSeed as AST_RS
from mylab.algos.mcts import MCTS

class MCTSRS(MCTS):
	"""
	MCTS with Random Seed as action
	"""
	def __init__(self,
		seed,
		rsg_length,
		**kwargs):
		"""
		:param seed: the seed used to generate the initial random seed generator.
		:param rsg_length: the length of the state of teh random seed generator. Set it to higher values for extreme large problems.
		:return: No return value.
		"""
		self.seed = seed
		self.rsg_length = rsg_length
		super(MCTSRS, self).__init__(**kwargs)

	def init(self):
		ast_params = AST_RS.ASTParams(self.max_path_length,self.rsg_length,self.seed,self.log_interval,self.log_tabular)
		self.ast = AST_RS.AdaptiveStressTestRS(p=ast_params, env=self.env, top_paths=self.top_paths)