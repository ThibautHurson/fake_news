import pandas as pd
import numpy as np
from find_parents import *
from find_parents2 import *
import pickle5 as pkl

from create_tree import *
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot  import graphviz_layout
# import igraph as ig

def main() :
    # db_tweet = pd.read_excel('twint_ForumCarbone.xlsx')#, encoding='latin-1')
    # db_retweet = pd.read_excel('twint_RTTest.xlsx')#, encoding='latin-1') #read_csv
    # db = pd.concat([db_tweet,db_retweet], ignore_index=True)
    with open('testPickle.pkl','rb') as f:
        db = pkl.load(f) 
        
    # Data cleaning
    db.reset_index(inplace = True,drop=True)
    db['user_id'] = pd.to_numeric(db['user_id'])
    db['id'] = pd.to_numeric(db['id'])
    db['user_rt_id'] = pd.to_numeric(db['user_rt_id'])

    # db.to_excel('dataset.xlsx')

    parents,enfants = find_parents2(db) #FIND_PARENT 1 ou 2 ICI
    db['Parents'] = parents
    db['Enfants'] = enfants

    graph = create_tree(db, root_child=None)
    pos = nx.drawing.nx_pydot.pydot_layout(graph, prog='dot') #"neato" pour les graph stylés mais marche que sous linux/mac
    # plt.figure(figsize=(8, 8))
    nx.draw_networkx(graph, pos = pos, node_size=15, width=0.3, alpha=0.8, node_color="skyblue",edge_color='grey', with_labels=False)
    plt.savefig('propagation_graph.png')
    plt.show()

if __name__ == "__main__":
    # execute only if run as a script
    main()
