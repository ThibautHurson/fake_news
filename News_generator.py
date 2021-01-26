import twint
import pandas
import pickle

def get_tweets(topics,user,keywords,language,RT):
    c = twint.Config()
    #c.Username = user
    #c.Custom["tweet"] = ["id", "username",]
    #c.Search = topic1,topic2
    c.Search=topics
    c.Hide_output=True
    # c.Since='2021-01-11'
    # c.Limit=100
    c.Pandas = True
    c.Native_retweets=RT
    twint.run.Search(c)
    Tweets_df = twint.storage.panda.Tweets_df
    Tweets_df.to_excel("colis_covid_RT.xlsx") 
    Tweets_df.to_pickle('colis_covid_RT.pkl')
    return Tweets_df

topics = ('colis','covid')
df=get_tweets(topics,'','','fr',True)
#print(df['user_id'].head())
#print(df['user_id_str'].head())
# with open('confinement.pkl','rb') as f:
#         df_p = pickle.load(f)        
# print(df_p['user_id'].head())
# print(df_p['user_id_str'].head())


