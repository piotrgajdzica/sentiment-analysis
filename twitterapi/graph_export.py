import twitterapi.db.dao as dao


def write_users_csv():
    users = open('users.csv', 'w', encoding='utf-8')
    lines = ['id;username;full_name;location;date_joined;followers;likes;lists;is_verified\n']
    lines.extend(['{};{};{};{};{};{};{};{};{}\n'.format(user.id, user.username, user.full_name or "", user.location or "",
                                                        user.date_joined or "", user.followers or 0, user.likes or 0,
                                                        user.lists or 0, user.is_verified or False)
                  for user in dao.select_all_users()])

    users.writelines(lines)
    users.close()


def write_hashtags_csv():
    hashtags = open('hashtags.csv', 'w', encoding='utf-8')
    lines = ['id;text\n']
    lines.extend(['{};#{}\n'.format(hashtag.id, hashtag.text)for hashtag in dao.select_all_hashtags()])

    hashtags.writelines(lines)
    hashtags.close()


def write_retweets_csv():
    retweets = open('retweets.csv', 'w', encoding='utf-8')
    lines = ['source;target;type;weight\n']
    lines.extend(['{};{};directed;{}\n'.format(retweet.user, retweet.retweeted_from_user, retweet.count)for retweet in dao.select_retweets_edges()])

    retweets.writelines(lines)
    retweets.close()


def write_quotes_csv():
    quotes = open('quotes.csv', 'w', encoding='utf-8')
    lines = ['source;target;type;weight\n']
    lines.extend(['{};{};directed;{}\n'.format(quote.user, quote.quoted_from_user, quote.count) for quote in
                  dao.select_quotes_edges()])

    quotes.writelines(lines)
    quotes.close()


def write_mentions_csv():
    mentions = open('mentions.csv', 'w', encoding='utf-8')
    lines = ['source;target;type;weight\n']
    lines.extend(['{};{};directed;{}\n'.format(mention.user, mention.tweet.user, mention.count)for mention in dao.select_mentions_edges()])

    mentions.writelines(lines)
    mentions.close()


def write_hashtag_users_csv():
    hashtag_users = open('hashtag_users.csv', 'w', encoding='utf-8')
    lines = ['source;target;type;weight\n']
    lines.extend(['{};{};directed;{}\n'.format(hashtag.tweet.user, hashtag.hashtag, hashtag.count) for hashtag in
                  dao.select_hashtags_edges()])

    hashtag_users.writelines(lines)
    hashtag_users.close()
