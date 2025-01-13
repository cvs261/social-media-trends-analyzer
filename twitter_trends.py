import tweepy
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# Twitter API credentials
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_TOKEN_SECRET = "your_access_token_secret"

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Function to fetch tweets
def fetch_tweets(keyword, count=100):
    tweets = tweepy.Cursor(api.search_tweets, q=keyword, lang="en").items(count)
    tweet_data = []
    for tweet in tweets:
        tweet_data.append({
            "text": tweet.text,
            "created_at": tweet.created_at,
            "user": tweet.user.screen_name,
        })
    return pd.DataFrame(tweet_data)

# Function to analyze sentiment
def analyze_sentiment(df):
    def get_sentiment(text):
        analysis = TextBlob(text)
        if analysis.sentiment.polarity > 0:
            return "Positive"
        elif analysis.sentiment.polarity < 0:
            return "Negative"
        else:
            return "Neutral"
    df["sentiment"] = df["text"].apply(get_sentiment)
    return df

# Function to visualize trends
def visualize_sentiment(df):
    sentiment_counts = df["sentiment"].value_counts()
    sentiment_counts.plot(kind="bar", color=["green", "red", "blue"])
    plt.title("Sentiment Analysis")
    plt.xlabel("Sentiment")
    plt.ylabel("Tweet Count")
    plt.show()

if __name__ == "__main__":
    keyword = input("Enter a keyword or hashtag to analyze: ")
    tweet_count = int(input("How many tweets to analyze? "))
    
    print("Fetching tweets...")
    tweets_df = fetch_tweets(keyword, count=tweet_count)
    
    print("Analyzing sentiment...")
    tweets_df = analyze_sentiment(tweets_df)
    
    print(tweets_df.head())
    
    print("Visualizing results...")
    visualize_sentiment(tweets_df)
