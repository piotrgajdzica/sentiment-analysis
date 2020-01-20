from twitterapi.db.dao import Tweet


def tweet_to_dict(tweet: Tweet):
    return {
        'timestamp': tweet.timestamp,
        'sentiment': 1 if tweet.sentiment == 'Positive' else 0 if tweet.sentiment == 'Neutral' else -1,
        'political_views': 1 if tweet.political_views == 'Republican' else -1
    }