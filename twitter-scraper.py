import os
import tweepy
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

# Set up Twitter API v2 credentials
bearer_token = os.getenv('BEARER_TOKEN')

# Initialize Tweepy client for API v2
client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

# Define search query
search_query = "ref world cup -is:retweet -is:reply"

# Number of tweets to retrieve
no_of_tweets = 100

try:
    # Retrieve tweets using the search_recent_tweets endpoint in API v2
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

    # Create DataFrame
    tweets_df = pd.DataFrame(attributes_container, columns=columns)

    # Save to CSV
    tweets_df.to_csv("tweets.csv", index=False)
    print("Tweets saved to tweets.csv")

except tweepy.TweepyException as e:
    print('Status Failed On:', str(e))
