import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd

from features import *
from propagation_simulation import BFS_propagation

#Load Graph
entry='network_simulation_100.pkl'
G = nx.read_gpickle(entry)


#Model Parameters
p_true = 0.4
decay_true = 0.2

p_fake = 0.6
decay_fake = 0.1

data_list = []
for k in range(200):
	#Pick a propagator
	
	idx = np.random.randint(len(G))
	current_idx=0
	for current_node in G.__iter__():
		if current_idx == idx :
			node_idx=current_node
		current_idx+=1
	#Get graph	
	result, prop, _ = BFS_propagation(G,node_idx,p_true,decay_true)
	# print(result)

	distances = Dijkstra(prop,node_idx)

	#To deal with 1-node graph
	if len(result) >= 2:
		data_list.append([nx.number_of_nodes(prop),get_max_depth(distances),get_max_breath(distances),get_virality(prop),avg_neigh(prop),1]) #get_virality(prop)
	else: data_list.append([0,0,0,0,0,1])

for k in range(200):
	#Pick a propagator
	idx = np.random.randint(len(G))
	current_idx=0
	for current_node in G.__iter__():
		if current_idx == idx :
			node_idx=current_node
		current_idx+=1
	#Get graph	
	result, prop, _ = BFS_propagation(G,node_idx,p_fake,decay_fake)
	# print(result)

	distances = Dijkstra(prop,node_idx)

	#To deal with 1-node graph	
	if len(result) >= 2:
		data_list.append([nx.number_of_nodes(prop),get_max_depth(distances),get_max_breath(distances),get_virality(prop) ,avg_neigh(prop),0]) #get_virality(prop)
	else: data_list.append([0,0,0,0,0,0])


df_true_fake = pd.DataFrame(data_list, columns=['Size','Depth','Breadth','Virality','Avg_neigh','label'])

output='dataset_'+entry
df_true_fake.to_pickle(output)
