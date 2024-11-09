import os
import tweepy
import pandas as pd
from dotenv import load_dotenv
load_dotenv()


bearer_token = os.getenv('BEARER_TOKEN') 
client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)
search_query = "ref world cup -is:retweet -is:reply"
no_of_tweets = 100

try:
    tweets = client.search_recent_tweets(
        query=search_query,
        max_results=min(no_of_tweets, 100),  # max 100 per request in API v2
        tweet_fields=['created_at', 'public_metrics', 'source'],
        user_fields=['username'],
        expansions='author_id'
    )

    # Create a container for extracted tweet attributes
    attributes_container = []
    for tweet in tweets.data:
        # Pull relevant tweet details
        attributes_container.append([
            tweet.author_id,                     # User ID
            tweet.created_at,                    # Date Created
            tweet.public_metrics['like_count'],  # Number of Likes
            tweet.source,                        # Source of Tweet
            tweet.text                           # Tweet Text
        ])

    # Define column names
    columns = ["User ID", "Date Created", "Number of Likes", "Source of Tweet", "Tweet"]
    print(tweets.data)
    # Create DataFrame
    tweets_df = pd.DataFrame(attributes_container, columns=columns)
    
    # Save to CSV
    tweets_df.to_csv("tweets.csv", index=False)
    print("Tweets saved to tweets.csv")

    # Load and display the saved tweets
    loaded_tweets_df = pd.read_csv("tweets.csv")
    print(loaded_tweets_df)

except tweepy.TweepyException as e:
    print('Status Failed On:', str(e))
