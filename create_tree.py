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
def create_tree(df, root_child = None):
    def helper(G, twt_id, df):
        childs = df[df['id'] == twt_id]['Enfants'].values[0]
        if not childs:
            return
        for child in childs:
            if child != int(float(twt_id)):
                G.append((twt_id, child))
                helper(G, child, df)

    G = []
    df_roots = df[(df['Parents'] == 0)]# | (df['Parents'] == -1)]  #when 0, the tweet corresponds to an original tweet
    if root_child:
        for twt_id in df_roots['id'][:root_child]:
            G.append((0, twt_id))
            helper(G, twt_id, df)        
    else:
        for twt_id in df_roots['id']:
            G.append((0, twt_id))
            helper(G, twt_id, df)

    return nx.DiGraph(G)


#Pour faire marcher l'exemple ci-dessous, décommenter | (df['Parents'] == -1)]
# df = pd.DataFrame([[1,-1,[5,7]],[2,-1,[3]],[3,2,[4]],[4,3,[]],[5,1,[6]],[6,5,[]],[7,1,[8,9]],[8,7,[10]],[9,7,[]],[10,8,[]]],index=[1,2,3,4,5,6,7,8, 9, 10], columns=['id', 'Parents', 'Enfants'])
# graph = create_tree(df)
# p = nx.drawing.nx_pydot.to_pydot(graph)
# p.write_png('prapagation_graph.png')
# nx.draw(p, with_labels=True, font_weight='bold')
# plt.show()


# def create_subtree(db)