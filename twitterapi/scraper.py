# from twitter_scraper import get_tweets
from twitterscraper import query_tweets, Tweet
from typing import List, Set, Dict, Tuple, Text, Optional

if __name__ == '__main__':

    # for tweet in get_tweets('borisjohnson', pages=1):
    #     print(tweet['text'])
    #     print(tweet)
    # list_of_tweets = query_tweets("Trump OR Clinton", 10)

    tweets = query_tweets("from:borisjohnson brexit :)", 10)  # type: List[Tweet]
    for tweet in tweets:
        print tweet.text, tweet.timestamp
