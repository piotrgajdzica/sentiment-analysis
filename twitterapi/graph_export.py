import datetime
import os
import re
import sys
import time

sys.path.append("/".join(os.path.realpath(__file__).split('/')[:-2]))

import twitterapi.db.dao as dao


date_start = datetime.datetime(2019, 10, 28)
date_end = date_start + datetime.timedelta(days=7)


user_id_to_username = {}


def strip_username(username):
    return re.sub(r'\W+', '', username)


def fill_usernames():
    global user_id_to_username
    user_id_to_username = {user.id: strip_username(user.username) for user in dao.select_all_users()}

def write_users_csv():
    users = open('data/users.csv', 'w', encoding='utf-8')
    lines = ['id;username\n']
    lines.extend(['{};{}\n'.format(user.id, strip_username(user.username))
                  for user in dao.select_all_users()])

    users.writelines(lines)
    users.close()


def write_hashtags_csv():
    hashtags = open('data/hashtags.csv', 'w', encoding='utf-8')
    lines = ['id;text\n']
    lines.extend(['{};#{}\n'.format(hashtag.id, hashtag.text)for hashtag in dao.select_all_hashtags()])

    hashtags.writelines(lines)
    hashtags.close()


def write_retweets_csv(start, end, limit):
    retweets = open(('data/%s%s/retweets.csv' % (start, end)).replace(' ', '_').replace(':', '_'), 'w', encoding='utf-8')
    lines = ['source;target;type;weight\n']
    lines.extend(['{};{};directed;{}\n'.format(user_id_to_username[retweet.user_id], user_id_to_username[retweet.retweeted_from_user_id], retweet.count)for retweet in
                  dao.select_retweets_edges(start, end, limit)])

    retweets.writelines(lines)
    retweets.close()


def write_quotes_csv(start, end, limit):
    quotes = open(('data/%s%s/quotes.csv' % (start, end)).replace(' ', '_').replace(':', '_'), 'w', encoding='utf-8')
    lines = ['source;target;type;weight\n']
    lines.extend(['{};{};directed;{}\n'.format(user_id_to_username[quote.user_id], user_id_to_username[quote.quoted_from_user_id], quote.count) for quote in
                  dao.select_quotes_edges(start, end, limit)])

    quotes.writelines(lines)
    quotes.close()


def write_mentions_csv(start, end, limit):
    mentions = open(('data/%s%s/mentions.csv' % (start, end)).replace(' ', '_').replace(':', '_'), 'w', encoding='utf-8')
    lines = ['source;target;type;weight\n']
    lines.extend(['{};{};directed;{}\n'.format(user_id_to_username[mention.user_id], user_id_to_username[mention.tweet.user_id], mention.count)for mention in
                  dao.select_mentions_edges(start, end, limit)])

    mentions.writelines(lines)
    mentions.close()


def write_hashtag_users_csv(start, end, limit):
    hashtag_users = open(('data/%s%s/hashtag_users.csv' % (start, end)).replace(' ', '_').replace(':', '_'), 'w', encoding='utf-8')
    lines = ['source;target;type;weight\n']
    lines.extend(['{};{};directed;{}\n'.format(user_id_to_username[hashtag.tweet.user_id], hashtag.hashtag, hashtag.count) for hashtag in
                  dao.select_hashtags_edges(start, end, limit)])

    hashtag_users.writelines(lines)
    hashtag_users.close()


if __name__ == '__main__':

    limit = 10
    start = time.time()
    write_hashtags_csv()
    print(time.time() - start)
    start = time.time()
    write_users_csv()
    print(time.time() - start)
    fill_usernames()
    while date_end < datetime.datetime(2019, 12, 3):
        try:
            os.makedirs(('data/%s%s/' % (date_start, date_end)).replace(' ', '_').replace(':', '_'))
        except FileExistsError:
            pass
        start = time.time()
        write_hashtag_users_csv(date_start, date_end, limit)
        print(time.time() - start)
        start = time.time()
        write_mentions_csv(date_start, date_end, limit)
        print(time.time() - start)
        start = time.time()
        write_quotes_csv(date_start, date_end, limit)
        print(time.time() - start)
        start = time.time()
        write_retweets_csv(date_start, date_end, limit)
        print(time.time() - start)
        date_start = date_end
        date_end = date_end + datetime.timedelta(days=7)
