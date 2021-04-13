import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd
import pickle5 as pkl

from features import *
from propagation_simulation import BFS_propagation

#Load Graph
entry = 'network_simulation_500.pkl'#'fb_network.pkl'  #'network_simulation_100.pkl'
G = nx.read_gpickle(entry)
# print(nx.number_of_nodes(G))

#Model Parameters
# p_true = 0.3
mu_true, sigma_true = 0.3, 0.1 # mean and standard deviation
decay_true = 0.4

mu_fake, sigma_fake = 0.5, 0.2 # mean and standard deviation
# p_fake = 0.5
decay_fake = 0.4


data_list = []

for k in range(1000):
	#Pick a propagator
	p_true = np.random.normal(mu_true, sigma_true)
	if p_true < 0.001:
		p_true = 0.001
	elif p_true > 0.999:
		p_true = 0.999

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

for k in range(1000):
	#Pick a propagator
	p_fake = np.random.normal(mu_fake, sigma_fake)
	if p_fake < 0.001:
		p_fake = 0.001
	elif p_fake > 0.999:
		p_fake = 0.999

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

print('Over')

df_true_fake = pd.DataFrame(data_list, columns=['Size','Depth','Breadth','Virality','Avg_neigh','label'])

output='dataset_'+entry
df_true_fake.to_pickle(output)
