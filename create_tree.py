import pandas as pd
import numpy as np
# from graphviz import Graph
import networkx as nx
import matplotlib.pyplot as plt
# import igraph as ig

#Tweet id c'est l'id du tweet
#Tweet parent c'est l'id de son parent (si c'est un RT)
#-1 dans tweet_parent: tweet original (point de départ)


#We are considering tweet_id, tweet_parent, tweet_fils to create the tree
def create_tree(df, initial_twt_id, root_child = None):
    '''
    Param
        df: dataframe containing information about tweet, retweet, users etc.
        root_child: number of root children you want to consider. If None than you consider every root children.
    Output
        a networkx DiGraph
    '''
    def helper(G, twt_id, df):
        childs = df[df['id'] == twt_id]['Enfants'].values[0]
        if not childs:
            return
        for child in childs:
            if child != int(twt_id):
                G.append((twt_id, child))
                helper(G, child, df)

    G = []
    df_roots = df[(df['Parents'] == initial_twt_id)]# | (df['Parents'] == -1)]  #when 0, the tweet corresponds to an original tweet
    if root_child:
        for twt_id in df_roots['id'][:root_child]:
            G.append((initial_twt_id, twt_id))
            helper(G, twt_id, df)        
    else:
        for twt_id in df_roots['id']:
            G.append((initial_twt_id, twt_id))
            helper(G, twt_id, df)
    print(G)
    return nx.DiGraph(G)



# df = pd.DataFrame([[1377206604618215429], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [1377150118017691654], [], [], [1377178658977112070], [], [], [1377193333068562433], [], [1377163985531768836], [], [], [1377175954540257280], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [1377158134234419209], [], [], [], [], [], [], [], [], [], [], [], []]
# ,index=[1,2,3,4,5,6,7,8, 9, 10], columns=['id', 'Parents', 'Enfants'])
# graph = create_tree(df, 1377153920263356420, root_child=None)
# pos = nx.drawing.nx_pydot.pydot_layout(graph, prog='dot')
# nx.draw_networkx(graph, pos = pos, node_size=15, width=0.3, alpha=0.8, node_color="skyblue",edge_color='grey', with_labels=False)
# plt.savefig('propagation_graph.png')
# plt.show()