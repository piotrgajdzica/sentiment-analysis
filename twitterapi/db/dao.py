import string

from peewee import *

import twitterapi.db.database_access as db

# db = SqliteDatabase('my_database.db')
db = MySQLDatabase(db.DATABASE, user=db.USER, password=db.PASSWORD,
                   host=db.HOST, port=db.PORT)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = BigIntegerField(primary_key=True)
    username = CharField()
    full_name = CharField(null=True)
    location = CharField(null=True)
    date_joined = DateField(null=True)
    followers = IntegerField(null=True)
    likes = IntegerField(null=True)
    lists = IntegerField(null=True)
    is_verified = BooleanField(null=True)


class Tweet(BaseModel):
    id = BigIntegerField(primary_key=True)
    user = ForeignKeyField(User, backref='tweets')
    text = TextField()
    url = CharField(max_length=1024, null=True)
    has_video = BooleanField()
    has_image = BooleanField()
    retweets = IntegerField()
    timestamp = DateTimeField()
    likes = IntegerField()
    is_retweet = BooleanField()
    retweeted_from_user = ForeignKeyField(User, backref='retweets', null=True)
    retweeted_from = ForeignKeyField('self', backref='retweets', null=True)
    quoted_from_user = ForeignKeyField(User, backref='quotes', null=True)
    quoted_from = ForeignKeyField('self', backref='quotes', null=True)


class UserMentions(BaseModel):
    tweet = ForeignKeyField(Tweet, on_delete='CASCADE', backref='usermentions')
    user = ForeignKeyField(User, on_delete='CASCADE', backref='usermentions')


class Url(BaseModel):
    tweet = ForeignKeyField(Tweet, on_delete='CASCADE', backref='urls')
    expanded_url = CharField(max_length=1024)


class Hashtag(BaseModel):
    text = CharField(max_length=1024)


class HashtagTweet(Model):
    hashtag = ForeignKeyField(Hashtag)
    tweet = ForeignKeyField(Tweet)


class UserNotFoundException(Exception):
    pass


def create_minimal_user_object(user_id, name):
    return User(
        id=int(user_id),
        username=name
    )


def create_tweet_object(tweet, user, retweeted_from_user):
    if not hasattr(tweet, 'has_video'):
        tweet.has_video = False
    if not hasattr(tweet, 'has_image'):
        tweet.has_image = False
    return Tweet(
        id=int(tweet.tweet_id),
        text=tweet.text,
        url=tweet.tweet_url,
        has_video=tweet.has_video,
        has_image=tweet.has_image,
        retweets=tweet.retweets,
        user=user,
        retweeted_from_user=retweeted_from_user,
        timestamp=tweet.timestamp,
        likes=tweet.likes,
        is_retweet=tweet.is_retweet,
    )


def add_bulk_tweets_and_users(tweets):

    users_to_insert = {}
    tweets_to_insert = {}

    for tweet in tweets:
        if tweet.is_retweet and tweet.retweeter_userid is not None and tweet.retweeter_username is not None:
            retweeted_from = create_minimal_user_object(tweet.retweet_id, tweet.retweeter_username)
            users_to_insert[tweet.retweeter_userid] = retweeted_from
        else:
            retweeted_from = None
        if tweet.user_id is not None and tweet.username is not None:
            user = create_minimal_user_object(tweet.user_id, tweet.username)
            users_to_insert[tweet.user_id] = user
            tweets_to_insert[tweet.tweet_id] = create_tweet_object(tweet, user, retweeted_from)
    User.bulk_create(users_to_insert.values(), 1000)
    Tweet.bulk_create(tweets_to_insert.values(), 1000)


def add_tweet(tweet):

    if not hasattr(tweet, 'has_video'):
        tweet.has_video = False
    if not hasattr(tweet, 'has_image'):
        tweet.has_image = False
    user = User.select().where(User.id == tweet.user_id).first()
    if user is None:
        raise UserNotFoundException
    return \
        Tweet.get_or_none(id=tweet.tweet_id) or Tweet.get_or_create(
            id=int(tweet.tweet_id),
            defaults={
                'text': tweet.text,
                'url': tweet.tweet_url,
                'has_video': tweet.has_video,
                'has_image': tweet.has_image,
                'retweets': tweet.retweets,
                'user': user,
                'timestamp': tweet.timestamp,
                'likes': tweet.likes,
                'is_retweet': tweet.is_retweet,
            }
        )


