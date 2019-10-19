# from twitter_scraper import get_tweets
from twitterscraper import query_tweets, Tweet, User
from typing import List, Set, Dict, Tuple, Text, Optional
import dao


if __name__ == '__main__':

    # for tweet in get_tweets('borisjohnson', pages=1):
    #     print(tweet['text'])
    #     print(tweet)
    # list_of_tweets = query_tweets("Trump OR Clinton", 10)

    """
    conn = dao.create_connection("C:\sqlite\db\pythonsqlite.db")
    with conn:
        dao.create_tables_if_not_exist(conn)

        user = User()
        user.user = "aa"
        user.blog = "bb"
        user.location = "ba"
        user.id = 1
        user.followers = 2

        tweet = Tweet("a", "fullname", 1, 1, "url", "a", 1, 1, 1, 1, 1, "b", None, None, "pomocy", "<div>pomocy</div>")

        dao.add_user(conn, user)
        dao.add_tweet(conn, tweet)

        print dao.select_all_tweets(conn)
        print dao.select_all_users(conn)
    """

    tweets = query_tweets("from:borisjohnson brexit :)", 10)  # type: List[Tweet]
    for tweet in tweets:
        print tweet.text, tweet.timestamp
