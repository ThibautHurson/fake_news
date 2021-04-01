import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pydot
from networkx.drawing.nx_pydot import graphviz_layout

import networkx as nx
import random

def basic_graph(n_tweet,n_max),P:
    G = nx.DiGraph()
    G.add_nodes_from([i+1 for i in range(n_tweet)])
    G.add_edges_from([(1,i) for i in range(n_tweet-1)])
    n_tot=n_tweet
    while n_tot<n_max:
        n=randint(1,n_tot)
        if random() < P :
            n_tot+=1
            
    return G

G=basic_graph(20)
nx.draw(G)
#pos = hierarchy_pos(G,1)   
#nx.draw(G,pos,with_labels=True)
plt.show()