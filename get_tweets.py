import tweepy
import config
import pandas as pd
import numpy as np

client = tweepy.Client(bearer_token = config.bearer_token)

# define query
query = 'FIFA2022 -is:retweet'

# start time and end time
start_time = '2022-12-18T00:00:00Z'
end_time = '2022-12-19T00:00:00Z'

# output fields
fields = ['id','tweet','date','source','likes','RTs','lang']
df = pd.DataFrame(columns = fields)

# run paginated search to extract all tweet
for tweet in tweepy.Paginator(
            client.search_recent_tweets, query=query,max_results = 10,
            start_time = start_time, end_time = end_time, 
            tweet_fields = ['created_at','lang','public_metrics']).flatten(limit=10):
    # only parse english tweets
    if tweet.lang == 'en':
        df = df.append(
            pd.DataFrame([[tweet.id,tweet.text,tweet.created_at,tweet.source,
                        tweet.public_metrics['like_count'],tweet.public_metrics['retweet_count'],tweet.lang]],
                        columns = fields))
    
# write to parquet gzipped file
df.to_parquet('api_data/api_data.parquet.gzip',compression='gzip')