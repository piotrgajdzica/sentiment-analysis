from twitterapi.db.dao import db, User, Tweet, UserMentions, Hashtag, Url, HashtagTweet


def run_migration():
    db.connect()
    db.create_tables([User, Tweet, UserMentions, Hashtag, Url, HashtagTweet])
    db.close()


def clear_database():
    db.connect()
    db.execute_sql("SET FOREIGN_KEY_CHECKS=0")
    db.drop_tables([User, Tweet, UserMentions, Hashtag, Url])
    db.create_tables([User, Tweet, UserMentions, Hashtag, Url])
    db.execute_sql("SET FOREIGN_KEY_CHECKS=1")
    db.close()


if __name__ == '__main__':
    run_migration()
    # clear_database()
