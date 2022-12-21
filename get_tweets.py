import tweepy
import config
import pandas as pd
import numpy as np

client = tweepy.Client(bearer_token = config.bearer_token)
query = 'FIFA2022 -is:retweet'

start_time = '2022-12-18T17:30:00Z'
end_time = '2022-12-18T18:30:00Z'

fields = ['id','tweet','date','source','likes','RTs','lang']
df = pd.DataFrame(columns = fields)

for tweet in tweepy.Paginator(
            client.search_recent_tweets, query=query,max_results = 10,
            start_time = start_time, end_time = end_time, 
            tweet_fields = ['created_at','lang','public_metrics']).flatten(limit = 10):
    if tweet.lang == 'en' or tweet.lang == 'es':
        df = df.append(
            pd.DataFrame([[tweet.id,tweet.text,tweet.created_at,tweet.source,
                        tweet.public_metrics['like_count'],tweet.public_metrics['retweet_count'],tweet.lang]],
                        columns = fields))

print(df.head())