import pandas as pd
import numpy as np
import pickle5 as pkl
import networkx as nx
from create_tree import *

def Dijkstra(G,v): #Inspired from BFS
    distances = {v : 0}
    seen = [v]
    active = [v]
    while(len(active) != 0):
        w = active.pop(0)
        for x in G[w]:
	        if x not in seen: 
	            seen.append(x) #FILL HERE !
	            active.append(x) #FILL HERE !
	            distances[x] = distances[w] + 1
    return distances

def plot_depth(distance):
	pos = nx.drawing.nx_pydot.pydot_layout(graph, prog='dot')
	# nx.draw(graph, labels=distances, with_labels = True)
	nx.draw(graph, pos = pos, labels=distances, alpha=0.8, node_color="skyblue",edge_color='grey')
	#node_size=20, width=0.3
	plt.show()


def get_max_depth(distance):
	return max(distance.values())

def get_breath(distance):
	'''
	Input: distance (dict): distance of each node from the original node
	Output: 
	'''
	return [np.count_nonzero(list(distance.values())==i, axis = 0) for i in range(get_max_depth(distance))]


filename = 'colis_covid.pkl'
with open(filename,'rb') as f:
	db = pkl.load(f)

graph = create_tree(db, root_child=20) #nx.DiGraph(G)
distance = Dijkstra(graph,0)
# print(type(list(distance.values())[0]))
print(get_breath(distance))

# plot_depth(distance)
# print('max_depth', get_max_depth(filename))