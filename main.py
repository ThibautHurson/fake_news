import pandas as pd
import numpy as np
from find_parents import *
from create_tree import *
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot  import graphviz_layout
# import igraph as ig

def main() :
    db_tweet = pd.read_csv('twint_ForumCarbone.csv', encoding='latin-1')
    db_retweet = pd.read_csv('twint_RTTest.csv', encoding='latin-1')
    db = pd.concat([db_tweet,db_retweet], ignore_index=True)
    parents,enfants = find_parents(db)
    db['Parents'] = parents
    db['Enfants'] = enfants

    # print(list(db['Enfants']))

    graph = create_tree(db, root_child=30)
    pos = nx.drawing.nx_pydot.pydot_layout(graph, prog='dot')
    nx.draw_networkx(graph, pos = pos, node_size=15, width=0.3, alpha=0.8, node_color="skyblue",edge_color='grey', with_labels=False)
    plt.savefig('propagation_graph.png')
    plt.show()

    # pos = nx.nx_pydot.graphviz_layout(graph, prog="neato")
    # pos = graphviz_layout(graph, prog="dot")#, args="")
    # pos[0] = np.array([0, 0])
    # plt.figure(figsize=(8, 8))
    # nx.draw_networkx(graph, pos = pos, node_size=15, width=0.3, alpha=0.5, node_color="skyblue",edge_color='grey', with_labels=False)
    # plt.axis("equal")
    # plt.show()
    # return

if __name__ == "__main__":
    # execute only if run as a script
    main()
