import math
import numpy as np
import pickle
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

top_k = 50
num_trees = 238

def endpoint_plotter():
    for i in range(num_trees):
        trajectory_list = pickle.load(open('forest_data/F2/'+str(i)+'.pkl', "rb"))[1]

        agent1_ep = [[],[]]
        agent2_ep = [[],[]]

        for j in range(top_k):
            
            traj =  trajectory_list[j]
            agent1_ep[0].append(0)
            agent1_ep[1].append(traj[-1][0][1])

            agent2_ep[0].append(traj[-1][1][1])
            agent2_ep[1].append(0)

        plt.scatter(agent1_ep[0], agent1_ep[1], s=3)
        plt.scatter(agent2_ep[0], agent2_ep[1], s=3)
        plt.show()


def endpoint_plotter_all():
    agent1_ep = [[],[]]
    agent2_ep = [[],[]]

    for i in range(num_trees):
        trajectory_list = pickle.load(open('forest_data/F2/'+str(i)+'.pkl', "rb"))[1]

        for j in range(top_k):
            
            traj =  trajectory_list[j]
            agent1_ep[0].append(0)
            agent1_ep[1].append(traj[-1][0][1])

            agent2_ep[0].append(traj[-1][1][1])
            agent2_ep[1].append(0)

    plt.scatter(agent1_ep[0], agent1_ep[1], s=3)
    plt.scatter(agent2_ep[0], agent2_ep[1], s=3)
    plt.show()


def endpoint_kmeans():
    agent1_ep = [[],[]]
    agent2_ep = [[],[]]

    for i in range(num_trees):
        trajectory_list = pickle.load(open('forest_data/F2/'+str(i)+'.pkl', "rb"))[1]

        for j in range(top_k):
            
            traj =  trajectory_list[j]
            agent1_ep[0].append(0)
            agent1_ep[1].append(traj[-1][0][1])

            agent2_ep[0].append(traj[-1][1][1])
            agent2_ep[1].append(0)

    a1 =np.array([list(a) for a in zip(agent1_ep[0], agent1_ep[1])])            # Assemble endpoint data into arrays: [[e1], [e2], ...]
    a2 = np.array([list(a) for a in zip(agent2_ep[0], agent2_ep[1])]) 

    kmeans_data = np.array([list(a) for a in zip(agent1_ep[1], agent2_ep[0])])   # Perform Kmeans with endpoint locations (ignoring zero components)
    print(a1)

    kmeans = KMeans(n_clusters=4).fit(kmeans_data)

    for i in range(len(a1)):
        if kmeans.labels_[i] == 0:
            plt.scatter(a1[i][0], a1[i][1], color='blue')
            plt.scatter(a2[i][0], a2[i][1], color='blue')
        elif kmeans.labels_[i] == 1:
            plt.scatter(a1[i][0], a1[i][1], color='red')
            plt.scatter(a2[i][0], a2[i][1], color='red')
        elif kmeans.labels_[i] == 2:
            plt.scatter(a1[i][0], a1[i][1], color='green')
            plt.scatter(a2[i][0], a2[i][1], color='green')
        else:
            plt.scatter(a1[i][0], a1[i][1], color='purple')
            plt.scatter(a2[i][0], a2[i][1], color='purple')

    plt.show()

    
def num_cluster_elbow(cluster_nums, data):
    # Generate elbow graph
    sd = []
    for k in cluster_nums:
        km = KMeans(n_clusters=k).fit(data)
        sd.append(km.inertia_)

    plt.plot(K, sd, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum_of_squared_distances')
    plt.title('Elbow Method For Optimal k')
    plt.show()
    

if __name__ == '__main__':
    endpoint_kmeans()

