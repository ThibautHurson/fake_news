import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import glob
from PIL import Image
import os
import shutil

os.environ["PATH"] += os.pathsep + 'C:\Program Files\Graphviz 2.44.1/bin/'



def BFS_propagation(G,v,p_start,decay): #Inspired from BFS
	Prop=nx.DiGraph()
	seen = [v]
	active = [v]
	result = []
	distances = {v : 0}
	while(len(active) != 0):
		w = active.pop(0)
		result.append(w)
		Prop.add_nodes_from([w])
		for x in G[w]:
			if x not in seen and np.random.random() < p_start*(1-decay)**(distances[w]+1):
				Prop.add_edges_from([(w,x)])
				seen.append(x)
				active.append(x)
				distances[x] = distances[w] + 1
	return result, Prop

def get_gif(G, result):
	# Create a directory if don't exist to store images that will be used to create the gif
	dir_images = "images_for_gif"
	if not os.path.exists(dir_images):
	    os.mkdir(dir_images)
	else:
		shutil.rmtree(dir_images) #Delete the folder and its content
		os.mkdir(dir_images)


	labeldict = {val:'' for val in G}
	colors = ['b'] * len(G) #Initialize each vertex color to black

	pos = nx.spring_layout(G)

	for i in range(len(result)):
		node_idx = result[i]
		labeldict[node_idx] = i
		colors[node_idx] = 'r'

		nx.draw_networkx(G, pos,labels=labeldict, node_size=15,alpha=0.6, node_color=colors, with_labels=True) #width=0.3,node_size=15, 
		nx.draw_networkx_edges(G, pos, edge_color='grey',alpha=0.1)
		plt.savefig(dir_images +"/image_{}.png".format(str(i)), dpi=1200)



	dir_gif = "gif"
	if not os.path.exists(dir_gif):
	    os.mkdir(dir_gif)

	# filepaths
	fp_in = dir_images +"/image_*.png"
	fp_out = dir_gif + "/image.gif"

	# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
	img, *imgs = [Image.open(dir_images +"/image_{}.png".format(k)) for k in range(len(os.listdir(dir_images)))]
	img.save(fp=fp_out, format='GIF', append_images=imgs, duration=200,
	         save_all=True, loop=0)#diposal=2 to restore background color # duration=100


def plot_propagation_graph(prop,idx):
	pos = nx.drawing.nx_pydot.pydot_layout(prop, prog='dot')
	nx.draw_networkx(prop, pos, node_size=15,alpha=0.6) #width=0.3,node_size=15, 
	nx.draw_networkx_edges(prop, pos, edge_color='grey',alpha=0.1)
	plt.show()
	#Pickle Time
	name=str(idx)+'_propagation_tree.pkl'
	nx.write_gpickle(prop, name)

def plot_propagation_in_graph(G,result):
	#Create Labels
	labeldict = {}
	colors = []
	for i, val in enumerate(G):
		if i in result:		
			labeldict[val] = result.index(i)
			colors.append('r')
		else:
			labeldict[val] = ''
			colors.append('b')

	#Print Graph
	print(result)

	pos = nx.spring_layout(G)
	nx.draw_networkx(G, pos,labels=labeldict, node_size=15,alpha=0.6, node_color=colors, with_labels=True) #width=0.3,node_size=15, 
	nx.draw_networkx_edges(G, pos, edge_color='grey',alpha=0.1)
	plt.show()


#Load Graph
G = nx.read_gpickle('network_simulation_30.pkl')


#Pick a propagator
idx = np.random.randint(len(G))

#Model Parameters
p = 0.8
decay=0.2

#Get graph	
result, prop = BFS_propagation(G,idx,p,decay)

get_gif(G, result)