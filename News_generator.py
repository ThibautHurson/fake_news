import twint
import pandas
import pickle

def get_tweets(topic1,topic2,user,keywords,language,RT):
    c = twint.Config()
    #c.Username = user
    #c.Custom["tweet"] = ["id", "username",]
    #c.Search = topic1,topic2
    c.Search=topic1
    c.Hide_output=True
    c.Since='2021-01-11'
    c.Limit=100
    c.Pandas = True
    #c.Native_retweets=RT
    twint.run.Search(c)
    Tweets_df = twint.storage.panda.Tweets_df
    Tweets_df.to_excel("test2.xlsx") 
    Tweets_df.to_pickle('testPickle.pkl')
    return Tweets_df

df=get_tweets('TDC2020','équipe','','','fr',True)
#print(df['user_id'].head())
#print(df['user_id_str'].head())
with open('testPickle.pkl','rb') as f:
        df_p = pickle.load(f)        
print(df_p['user_id'].head())
print(df_p['user_id_str'].head())


