from trainmodel.political_views.views_tagger import ViewsTagger
from trainmodel.sentiment.sentiment_tagger import SentimentTagger
from twitterapi.db.dao import select_sample_tweets_no_sentiment_no_political_views, count_tweets_no_sentiment_no_political_views
from twitterapi.db.sentiment_helpers import tweet_prediction_bulk_update
import time

if __name__ == '__main__':

    sentiment_classifier = SentimentTagger()
    political_classifier = ViewsTagger()
    n = 100
    processed_tweets_counter = 0

    all_tweets_count = count_tweets_no_sentiment_no_political_views()

    start = time.time()
    tweets = select_sample_tweets_no_sentiment_no_political_views(n)
    end = time.time()
    print('Read first %s tweets time: %s' % (n, (end - start)))

    print('There are %s tweets to process.' % all_tweets_count)
    print('Starting...')

    while len(tweets) != 0:
        tweets_text = list(map(lambda tweet: tweet.text, tweets))

        start = time.time()
        result_sentiment = sentiment_classifier.predict(tweets_text)
        result_political_option = political_classifier.predict(tweets_text)
        end = time.time()
        print('Predict %s tweets time: %s' % (n, (end - start)))

        for i, tweet in enumerate(tweets):
            tweet.sentiment = result_sentiment[i].value
            tweet.sentiment_confidence = result_sentiment[i].score
            tweet.political_views = result_political_option[i].value
            tweet.political_views_confidence = result_political_option[i].score

        start = time.time()
        tweet_prediction_bulk_update(tweets)
        end = time.time()
        print('Save %s tweets time: %s' % (n, (end - start)))

        processed_tweets_counter += n
        print('%s/%s' % (processed_tweets_counter, all_tweets_count))

        start = time.time()
        tweets = select_sample_tweets_no_sentiment_no_political_views()
        end = time.time()
        print('Read next %s tweets time: %s' % (n, (end - start)))

    print('All %s tweets processed.' % processed_tweets_counter)
