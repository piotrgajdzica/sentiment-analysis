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
    username = CharField(unique=True)
    full_name = CharField(null=True)
    location = CharField(null=True)
    blog = CharField(null=True)
    date_joined = DateField(null=True)
    tweets = IntegerField(null=True)
    following = IntegerField(null=True)
    followers = IntegerField(null=True)
    likes = IntegerField(null=True)
    lists = IntegerField(null=True)
    is_verified = BooleanField(null=True)


class Tweet(BaseModel):
    id = BigIntegerField(primary_key=True)
    user = ForeignKeyField(User, backref='tweets')
    text = TextField()
    url = CharField(max_length=1024)
    has_video = BooleanField()
    has_image = BooleanField()
    retweets = IntegerField()
    timestamp = DateTimeField()
    replies = IntegerField()
    likes = IntegerField()
    is_retweet = BooleanField()
    retweeted_from_user = ForeignKeyField(User, backref='retweets', null=True)
    retweeted_from = ForeignKeyField('self', backref='retweets', null=True)


class UserMentions(BaseModel):
    tweet = ForeignKeyField(Tweet, on_delete='CASCADE', backref='usermentions')
    user = ForeignKeyField(User, on_delete='CASCADE', backref='usermentions')


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
        replies=tweet.replies,
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
                'replies': tweet.replies,
                'likes': tweet.likes,
                'is_retweet': tweet.is_retweet,
                # retweeted_from=Tweet.select().where(Tweet.id == tweet.retweet_id) if len(tweet.retweet_id) > 0 else None,
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


def select_all_users():
    return User.select()


def select_all_tweets():
    return Tweet.select()
