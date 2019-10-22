from twitterapi.db.dao import db, User, Tweet


def run_migration():
    db.connect()
    db.create_tables([User, Tweet])
    db.close()


def clear_database():
    db.connect()
    db.drop_tables([User, Tweet])
    db.create_tables([User, Tweet])
    db.close()


if __name__ == '__main__':
    run_migration()
    # clear_database()
