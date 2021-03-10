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
    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True,retry_count=10, retry_delay=5, retry_errors=set([503])) #Over capacity which Corresponds with HTTP 503. Twitter is temporarily over capacity


    parents=np.zeros((db.shape[0],1))
    enfants=[[] for i in range(db.shape[0])]


    db_tweet_retweeted = db[(db['retweet'] == False) & (db['nretweets'] > 0)] 
    db_retweet = db[db['retweet'] == True]

    # unique_user_rt_id = db_retweet.user_rt_id[pd.unique(db['user_rt_id'])]

    for i, row in db_tweet_retweeted.iterrows():
        print('row number',i)
        parent_tweet_id = row['id'] #tweet id

        #We create a df of this initial tweet retweets
        df_this_tweet_retweeters  = db_retweet[db_retweet['retweet_id'] == parent_tweet_id]


        if df_this_tweet_retweeters.empty: #Retweeters of this tweet are not in the dataset
            parents[i] = -1
        else:
            #Retweeters of this tweet are in the dataset.
            #We assume that if a1 and a2 retweeted a0, than a2 is a child of a1 iff a1 retweeted the tweet earlier 
            #than a2 and if a2 follows a1 
            df_this_tweet_retweeters.sort_values(by=['day','hour'])

            already_child = set([])

            current_parent_id = parent_tweet_id
            current_parent_idx = i

            while not df_this_tweet_retweeters.empty:
                current_size = len(df_this_tweet_retweeters.index)
                print('df_this_tweet_retweeters size',current_size)

                for idx, row_user in df_this_tweet_retweeters.iterrows():
                    #If the retweet is already the child of another retweet, we do not need to find its father anymore
                    if row_user['id'] not in already_child:
                        print(db[db.index == current_parent_idx].user_id.values[0])
                        # print(row_user['user_id'])
                        try:
                            status = api.show_friendship(source_id = db[db.index == current_parent_idx].user_id.values[0], target_id = row_user['user_id'])#show_friendship
                            # print(status[1].following)
                            if status[1].following:
                                print('friends')
                                enfants[current_parent_idx].append(row_user['id'])
                                parents[idx] = current_parent_id

                                already_child.add(row_user['id'])

                                # df_this_tweet_retweeters.drop(index = idx,inplace = True)
                                print('------------------------\n')
                                print(enfants)
                        except tweepy.error.TweepError as e:
                            if e == [{'code': 50, 'message': 'User not found.'}]: #User not found
                                continue
                            else:
                                try: #Handle potential connection error
                                    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True,retry_count=10, retry_delay=5, retry_errors=set([503]))
                                    
                                    status = api.show_friendship(source_id = db[db.index == current_parent_idx].user_id.values[0], target_id = row_user['user_id'])#show_friendship
                                    # print(status[1].following)
                                    if status[1].following:
                                        print('friends')
                                        enfants[current_parent_idx].append(row_user['id'])
                                        parents[idx] = current_parent_id

                                        already_child.add(row_user['id'])

                                        # df_this_tweet_retweeters.drop(index = idx,inplace = True)
                                        print('------------------------\n')
                                        print(enfants)
                                except tweepy.error.TweepError as er: #If it is not a connection error nor a 'user not found error' we just go to the next user
                                    print('unknow tweepy error passed: ', er)
                                    continue

                # followers = get_followings_from_id(db[db.index == current_parent_idx].user_id.values[0])
                # print(followers)
                # for follower_id in followers:
                #     #If the retweet is already the child of another retweet, we do not need to find its father anymore
                #     if follower_id not in already_child and follower_id in df_this_tweet_retweeters.user_id:
                #         print('friend', follower_id)
                #         enfants[current_parent_idx].append(follower_id)
                #         parents[idx] = current_parent_id

                #         already_child.add(follower_id)


                current_parent_id = df_this_tweet_retweeters.id.values[0]
                current_parent_idx = df_this_tweet_retweeters.index.values[0]

                #If it is not the first iteration
                if current_parent_idx != i:
                    #Drop the most recent retweeter
                    df_this_tweet_retweeters.drop(index = current_parent_idx,inplace = True)

    return parents,enfants


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
        time.sleep(20)

    # print len(ids)

    return ids

def get_followings_from_id(user_id):
    '''
    Input: username: name of the user
    Output: list of followers ids
    '''
    print('in get_following_from_id')
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
    for page in tweepy.Cursor(api.followers_ids, id=user_id).pages():
        print('go')
        ids.extend(page)
        time.sleep(60)

    # print len(ids)

    return ids

#print(get_followings('Pontsbschool'))

#print(ids)

  
