import datetime
import os
import re
import sys
import time
import networkx as nx

sys.path.append("/".join(os.path.realpath(__file__).split('/')[:-2]))

import twitterapi.db.dao as dao


date_start = datetime.datetime(2019, 10, 28)
date_end = date_start + datetime.timedelta(days=7)


user_id_to_username = {}
hashtag_id_to_text = {}


def strip_username(username):
    return re.sub(r'\W+', '', username)


def fill_usernames():
    global user_id_to_username
    global hashtag_id_to_text
    user_id_to_username = {user.id: strip_username(user.username) for user in dao.select_all_users()}
    hashtag_id_to_text = {hashtag.id: hashtag.text for hashtag in dao.select_all_hashtags()}


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
    retweets = open('retweets.csv', 'w', encoding='utf-8')
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
    lines.extend(['{};{};directed;{}\n'.format(user_id_to_username[hashtag.tweet.user_id], hashtag_id_to_text[hashtag.hashtag_id], hashtag.count) for hashtag in
                  dao.select_hashtags_edges(start, end, limit)])

    hashtag_users.writelines(lines)
    hashtag_users.close()


def group_hashtag_users(start, end, limit):
    fill_usernames()
    hashtag_users = [(user_id_to_username[hashtag.tweet.user_id], hashtag_id_to_text[hashtag.hashtag_id]) for hashtag in
                     dao.select_hashtags_edges(start, end, limit)]
    G = nx.Graph()
    G.add_nodes_from([name for hashtag in hashtag_users for name in hashtag])
    G.add_edges_from([(hashtag[0], hashtag[1]) for hashtag in hashtag_users])
    communities = list()
    for i, community in enumerate(nx.algorithms.community.k_clique_communities(G, 2)):
        for name in community:
            communities.append((name, i))
    nodes = open('nodes.csv', 'w', encoding='utf-8')
    lines = ['id;community\n']
    lines.extend(['{};{}\n'.format(name[0], name[1]) for name in communities])
    nodes.writelines(lines)
    nodes.close()


def group_retweets(start, end, limit, k):
    fill_usernames()
    retweets = [(user_id_to_username[retweet.user_id], user_id_to_username[retweet.retweeted_from_user_id])for retweet in
                dao.select_retweets_edges(start, end, limit)]
    G = nx.Graph()
    G.add_nodes_from([name for retweet in retweets for name in retweet])
    G.add_edges_from([(retweet[0], retweet[1]) for retweet in retweets])
    communities = list()
    for i, community in enumerate(nx.algorithms.community.k_clique_communities(G, k)):
        for name in community:
            communities.append((name, i))
    nodes = open('nodes.csv', 'w', encoding='utf-8')
    lines = ['id;community\n']
    lines.extend(['{};{}\n'.format(name[0], name[1]) for name in communities])
    nodes.writelines(lines)
    nodes.close()


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
