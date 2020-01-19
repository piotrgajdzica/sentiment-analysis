from trainmodel.political_views.views_tagger import ViewsTagger
from trainmodel.sentiment.sentiment_tagger import SentimentTagger
from twitterapi.db.dao import select_sample_tweets_no_sentiment_no_political_views, count_tweets_no_sentiment_no_political_views
from twitterapi.db.sentiment_helpers import tweet_prediction_bulk_update

if __name__ == '__main__':

    sentiment_classifier = SentimentTagger()
    political_classifier = ViewsTagger()

    all_tweets_count = count_tweets_no_sentiment_no_political_views()
    tweets = select_sample_tweets_no_sentiment_no_political_views()
    processed_tweets_counter = 0

    print('There are %s tweets to process.' % all_tweets_count)
    print('Starting...')

    while len(tweets) != 0:
        tweets_text = list(map(lambda tweet: tweet.text, tweets))
        result_sentiment = sentiment_classifier.predict(tweets_text)
        result_political_option = political_classifier.predict(tweets_text)

        for i, tweet in enumerate(tweets):
            tweet.sentiment = result_sentiment[i].value
            tweet.sentiment_confidence = result_sentiment[i].score
            tweet.political_views = result_political_option[i].value
            tweet.political_views_confidence = result_political_option[i].score

        tweet_prediction_bulk_update(tweets)
        processed_tweets_counter += len(tweets)
        print('%s/%s' % (processed_tweets_counter, all_tweets_count))
        tweets = select_sample_tweets_no_sentiment_no_political_views()

    print('All %s tweets processed.' % processed_tweets_counter)
