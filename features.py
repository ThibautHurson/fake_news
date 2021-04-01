import pandas as pd
import numpy as np
import pickle as pkl
import networkx as nx
from create_tree import *
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot  import graphviz_layout

def Dijkstra(graph,v): #Inspired from BFS
    G=graph.to_undirected()
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
	nx.draw(graph, pos = pos, labels=distance, alpha=0.8, node_color="skyblue",edge_color='grey')
	#node_size=20, width=0.3
	plt.show()


def get_max_depth(distance):
	return max(distance.values())

def get_size(graph):
	return graph.number_of_nodes()

def get_breath(graph):
	'''
	Input: distance (dict): distance of each node from the original node
	Output: 
	'''
	distance=Dijkstra(graph,graph[0])
	breadth=[0]*(get_max_depth(distance)+1)
	for k,v in distance.items():
		breadth[v]+=1
	return np.argmax(breadth)
	
def get_virality(graph):
	size=get_size(graph)
	virality=0
	for node in graph.__iter__():
		distances=Dijkstra(graph,node)
		virality+=sum(distances.values())
	virality=virality/size/(size-1)
	return virality

def avg_neigh(graph):
    G=graph.to_undirected()
    return sum([deg for (node,deg) in G.degree])/get_size(graph)


filename = 'colis_covid_corrige.pkl'
with open(filename,'rb') as f:
	db = pkl.load(f)


graph = create_tree(db, root_child=70) #nx.DiGraph(G)

#Plot Arbre
pos = nx.drawing.nx_pydot.pydot_layout(graph, prog='dot') #"neato" ou "twopi" pour les graph stylés mais marche que sous linux/mac
plt.figure(figsize=(8, 8))
nx.draw_networkx(graph, pos = pos, node_size=15, width=0.3, alpha=0.8, node_color="skyblue",edge_color='grey', with_labels=False)
# plt.axis("equal")
plt.savefig('propagation_graph.png')
plt.show()


distance = Dijkstra(graph,0)
# print(type(list(distance.values())[0]))
print(db.head())
print(get_breath(distance))

# plot_depth(distance)
# print('max_depth', get_max_depth(filename))