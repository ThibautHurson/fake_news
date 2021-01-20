import pandas as pd
import numpy as np

def letter_count(texte):
    a=texte.count('a')
    e=texte.count('e')
    o=texte.count('o')
    t=texte.count('t')
    r=texte.count('r')
    s=texte.count('s')
    return a,e,o,t,r,s

def comparaison_texte(database,texte_tweet):
    id_parent = -1
    for i in range(database.shape[0]):
        texte_parent_test = database.at[database.index[i],'tweet']
        if letter_count(texte_parent_test) == letter_count(texte_tweet):
            id_parent = int(database.at[database.index[i],'id'])
            break
    return id_parent

#Pseudo-code idea
# for each tweet in database:  #chope le user_rt_id pour chaque tweet
#     if parent_user_id in database: #Cherche cette id  dans la base des tweets
#       find parent_tweet among all parent_user_id tweets which has the same corps as tweet.
#       parent_tweet.append(tweet id)    
#       tweet.append(parent_tweet id)

#chope user_rt_id pour chopper tous les rtweeters
def find_parents2(db) :
    parents=np.zeros((db.shape[0],1))
    enfants=[[] for i in range(db.shape[0])]
    db_retweet = db[db['retweet'] == True]
    for i, row in db_retweet.iterrows():
        parent_user_id = int(row['user_rt_id'])
        #On crée la liste des tweets postés par le père
        tweets_parent_pot = db[(db.user_id == parent_user_id)]

        #On veut retrouver le tweet original dans les différents tweets du père. Filtrage successifs
        #1er filtre : nretweets>0, tweets postés à la même heure.
        tweet_parent = tweets_parent_pot[(tweets_parent_pot.nretweets > 0) & (tweets_parent_pot.date == row['retweet_date'][0:19])]
        if not tweet_parent.shape[0]: #If no match found using the 1st filter, than this tweet's parent is not in the DB 
            parents[i] = -1 #Not in DB           
        else:
            id_parent = comparaison_texte(tweet_parent,row['user_rt']) #2ème filtre : comparaison texte 
            parents[i] = id_parent #To associate the tweet parent id to the corresponding tweet children
            enfants[db[db.id == id_parent].index.values[0]].append(int(row['id'])) #For each tweet parent we create the list of its tweet children
    return parents,enfants