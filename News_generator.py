import twint
import pandas
import pickle

def get_tweets(topics,user,date,RT):
    c = twint.Config()

    if user:
        c.Username = user
    if topics:
        c.Search = topics
    if date:
        c.Since = date

    c.Hide_output = True

    # c.Limit=100
    c.Pandas = True
    c.Native_retweets = RT
    twint.run.Search(c)
    Tweets_df = twint.storage.panda.Tweets_df
    Tweets_df.to_excel("HajimeIsayama_RT.xlsx") 
    Tweets_df.to_pickle('HajimeIsayama_RT.pkl')
    return Tweets_df

topics = ('ThankYouHajimeIsayama')
username = ''
date = ''#'2021-02-05'
df=get_tweets(topics,username,date,True)
#print(df['user_id'].head())
#print(df['user_id_str'].head())
# with open('confinement.pkl','rb') as f:
#         df_p = pickle.load(f)        
# print(df_p['user_id'].head())
# print(df_p['user_id_str'].head())


