from twitterapi.db.dao import select_all_hashtags, select_all_tweets, select_sample_tweets, HashtagTweet

if __name__ == '__main__':
    tweets = select_all_tweets()
    hashtags = select_all_hashtags()
    to_insert = []
    for hashtag in hashtags:
        hashtag_text = '#%s' % hashtag.text
        for tweet in tweets:
            if hashtag_text in tweet.text:
                to_insert.append(HashtagTweet(tweet=tweet, hashtag=hashtag))
        print(hashtag_text)
    print(HashtagTweet.bulk_create(to_insert, 1000))
