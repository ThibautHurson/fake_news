import pandas as pd
import numpy as np
from find_parents import *
from create_tree import *
import networkx as nx
import matplotlib.pyplot as plt

def main() :
    db_tweet = pd.read_csv('twint_ForumCarbone.csv', encoding='latin-1')
    db_retweet = pd.read_csv('twint_RTTest.csv', encoding='latin-1')
    db = pd.concat([db_tweet,db_retweet], ignore_index=True)
    parents,enfants = find_parents(db)
    db['Parents'] = parents
    db['Enfants'] = enfants
    # print(db[db.Parents==-1].shape)
    # print(db[db.Parents==-1].head())
    # print(db[db.Parents==0].head())

    # print(list(db['Enfants']))

    graph = create_tree(db)
    # subgraph = graph.subgraph([0,1,2,3,4])
    # p = nx.drawing.nx_pydot.to_pydot(subgraph)
    # p.write_png('prapagation_graph.png')
    
    # nx.draw_networkx(graph)
    # plt.show()

    # p = nx.drawing.nx_pydot.to_pydot(graph)
    # p.write_png('prapagation_graph.png')

    pos = nx.nx_pydot.graphviz_layout(graph, prog="neato")
    pos[0] = np.array([0, 0])
    nx.draw_shell(graph,alpha=0.4,pos=pos)
    plt.show()
    return

if __name__ == "__main__":
    # execute only if run as a script
    main()