def add_user(user):
    if not hasattr(user, 'is_verified'):
        setattr(user, 'is_verified', False)

    return User.create(
        id=user.id,
        username=user.user,
        full_name=user.full_name,
        location=user.location,
        blog=user.blog,
        date_joined=user.date_joined,
        tweets=user.tweets,
        following=user.following,
        followers=user.followers,
        likes=user.likes,
        lists=user.lists,
        is_verified=True if user.is_verified == 1 else False
    )


def select_minimal_user_ids():
    return set([user.id for user in User.select(User.id).where(User.full_name==None)])


def select_minimal_users(ids):
    return set([user for user in User.select().where(User.full_name==None and User.id in ids)])


def select_all_users():
    return User.select()


def select_all_tweets():
    return Tweet.select()


def select_all_hashtags():
    return Hashtag.select()


def select_all_user_mentions():
    return UserMentions.select()


def select_all_urls():
    return Url.select()


def add_bulk_objects(users, tweets, hashtags, urls, mentions):
    user_ids = set([user.id for user in User.select(User.id)])
    users_to_insert = [user for user in users.values() if user.id not in user_ids]
    User.bulk_create(users_to_insert, 1000)

    minimal_users = select_minimal_users(users.keys())
    for user in minimal_users:
        user.full_name = users[user.id].full_name
        user.location = users[user.id].location
        user.date_joined = users[user.id].date_joined
        user.followers = users[user.id].followers
        user.likes = users[user.id].likes
        user.lists = users[user.id].lists
        user.is_verified = users[user.id].is_verified
    User.bulk_update(minimal_users, [
            User.full_name,
            User.location,
            User.date_joined,
            User.followers,
            User.likes,
            User.lists,
            User.is_verified,
        ], 1000)

    tweet_ids = set([tweet.id for tweet in Tweet.select(Tweet.id)])
    tweets_to_insert = [tweet for tweet in tweets.values() if tweet.id not in tweet_ids]
    original_tweets_ids = set([tweet.retweeted_from for tweet in tweets.values() if tweet.retweeted_from is not None] +
                              [tweet.quoted_from for tweet in tweets.values() if tweet.quoted_from is not None])
    original_tweets = [tweet for tweet in tweets.values() if tweet.id in original_tweets_ids and tweet.id not in
                       tweet_ids]

    tweets_to_insert = [tweet for tweet in tweets_to_insert if tweet.id not in original_tweets_ids]
    db.execute_sql("SET FOREIGN_KEY_CHECKS=0")
    Tweet.bulk_create(original_tweets, 1000)
    db.execute_sql("SET FOREIGN_KEY_CHECKS=1")

    for tweet in tweets_to_insert:
        if tweet.likes is None:
            print('zero likes')
            tweet.likes = 0

    Tweet.bulk_create(tweets_to_insert, 1000)

    hashtag_texts = set([hashtag.text for hashtag in Hashtag.select(Hashtag.text)])
    hashtags_to_insert = [hashtag for hashtag in hashtags.values() if hashtag.text not in hashtag_texts]
    Hashtag.bulk_create(hashtags_to_insert, 1000)

    Url.bulk_create(urls, 1000)

    new_users = list()
    user_ids = user_ids.union([user.id for user in users_to_insert])
    mentions_to_insert = []
    for user_mention in mentions:
        if user_mention.user not in user_ids:
            new_user = create_minimal_user_object(user_mention.user, user_mention.full_name)
            if any([letter in string.ascii_letters for letter in new_user.username]):
                new_users.append(new_user)
                user_ids.add(new_user.id)
                mentions_to_insert.append(user_mention)
    User.bulk_create(new_users, 1000)

    UserMentions.bulk_create(mentions_to_insert, 1000)
