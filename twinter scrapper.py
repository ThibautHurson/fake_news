import twint
import pandas

# Configure
c = twint.Config()
c.Search = "ForumZeroCarbone"
c.Hide_output=True
c.Limit=10
c.Pandas = True
#c.Native_retweets=True


# Run
twint.run.Search(c)

Tweets_df = twint.storage.panda.Tweets_df
Tweets_df.to_excel("16122020_Tweets.xlsx")

# Configure
d = twint.Config()
d.Search = "ForumZeroCarbone"
d.Hide_output=True
d.Pandas = True
c.Limit=10
d.Native_retweets=True


# Run
twint.run.Search(d)

RTweets_df = twint.storage.panda.Tweets_df
RTweets_df.to_excel("16122020_RT.xlsx") 