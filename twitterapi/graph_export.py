import datetime
import os
import sys
import time

sys.path.append("/".join(os.path.realpath(__file__).split('/')[:-1]))

import twitterapi.db.dao as dao


date_start = datetime.datetime(2019, 11, 1)
date_end = date_start + datetime.timedelta(days=7)


def write_users_csv():
    users = open('data/users.csv', 'w', encoding='utf-8')
    lines = ['id;username;full_name;location;date_joined;followers;likes;lists;is_verified\n']
    lines.extend(['{};{};{};{};{};{};{};{};{}\n'.format(user.id, user.username, user.full_name or "", user.location or "",
                                                        user.date_joined or "", user.followers or 0, user.likes or 0,
                                                        user.lists or 0, user.is_verified or False)
                  for user in dao.select_all_users()])

    users.writelines(lines)
    users.close()


def write_hashtags_csv():
    hashtags = open('data/hashtags.csv', 'w', encoding='utf-8')
    lines = ['id;text\n']
    lines.extend(['{};#{}\n'.format(hashtag.id, hashtag.text)for hashtag in dao.select_all_hashtags()])

    hashtags.writelines(lines)
    hashtags.close()


def write_retweets_csv(start, end):
    retweets = open(('data/%s%s/retweets.csv' % (start, end)).replace(' ', '_').replace(':', '_'), 'w', encoding='utf-8')
    lines = ['source;target;type;weight\n']
    lines.extend(['{};{};directed;{}\n'.format(retweet.user, retweet.retweeted_from_user, retweet.count)for retweet in dao.select_retweets_edges(start, end)])

    retweets.writelines(lines)
    retweets.close()


def write_quotes_csv(start, end):
    quotes = open(('data/%s%s/quotes.csv' % (start, end)).replace(' ', '_').replace(':', '_'), 'w', encoding='utf-8')
    lines = ['source;target;type;weight\n']
    lines.extend(['{};{};directed;{}\n'.format(quote.user, quote.quoted_from_user, quote.count) for quote in
                  dao.select_quotes_edges(start, end)])

    quotes.writelines(lines)
    quotes.close()


def write_mentions_csv(start, end):
    mentions = open(('data/%s%s/mentions.csv' % (start, end)).replace(' ', '_').replace(':', '_'), 'w', encoding='utf-8')
    lines = ['source;target;type;weight\n']
    lines.extend(['{};{};directed;{}\n'.format(mention.user, mention.tweet.user, mention.count)for mention in dao.select_mentions_edges(start, end)])

    mentions.writelines(lines)
    mentions.close()


def write_hashtag_users_csv(start, end):
    hashtag_users = open(('data/%s%s/hashtag_users.csv' % (start, end)).replace(' ', '_').replace(':', '_'), 'w', encoding='utf-8')
    lines = ['source;target;type;weight\n']
    lines.extend(['{};{};directed;{}\n'.format(hashtag.tweet.user, hashtag.hashtag, hashtag.count) for hashtag in
                  dao.select_hashtags_edges(start, end)])

    hashtag_users.writelines(lines)
    hashtag_users.close()


if __name__ == '__main__':
    try:
        os.makedirs(('data/%s%s/' % (date_start, date_end)).replace(' ', '_').replace(':', '_'))
    except FileExistsError:
        pass
    start = time.time()
    write_hashtag_users_csv(date_start, date_end)
    print(time.time() - start)
    start = time.time()
    write_hashtags_csv()
    print(time.time() - start)
    start = time.time()
    write_mentions_csv(date_start, date_end)
    print(time.time() - start)
    start = time.time()
    write_quotes_csv(date_start, date_end)
    print(time.time() - start)
    start = time.time()
    write_retweets_csv(date_start, date_end)
    print(time.time() - start)
    start = time.time()
    write_users_csv()
    print(time.time() - start)