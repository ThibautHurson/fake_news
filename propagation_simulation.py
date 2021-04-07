import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import glob
from PIL import Image
import os
import shutil

os.environ["PATH"] += os.pathsep + 'C:\Program Files\Graphviz 2.44.1/bin/'

def generate_prop_graph() :
	#Load a graph
	G = nx.read_gpickle('network_simulation.pkl')

	#Pick a propagator
	idx = np.random.randint(len(G))
	n_max = 100
	p = 0.8

	#Get graph	
	result, prop = BFS_propagation(G,idx,p)

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
	pos = nx.drawing.nx_pydot.pydot_layout(prop, prog='dot')
	nx.draw_networkx(prop, pos,labels=labeldict, node_size=15,alpha=0.6,node_color=colors, with_labels=True) #width=0.3,node_size=15, 
	nx.draw_networkx_edges(prop, pos, edge_color='grey',alpha=0.1)
	plt.show()

	#pos = nx.spring_layout(G)
	#nx.draw_networkx(G, pos,labels=labeldict, node_size=15,alpha=0.6, node_color=colors, with_labels=True) #width=0.3,node_size=15, 
	#nx.draw_networkx_edges(G, pos, edge_color='grey',alpha=0.1)
	#plt.show()

	return


def BFS_propagation(G,v,p): #Inspired from BFS
	Prop=nx.DiGraph()
	seen = [v]
	active = [v]
	result = []
	while(len(active) != 0):
		w = active.pop(0)
		result.append(w)
		Prop.add_nodes_from([w])
		for x in G[w]:
			if x not in seen and np.random.random() < p:
				Prop.add_edges_from([(w,x)])
				seen.append(x)
				active.append(x)
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
	img = [Image.open(dir_images +"/image_{}.png".format(str(k))) for k in range(len(os.listdir(dir_images)))]
	img[0].save(fp=fp_out, format='GIF', append_images=img[1:], duration=100,
	         save_all=True, loop=0)#diposal=2 to restore background color # duration=100

generate_prop_graph()