
import numpy as np

def get_critical_states (n_step_critical, trajectories):
	
	#state format: [ [[PED1],[PED2]] , [CAR1] , [CAR2] ]

	return_state_list = []

	for traj in trajectories:
		critical_state = traj[len(traj)-n_step_critical-1]
		return_state_list.append([critical_state[0][0], critical_state[0][1], critical_state[1], critical_state[2]])

	return return_state_list