from typing import List

from twitterapi.db.dao import Tweet


def set_tweet_sentiment(tweet: Tweet, value: str, confidence: float):
    tweet.sentiment = value
    tweet.sentiment_confidence = confidence
    tweet.save()


def set_tweet_political_views(tweet: Tweet, value: str, confidence: float):
    tweet.political_views = value
    tweet.political_views_confidence = confidence
    tweet.save()


def tweet_sentiment_bulk_update(tweets: List[Tweet]):
    Tweet.bulk_update(tweets, fields=[Tweet.sentiment, Tweet.sentiment_confidence])


def tweet_political_views_bulk_update(tweets: List[Tweet]):
    Tweet.bulk_update(tweets, fields=[Tweet.political_views, Tweet.political_views_confidence])


if __name__ == '__main__':
    pass
    # sample usage:
    # t1: Tweet
    # t2: Tweet
    # t1.sentiment = 'Negative'
    # t1.sentiment_confidence = 0.5
    # t2.sentiment = 'Negative'
    # t2.sentiment_confidence = 0.6
    # tweet_sentiment_bulk_update([t1,t2])
