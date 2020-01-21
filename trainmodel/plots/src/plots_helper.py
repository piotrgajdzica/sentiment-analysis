from twitterapi.db.dao import Tweet


def tweet_to_dict_political_views(tweet: Tweet):
    return {
        'timestamp': tweet.timestamp,
        'political_views': 1 if tweet.political_views == 'Democrat' else -1
    }


def tweet_to_dict_sentiment(tweet: Tweet):
    return {
        'timestamp': tweet.timestamp,
        'sentiment': 1 if tweet.sentiment == 'Positive' else 0 if tweet.sentiment == 'Neutral' else -1
    }
