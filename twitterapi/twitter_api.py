import json
import time

import requests
from twython import Twython


class User:

    def __init__(self, user_data):
        self.full_name = user_data['name']
        self.followers = user_data['followers_count']
        self.id = user_data['id']
        self.location = user_data['location']
        self.date_joined = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(user_data['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
        self.following = user_data['following']
        self.is_verified = user_data['verified']
        self.lists = user_data['listed_count']
        self.username = user_data['screen_name']
        self.likes = user_data['favourites_count']


class Tweet:
    user = None
    likes = None
    url = None
    has_image = False
    has_video = False
    quoted_from_user = None
    quoted_from = None
    retweeted_from_user = None
    retweeted_from = None

    def __init__(self, tweet_data):
        self.id = tweet_data['id']
        self.text = tweet_data['text']
        self.retweets = tweet_data['retweet_count']
        # self.timestamp = tweet_data['created_at']
        self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet_data['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
        self.likes = tweet_data['favorite_count']
        self.is_retweet = 'retweeted_status' in tweet_data.keys()
        self.is_quote = tweet_data['is_quote_status']


class Hashtag:
    def __init__(self, tweet_id, hashtag_data):
        self.text = hashtag_data['text']
        self.tweet = tweet_id


class Url:
    def __init__(self, tweet_id, url_data):
        self.expanded_url = url_data['expanded_url']
        self.tweet = tweet_id


class UserMentions:
    def __init__(self, tweet_id, user_mention_data):
        self.tweet = tweet_id
        self.user = user_mention_data['id']
        self.full_name = user_mention_data['name']
        self.username = user_mention_data['screen_name']


def query_api(query, max_pages=1):
    users = dict()
    tweets = dict()
    urls = list()
    hashtags = dict()
    mentions = list()
    cache = open('%s.txt' % query, 'w')
    APP_KEY = '3bW9nlsI1KFNGemyKABIExJvw'
    ACCESS_TOKEN = 'AAAAAAAAAAAAAAAAAAAAADBcAQEAAAAACmObvD8B4MwW4Bk%2B%2FvMcs75QuvA%3DV6QxfukBXCbsrDBykrZiNklTnjr2tY3A9AubSFDw1T19kh9OJY'

    twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
    api_url = 'https://api.twitter.com/1.1/search/tweets.json'
    # api_url = 'https://api.twitter.com/1.1/tweets/search/30day/production.json'
    constructed_url = twitter.construct_api_url(api_url, q=query, maxResults=1000)
    response = requests.get(constructed_url, headers={
        'Authorization': 'Bearer %s' % ACCESS_TOKEN
    })
    time.sleep(60)
    cache.write(json.dumps(response.json()))
    cache.write('\n')
    results = response.json()
    for result in results['statuses']:
        parse_tweet(result, users, tweets, hashtags, urls, mentions)

    search_metadata = results['search_metadata']
    if max_pages > 1:
        for _ in range(max_pages - 1):
            if 'next_results' not in search_metadata.keys():
                break

            constructed_url = api_url + search_metadata['next_results']
            time.sleep(60)
            response = requests.get(constructed_url, headers={
                'Authorization': 'Bearer %s' % ACCESS_TOKEN
            })

            cache.write(json.dumps(response.json()))
            cache.write('\n')
            results = response.json()
            search_metadata = results['search_metadata']

            for result in results['statuses']:
                parse_tweet(result, users, tweets, hashtags, urls, mentions)
    cache.close()
    return users, tweets, hashtags, urls, mentions


def fetch_from_cache(filename):
    users = dict()
    tweets = dict()
    urls = list()
    hashtags = dict()
    mentions = list()
    for line in open(filename).readlines():
        results = json.loads(line)
        for result in results['statuses']:
            parse_tweet(result, users, tweets, hashtags, urls, mentions)

    return users, tweets, hashtags, urls, mentions


def parse_tweet(tweet_data, users, tweets, hashtags, urls, mentions):
    user_data = tweet_data['user']
    user = User(user_data)
    users[user.id] = user

    tweet = Tweet(tweet_data)
    tweet.user = user.id
    entities = tweet_data['entities']
    if 'urls' in entities.keys():
        for url_data in entities['urls']:
            url = Url(tweet.id, url_data)
            urls.append(url)

    if 'hashtags' in entities.keys():
        for hashtag_data in entities['hashtags']:
            hashtag = Hashtag(tweet.id, hashtag_data)
            hashtags[hashtag.text] = hashtag

    if 'media' in entities.keys():
        for media_data in entities["media"]:
            if media_data['type'] == 'photo':
                tweet.has_image = True
            if media_data['type'] == 'video':
                tweet.has_video = True

    for user_mentions_data in entities['user_mentions']:
        user_mentions = UserMentions(tweet.id, user_mentions_data)
        mentions.append(user_mentions)

    if tweet.is_retweet:
        retweeted_status = tweet_data['retweeted_status']
        original = parse_tweet(retweeted_status, users, tweets, hashtags, urls, mentions)
        tweet.retweeted_from_user = original.user
        tweet.retweeted_from = original.id

    if tweet.is_quote:
        quoted_status = tweet_data.get('quoted_status', None)
        if quoted_status is not None:
            original = parse_tweet(quoted_status, users, tweets, hashtags, urls, mentions)
            tweet.quoted_from_user = original.user
            tweet.quoted_from = original.id
    tweets[tweet.id] = tweet
    return tweet
