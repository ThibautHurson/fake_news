import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math


def BFS_propagation(G,v,p,n_max): #Inspired from BFS
	seen = [v]
	active = [v]
	result = []
	n = 0
	while(len(active) != 0) and n < n_max:
		n += 1
		w = active.pop(0)
		result.append(w)
		for x in G[w]:
			if x not in seen and np.random.random() < p:
				seen.append(x)
				active.append(x)
	return seen

G = nx.read_gpickle('network_simulation.pkl')
idx = np.random.randint(len(G))
n_max = 100
p = 0.8

result = BFS_propagation(G,idx,p,n_max)

print(result)


labeldict = {}
for i, val in enumerate(G):
	if i in result:		
		labeldict[val] = result.index(i)
	else:
		labeldict[val] = -1

nx.draw(G, labels=labeldict, with_labels = True)
plt.show()