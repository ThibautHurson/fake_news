import pandas as pd
import numpy as np

import twint
import time



# Configure Tweet
config_t = twint.Config()
config_t.Search = "ForumZeroCarbone"
#config_t.Limit = 100 #par tranche de 20-30
config_t.Hide_output=True
config_t.Pandas = True
config_t.Native_retweets=False 


# Search for Tweet
twint.run.Search(config_t)
tweets_df = twint.storage.panda.Tweets_df
# print(tweets_df.shape)



# Configure Retweet
config_rt = twint.Config()
config_rt.Search = "ForumZeroCarbone"
#config_rt.Limit = 100 #par tranche de 5
config_rt.Hide_output=True
config_rt.Pandas = True
config_rt.Native_retweets=True #Filter the results for retweets only (warning: a few tweets will be returned!).
# Search for Retweet
twint.run.Search(config_rt)
retweets_df = twint.storage.panda.Tweets_df



#Je comprends pas la différence entre retweet_id et id



#Pseudo-code idea
# for each tweet in database:  #chope le user_rt_id pour chaque tweet
#     if parent_user_id in database: #Cherche cette id  dans la base des tweets
#       find parent_tweet among all parent_user_id tweets which has the same corps as tweet.
#       parent_tweet.append(tweet id)    
#       tweet.append(parent_tweet id)

#chope user_rt_id pour chopper tous les rtweeters