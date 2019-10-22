import datetime as dt
import time

from twitterscraper import query_tweets, Tweet
from typing import List

from twitterapi.db.dao import add_bulk_tweets_and_users


def report_time(start, operation_name):
    end = time.time()
    print(operation_name + ' took ' + str(end - start) + ' seconds')
    return end


def get_tweets(start=dt.date(2010, 1, 1), end=dt.date.today(), query='brexit'):
    tweets = query_tweets(query, begindate=start, enddate=end, limit=100000, poolsize=20)  # type: List[Tweet]

    start = report_time(time.time(), 'downloading tweets')
    print(len(tweets))
    add_bulk_tweets_and_users(tweets)
    start = report_time(start, 'inserting tweets')


if __name__ == '__main__':
    get_tweets(start=dt.date(2019, 10, 1 ))