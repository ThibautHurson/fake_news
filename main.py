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


def main() :
    start = time.time()
    name = 'HajimeIsayama'#'merrick_garland_liar_BillBarr'#'JoeBiden_Nword'#stevie_wonder_ghana
    with open(name + '_T.pkl','rb') as f:
        db_tw = pkl.load(f) 
    with open(name + '_RT.pkl','rb') as f:
        db_rt = pkl.load(f)

    nb_rtw = 78 #134   
    parent_tweet_id = 1377153920263356420    

    db_tw['id'] = pd.to_numeric(db_tw['id'])
    db_rt['retweet_id'] = pd.to_numeric(db_rt['retweet_id'])

    db_tw.drop(db_tw[ db_tw['id']!=parent_tweet_id].index, inplace=True)
    db_rt.drop(db_rt[ db_rt['retweet_id']!=parent_tweet_id].index, inplace=True)
    db = pd.concat([db_tw,db_rt], ignore_index=True)

    db['user_id'] = pd.to_numeric(db['user_id'])
    db['id'] = pd.to_numeric(db['id'])
    db['user_rt_id'] = pd.to_numeric(db['user_rt_id'])
    db['nretweets'] = pd.to_numeric(db['nretweets'])
    db['day'] = pd.to_numeric(db['day'])
    db['hour'] = pd.to_numeric(db['hour'])
    db['retweet_id'] = pd.to_numeric(db['retweet_id'])

    db['nlikes'] = pd.to_numeric(db['nretweets']) 

    db.reset_index(inplace = True,drop=True)
    print('DB SIZE IS: ',db.shape)

    parents,enfants = find_parents3(db) 
    db['Parents'] = parents
    db['Enfants'] = enfants

    output_name = name + '_' + str(nb_rtw) + '_' + str(parent_tweet_id)

    db.to_excel(output_name +'.xlsx')
    db.to_pickle(output_name +'.pkl')

    end = time.time()
    print('Epoch: ' + str(start-end))

    graph = create_tree(db, db[(db['retweet'] == False)].id.values[0], root_child=None)
    pos = nx.drawing.nx_pydot.pydot_layout(graph, prog='dot') #"neato" ou "twopi" pour les graph stylés mais marche que sous linux/mac

    nx.draw_networkx(graph, pos = pos, node_size=15, width=0.3, alpha=0.8, node_color="skyblue",edge_color='grey', with_labels=False)
    plt.savefig(output_name + '.png')
    plt.show()

if __name__ == "__main__":
    main()
