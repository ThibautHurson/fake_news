import pandas as pd
import numpy as np
from find_parents import *
from find_parents2 import *
import pickle5 as pkl

from create_tree import *
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot  import graphviz_layout
import time
# import igraph as ig

def main() :
    # db_tweet = pd.read_excel('twint_ForumCarbone.xlsx')#, encoding='latin-1')
    # db_retweet = pd.read_excel('twint_RTTest.xlsx')#, encoding='latin-1') #read_csv
    # db = pd.concat([db_tweet,db_retweet], ignore_index=True)
    start = time.time()
    name = 'stevie_wonder_ghana'#'merrick_garland_liar_BillBarr'#'JoeBiden_Nword'#'fakesnow'
    with open(name + '_T.pkl','rb') as f:
        db_tw = pkl.load(f) 
    with open(name + '_RT.pkl','rb') as f:
        db_rt = pkl.load(f)
    db = pd.concat([db_tw,db_rt], ignore_index=True)
    
    
    # with open('testPickle2.pkl','rb') as f:
    #     db = pkl.load(f) 
        # db.to_excel('testPickle2.xlsx')
    # Data cleaning


    db.reset_index(inplace = True,drop=True)
    db['user_id'] = pd.to_numeric(db['user_id'])
    db['id'] = pd.to_numeric(db['id'])
    db['user_rt_id'] = pd.to_numeric(db['user_rt_id'])
    db['nretweets'] = pd.to_numeric(db['nretweets'])
    db['day'] = pd.to_numeric(db['day'])
    db['hour'] = pd.to_numeric(db['hour'])
    db['retweet_id'] = pd.to_numeric(db['retweet_id'])


    # db = pd.concat([db[db['retweet_id'] == 1352722423267909634], db[db['id'] == 1352722423267909634]])
    # db.reset_index(inplace = True,drop=True)

    # db.to_excel('dataset.xlsx')

    parents,enfants = find_parents3(db) 
    db['Parents'] = parents
    db['Enfants'] = enfants
    db.to_pickle(name + '.pkl')

    end = time.time()
    print('Epoch: ' + str(start-end))

    graph = create_tree(db, root_child=None)
    pos = nx.drawing.nx_pydot.pydot_layout(graph, prog='dot') #"neato" ou "twopi" pour les graph stylés mais marche que sous linux/mac
    # plt.figure(figsize=(8, 8))
    nx.draw_networkx(graph, pos = pos, node_size=15, width=0.3, alpha=0.8, node_color="skyblue",edge_color='grey', with_labels=False)
    plt.savefig('propagation_graph.png')
    plt.show()

if __name__ == "__main__":
    # execute only if run as a script
    main()
