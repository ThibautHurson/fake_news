import pandas as pd
import numpy as np
from find_parents import *
from create_tree import *

def precision_graphe(db):
    erreur=0
    c=0
    erreur2=0
    c2=0
    for i in range(db.shape[0]):
        
        erreur_loc2=abs(int(db.at[i,'nretweets'])-len(db.at[i,'Enfants']))
        erreur2+=erreur_loc2
        c2+=1
        if db.at[i,'Enfants']:
            erreur_loc=abs(int(db.at[i,'nretweets'])-len(db.at[i,'Enfants']))
            erreur+=erreur_loc
            c+=1
    return erreur/c,erreur2/c2

def pseudo_main():
    db = pd.read_csv('ForumCarbone_treated.csv',encoding='latin-1')
    precision,p2=precision_graphe(db)
    print(precision)
    print(p2)
    return

pseudo_main()