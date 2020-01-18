from trainmodel.political_views.views_tagger import ViewsTagger
from trainmodel.sentiment.sentiment_tagger import SentimentTagger


if __name__ == '__main__':
    political_classifier = ViewsTagger()
    sentiment_classifier = SentimentTagger()
    tweets = ["I am against abortion.", "I think women should decide"]
    result_political_option = political_classifier.predict(tweets)
    result_sentiment = sentiment_classifier.predict(tweets)
    print('First tweet: tag: %s, confidence: %f.2' % (result_political_option[0].value, result_political_option[0].score))
    print('Second tweet: tag: %s, confidence: %f.2' % (result_political_option[1].value, result_political_option[1].score))
    print('First tweet: tag: %s, confidence: %f.2' % (result_sentiment[0].value, result_sentiment[0].score))
    print('Second tweet: tag: %s, confidence: %f.2' % (result_sentiment[1].value, result_sentiment[1].score))
