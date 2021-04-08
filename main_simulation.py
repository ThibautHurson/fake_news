import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd

from features import *
from propagation_simulation import BFS_propagation

#Load Graph
G = nx.read_gpickle('network_simulation_30.pkl')


#Model Parameters
p_true = 0.5
decay_true = 0.4

p_fake = 0.7
decay_fake = 0.3

data_list = []
for k in range(20):
	#Pick a propagator
	idx = np.random.randint(len(G))

	#Get graph	
	result, prop = BFS_propagation(G,idx,p_true,decay_true)

	#To deal with 1-node graph
	if len(result) >= 2:
		data_list.append([nx.number_of_nodes(prop),get_depth(prop,idx),get_breath(prop,idx),get_virality(prop),avg_neigh(prop),1])

for k in range(20):
	#Pick a propagator
	idx = np.random.randint(len(G))

	#Get graph	
	result, prop = BFS_propagation(G,idx,p_fake,decay_fake)

	#To deal with 1-node graph	
	if len(result) >= 2:
		data_list.append([nx.number_of_nodes(prop),get_depth(prop,idx),get_breath(prop,idx),get_virality(prop),avg_neigh(prop),-1])



df_true_fake = pd.DataFrame(data_list, columns=['Size','Depth','Breadth','Virality','Avg_neigh','label'])


df_true_fake.to_pickle('simulation_dataset.pkl')
