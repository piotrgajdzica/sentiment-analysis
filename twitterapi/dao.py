import sqlite3
from sqlite3 import Error

sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        user text,
                                        full_name text,
                                        location text,
                                        blog text,
                                        date_joined text,
                                        tweets integer,
                                        following integer,
                                        followers integer,
                                        likes integer,
                                        lists integer,
                                        is_verified integer
                                    );"""

sql_create_tweets_table = """CREATE TABLE IF NOT EXISTS tweets (
                                    tweet_id integer PRIMARY KEY,
                                    text text,
                                    tweet_url text,
                                    has_video integer,
                                    has_image integer,
                                    retweets integer,
                                    user_id integer,
                                    timestamp text,
                                    timestamp_epochs integer,
                                    replies integer,
                                    likes integer,
                                    is_retweet integer,
                                    retweet_id integer,
                                    retweeter_userid integer,
                                    retweeter_username text,
                                    FOREIGN KEY (user_id) REFERENCES users (id),
                                    FOREIGN KEY (retweet_id) REFERENCES tweets (tweet_id),
                                    FOREIGN KEY (retweeter_userid) REFERENCES users (id)
                                );"""


def create_connection(db_file):
    """ create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print e
    return conn


def __create_table__(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def __drop_tables__(conn):
    try:
        c = conn.cursor()
        c.execute("""DROP TABLE users;""")
        c.execute("""DROP TABLE tweets;""")
    except Error as e:
        print(e)


def __create_user__(conn, user):
    """
    Create a new user
    :param conn:
    :param user:
    :return:
    """
    sql = ''' INSERT INTO users(id,
                                user,
                                full_name,
                                location,
                                blog,
                                date_joined,
                                tweets,
                                following,
                                followers,
                                likes,
                                lists,
                                is_verified)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid


def __create_tweet__(conn, tweet):
    """
    Create a new tweet
    :param conn:
    :param tweet:
    :return:
    """
    sql = ''' INSERT INTO tweets(tweet_id,
                                text,
                                tweet_url,
                                has_video,
                                has_image,
                                retweets,
                                user_id,
                                timestamp,
                                timestamp_epochs,
                                replies,
                                retweets,
                                likes,
                                is_retweet,
                                retweet_id,
                                retweeter_userid,
                                retweeter_username)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, tweet)
    return cur.lastrowid


def create_tables_if_not_exist(conn):
    __create_table__(conn, sql_create_users_table)
    __create_table__(conn, sql_create_tweets_table)


def add_tweet(conn, tweet):
    """
    Add Tweet object to database
    :param conn:
    :param tweet:
    :return:
    """
    if not hasattr(tweet, 'has_video'):
        tweet.has_video = None
    if not hasattr(tweet, 'has_image'):
        tweet.has_image = None

    try:
        __create_tweet__(conn, [tweet.tweet_id, tweet.text, tweet.tweet_url, tweet.has_video, tweet.has_image, tweet.retweets,
                              tweet.user_id, tweet.timestamp, tweet.timestamp_epochs, tweet.replies, tweet.retweets,
                              tweet.likes, tweet.is_retweet, tweet.retweet_id, tweet.retweeter_userid,
                              tweet.retweeter_username])
    except sqlite3.IntegrityError as e:
        print "{}, id = {}".format(e, tweet.tweet_id)


def add_user(conn, user):
    """
    Add User object to database
    :param conn:
    :param user:
    :return:
    """
    try:
        __create_user__(conn, [user.id, user.user, user.full_name, user.location, user.blog, user.date_joined, user.tweets,
                             user.following, user.followers, user.likes, user.lists, user.is_verified])
    except sqlite3.IntegrityError as e:
        print "{}, id = {}".format(e, user.id)


def select_all_users(conn):
    """
    :param conn: the Connection object
    :return: users list
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")

    return cur.fetchall()


def select_all_tweets(conn):
    """
    :param conn: the Connection object
    :return: tweets list
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tweets")

    return cur.fetchall()
