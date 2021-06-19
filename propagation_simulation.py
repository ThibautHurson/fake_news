import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import glob
from PIL import Image
import os
import shutil
from networkx.drawing.nx_pydot  import graphviz_layout
import time

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
	return result, Prop, distances

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
		plt.savefig(dir_images +"/"+str(i)+".png", dpi=1200)


	# time.sleep(30)

	dir_gif = "gif"
	if not os.path.exists(dir_gif):
	    os.mkdir(dir_gif)

	# filepaths
	fp_in = dir_images +"/image_*.png"
	fp_out = dir_gif + "/image.gif"

	# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
	imgs = []
	print('Nombre d image : ',len(os.listdir(dir_images)))
	for k in range(len(os.listdir(dir_images))):
		image = Image.open(dir_images +"/"+str(k)+".png")
		imgs.append(image)
		imgs.append(image)
		imgs.append(image)
		imgs.append(image)


	# img, *imgs = [Image.open(dir_images +"/image_{}.png".format(str(k))) for k in range()]
	imgs[0].save(fp_out, append_images=imgs[1:], #duration=200,
	         save_all=True, duration=400, loop=0, optimizer=False)#diposal=2 to restore background color # duration=100


def plot_propagation_graph(prop,idx):
	pos = nx.drawing.nx_pydot.pydot_layout(prop, prog='dot')
	nx.draw_networkx(prop, pos, node_size=15,alpha=0.6,with_labels=False) #width=0.3,node_size=15, 
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
	nx.draw_networkx(G, pos, labels=labeldict, node_size=15,alpha=0.6, node_color=colors, with_labels=True) #width=0.3,node_size=15,  with_labels=True
	nx.draw_networkx_edges(G, pos, edge_color='grey',alpha=0.1)
	plt.show()


#Load Graph
G = nx.read_gpickle('network_simulation_20.pkl')


#Pick a propagator
idx = np.random.randint(len(G))

# #Model Parameters
p_fake = 0.8
decay_fake = 0.1

#Get graph	
result, prop, _ = BFS_propagation(G,idx,p_fake,decay_fake)

get_gif(G, result)


# plot_propagation_graph(prop,idx)