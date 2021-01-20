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
    id_parent=-1
    for i in range(database.shape[0]):
        texte_parent_test = database.at[database.index[i],'tweet']
        letter_count(texte_tweet)
        if letter_count(texte_parent_test)==letter_count(texte_tweet):
            id_parent=int(database.at[database.index[i],'id'])
            return id_parent
    return id_parent

#Pseudo-code idea
# for each tweet in database:  #chope le user_rt_id pour chaque tweet
#     if parent_user_id in database: #Cherche cette id  dans la base des tweets
#       find parent_tweet among all parent_user_id tweets which has the same corps as tweet.
#       parent_tweet.append(tweet id)    
#       tweet.append(parent_tweet id)

#chope user_rt_id pour chopper tous les rtweeters

def find_parents(db) :
    parents=np.zeros((db.shape[0],1))
    enfants=[[] for i in range(db.shape[0])]
    for i in range(db.shape[0]) :
        #if db.at[i,'nretweets']==0:
            #enfants[i]=-1
        if db.at[i,'retweet'] :
            parent_user_id=int(db.at[i,'user_rt_id'])
            #On crée la liste des tweets postés par le père
            tweets_parent_pot=db[(db.user_id==parent_user_id)]
            #Levées d'exceptions : tweets not in DB
            if tweets_parent_pot.empty:
                parent_user_id=int(db.at[i,'user_rt_id'])+1
                tweets_parent_pot=db[(db.user_id==parent_user_id)]
                if tweets_parent_pot.empty:
                    parent_user_id=int(db.at[i,'user_rt_id'])-1
                    tweets_parent_pot=db[(db.user_id==parent_user_id)]
                    if tweets_parent_pot.empty:
                        parents[i]=-1 #Not in DB
                        continue

            # arg de db.at[i,'user_rt']==tweets_parents_pot[]

            #On veut retrouver le tweet original dans les différents tweets du père
            #On fait des filtrage successifs

            #1er filtre : nretweets>0, tweets postés à la même heure.
            tweet_parent=tweets_parent_pot[(tweets_parent_pot.nretweets>0)&(tweets_parent_pot.date==db.at[i,'retweet_date'][0:19])]
            
            
            if tweet_parent.shape[0]<1:
                parents[i]=-1 #Not in DB
                
            elif tweet_parent.shape[0]>1:
                
                #2ème filtre : comparaison texte 
                id_parent=comparaison_texte(tweet_parent,db.at[i,'user_rt'])
                parents[i]=id_parent
                #print(tweet_parent.id)
                enfants[db[db.id==int(tweet_parent.id.values[0])].index.values[0]].append(int(db.at[i,'id']))
                continue
            try :
                parents[i]=int(tweet_parent.id.values[0])
                enfants[db[db.id==int(tweet_parent.id)].index.values[0]].append(int(db.at[i,'id'])) #erreur ici
            except TypeError : #debugging
                print(i)
                #print(parent_user_id)
                #print(tweet_parent.head())
                print(tweet_parent.id)
                
                #print(db.at[i,'retweet_date'][0:19])
                print('hello')
                print(db[db.id==int(tweet_parent.id)].id.values[0])
                return
    retour=parents,enfants
    #print(retour)
    return retour

#parents=find_parents(db_tweet,db_retweet)
#print(parents)
