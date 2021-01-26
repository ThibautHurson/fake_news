import pandas as pd
import numpy as np
import twint
import tweepy 
import time
import collections

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

def find_parents3(db):
    consumer_key = "6ljnnBOMpNjmKGHh0DpoczkMC" 
    consumer_secret = "NDafWcimWv9AF2Aul8yQKVwcmSROmVc8D9wFEjNHGV2VdcXoPb" 
    access_token = "1322253203296210945-HVnEkHfqdKtlX9TADHUZBHSWQvZWpP" 
    access_token_secret = "bBmEzaEJcmwB94WRpprR1UqKqDdeGdYY1zekr2WjjTpKC" 
      
    # authorization of consumer key and consumer secret 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
      
    # set access to user's access key and access secret  
    auth.set_access_token(access_token, access_token_secret) 
      
    # calling the api  
    api = tweepy.API(auth, wait_on_rate_limit=True)


    parents=np.zeros((db.shape[0],1))
    enfants=[[] for i in range(db.shape[0])]


    db_tweet_retweeted = db[(db['retweet'] == False) & (db['nretweets'] > 0)] 
    db_retweet = db[db['retweet'] == True]

    # unique_user_rt_id = db_retweet.user_rt_id[pd.unique(db['user_rt_id'])]

    for i, row in db_tweet_retweeted.iterrows():
        parent_tweet_id = row['id'] #tweet id

        #We create a df of this "father"'s retweeters. Note: It takes into account this person plublished tweet that are in 
        #this database. (i.e can be retweeters from different tweets)
        df_this_tweet_retweeters  = db_retweet[db_retweet['retweet_id'] == parent_tweet_id]


        if df_this_tweet_retweeters.empty: #Retweeters of this tweet are not in the dataset
            parents[i] = -1
        else:
            #Retweeters of this tweet are in the dataset.
            #We assume that if a1 and a2 retweeted a0, than a2 is a child of a1 iff a1 retweeted the tweet earlier 
            #than a2 and if a2 follows a1 
            df_this_tweet_retweeters.sort_values(by=['day','hour'])

            current_parent_id = parent_tweet_id
            current_parent_idx = i
            queue_childs = collections.deque([(current_parent_idx,current_parent_id)])

            while not df_this_tweet_retweeters.empty:
                # print('df_rtwers')
                current_size = len(df_this_tweet_retweeters.index)
                print('df_this_tweet_retweeters size',current_size)
                print('queue_childs',len(queue_childs))
                if not queue_childs:
                    print('empty queue')
                #It means that there is no more parent-child relationship possible between retweeters
                #we assume every last retweeters to be the original tweeter's children
                    for idx, row_user in df_this_tweet_retweeters.iterrows():
                        parents[idx] = parent_tweet_id
                    break

                current_parent_idx, current_parent_id = queue_childs.popleft()

                for idx, row_user in df_this_tweet_retweeters.iterrows():
                    print(db[db.index == current_parent_idx].user_id.values[0])
                    print(row_user['user_id'])
                    status = api.show_friendship(source_id = db[db.index == current_parent_idx].user_id.values[0], target_id = row_user['user_id'])
                    print(status[1].following)
                    if status[1].following:
                        print('friend')
                        enfants[current_parent_idx].append(row_user['id'])
                        parents[idx] = current_parent_id

                        queue_childs.append((idx,row_user['id']))
                        df_this_tweet_retweeters.drop(index = idx,inplace = True)
                        print('------------------------\n')
                        print(enfants)


    return parents,enfants

        #Trier par le temps, puis par followers
        # for idx, row_retweeter in df_this_tweet_retweeters.iterrows():


        #On crée la liste des tweets postés par le père
        # tweets_parent_pot = db[(db.user_id == parent_user_id)]

        # #On veut retrouver le tweet original dans les différents tweets du père. Filtrage successifs
        # #1er filtre : nretweets>0, tweets postés à la même heure.
        # tweet_parent = tweets_parent_pot[(tweets_parent_pot.nretweets > 0) & (tweets_parent_pot.date == row['retweet_date'][0:19])]
        # if not tweet_parent.shape[0]: #If no match found using the 1st filter, than this tweet's parent is not in the DB 
        #     parents[i] = -1 #Not in database           
        # else:
        #     id_parent = comparaison_texte(tweet_parent,row['user_rt']) #2ème filtre : comparaison texte 
        #     parents[i] = id_parent #To associate the tweet parent id to the corresponding tweet children
        #     # enfants[db[db.id == id_parent].index.values[0]].append(int(row['id'])) #For each tweet parent we create the list of its tweet children
        # if row['id'] not in db_retweet['user_rt_id']:
        #     #As the tweet's retweets are not in the database, we give parents[i] the default -1 so that we do not take this tweet into account
        #     parents[i] = -1
        # else:
        #     #We want to find interconnections between one tweet's retweeters in order to find out who retweeted who
        #     db_retweeters = db_retweet[db_retweet['user_rt_id'] == row['id']]
        #     # for retweeter_idx, row_retweeter in db_retweeters.iterrows():
        #         #Trouve ceux qui follow l'originel et on les prend comme les mecs de bases. Puis en fonction du temps.



def get_followings(username):
    '''
    Input: username: name of the user
    Output: list of followers ids
    '''
    consumer_key = "6ljnnBOMpNjmKGHh0DpoczkMC" 
    consumer_secret = "NDafWcimWv9AF2Aul8yQKVwcmSROmVc8D9wFEjNHGV2VdcXoPb" 
    access_token = "1322253203296210945-HVnEkHfqdKtlX9TADHUZBHSWQvZWpP" 
    access_token_secret = "bBmEzaEJcmwB94WRpprR1UqKqDdeGdYY1zekr2WjjTpKC" 
      
    # authorization of consumer key and consumer secret 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
      
    # set access to user's access key and access secret  
    auth.set_access_token(access_token, access_token_secret) 
      
    # calling the api  
    api = tweepy.API(auth) 

    ids = []
    for page in tweepy.Cursor(api.followers_ids, screen_name=username).pages():
        ids.extend(page)
        time.sleep(60)

    # print len(ids)

    return ids

# print(get_followings('Pontsbschool'))

# print(ids)

  
