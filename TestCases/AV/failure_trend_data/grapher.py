import math
import numpy as np
import pickle
import matplotlib.pyplot as plt

distances = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
AST_data = [14, 869, 873, 503, 1498, 1323, 279, 1443, 4414, 6835]
Random_data = [257, 295, 1554, 3326, 5518, 1817, 4818, 6433, 18840, 38576]

distances = np.array(distances)
ast_line = plt.plot(distances, AST_data, marker='.', markersize=11, color='xkcd:azure')
random_line = plt.plot(distances, Random_data, marker='.', markersize=11, color='xkcd:orange')
#plt.gca().set_xscale('log', basex=2)
plt.gca().set_xticks(distances)
plt.tick_params(labelsize=9)
plt.grid(True)


leg = plt.legend([ast_line[0], random_line[0]], ['AST', 'Random Sample'],  prop={'size': 12})
for lh in leg.legendHandles: 
    lh._legmarker.set_alpha(1)
leg.get_frame().set_linewidth(1.5)
leg.get_frame().set_edgecolor('black')


plt.xlabel("Max Vehicle/Pedestrian Separation (m)", size=12)
plt.ylabel("Solver Iterations", size=12)
plt.gca().invert_xaxis()
plt.savefig('ast_v_random.png', dpi=600)
plt.show()

