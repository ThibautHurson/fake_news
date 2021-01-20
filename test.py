import pandas as pd
import numpy as np


#df = pd.DataFrame([[1,-1,[5,7]],[2,-1,[3]],[3,2,[4]],[4,3,[]],[5,1,[6]],[6,5,[]],[7,1,[8,9]],[8,7,[10]],[9,7,[]],[10,8,[]]],index=[1,2,3,4,5,6,7,8, 9, 10], columns=['tweet_id', 'tweet_parent', 'tweet_fils'])
def transtype(L):
    if L=='[]':
        return []
    else :
        L2=L[1:-1]
        elts=L2.split(",")
        Liste=[]
        for i in elts :
            Liste.append(i)
        return Liste

db = pd.read_csv('ForumCarbone_treated.csv',encoding='latin-1')
for i in range(db.shape[0]):
    db.loc[i, 'Enfants']=transtype(db.loc[i, 'Enfants'])
print(db.at[2500,'Enfants'])
print(type(db.at[2500,'Enfants']))
print(type(transtype(db.at[2500,'Enfants'])))
if db.at[2500,'Enfants'].value==[]:
    print('A')
print(len(db[(db.Enfants==[])]))

