import pandas as pd
import numpy as np
from find_parents2 import *
import pickle5 as pkl

from create_tree import *
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot  import graphviz_layout

with open('HajimeIsayama_78.pkl','rb') as f:
    db = pkl.load(f) 

# db.to_excel("HajimeIsayama_78.xlsx") 
initial_twt_id = 1377153920263356420#db[(db['retweet'] == False)].id.values[0]
graph = create_tree(db, initial_twt_id, root_child=None)
pos = nx.drawing.nx_pydot.pydot_layout(graph, prog='dot') #"neato" ou "twopi" pour les graph stylés mais marche que sous linux/mac
plt.figure(figsize=(8, 8))
nx.draw_networkx(graph, pos = pos, node_size=15, width=0.3, alpha=0.8, node_color="skyblue",edge_color='grey', with_labels=False)
# plt.axis("equal")
plt.savefig('propagation_graph.png')
plt.show()