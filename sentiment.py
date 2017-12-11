import os
from textblob import TextBlob
import tweepy
import numpy as np
import re

consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']
access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def searh_tweets(q):
    tweets = [tweet for tweet in tweepy.Cursor(api.search, q=q).items(1)]
    process_tweets(tweets)

def process_tweets(tweets):
    print(len(tweets),'Tweets')
    sentiments = {'pol': [], 'sub': []}
    translation_errors_count = 0
    for tweet in tweets:
        text = clean_tweet(tweet.text)
        blob = TextBlob(clean_tweet(text))
        sentiments['pol'].append(blob.sentiment.polarity)
        sentiments['sub'].append(blob.sentiment.subjectivity)
    print(sentiments)
    print('Ploarity', np.mean(sentiments['pol']))
    print('Subjectivity', np.mean(sentiments['sub']))

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
