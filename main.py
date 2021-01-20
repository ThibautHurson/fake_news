import pandas as pd
import numpy as np
from find_parents import *
from create_tree import *
#from AnalyseG import *

def main() :
    db_tweet = pd.read_csv('twint_ForumCarbone.csv',encoding='latin-1')
    db_retweet = pd.read_csv('twint_RTTest.csv',encoding='latin-1')
    db = pd.concat([db_tweet,db_retweet],ignore_index=True)
    parents,enfants = find_parents(db)
    db['Parents'] = parents
    db['Enfants'] = enfants
    # print(db[db.Parents==-1].shape)
    # print(db[db.Parents==-1].head())
    # print(db[db.Parents==0].head())

    # print(db.columns)
    graph = create_tree(db)
    p = nx.drawing.nx_pydot.to_pydot(graph)
    p.write_png('propagation_graph.png')

    return 
main()
#Data_set=main()
#Data_set.to_excel("ForumCarbone_treated.xlsx") 