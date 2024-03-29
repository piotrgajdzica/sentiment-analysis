import json
import os
import sys
import traceback

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from twitterapi.db import dao
from twitterapi.twitter_api import query_api, fetch_from_cache


def pretty_print(d):
    print(json.dumps(d, indent=4, sort_keys=True))


def fetch_query(query):
    # users, tweets, hashtags, urls, mentions = query_api('brexit from:borisjohnson', max_pages=20)
    users, tweets, hashtags, urls, mentions = query_api(query, max_pages=100)
    print('stats for %s' % query)
    print('users', len(users))
    print('tweets', len(tweets))
    print('hashtags', len(hashtags))
    print('urls', len(urls))
    print('mentions', len(mentions))
    try:
        dao.add_bulk_objects(users, tweets, hashtags, urls, mentions)
    except Exception:
        traceback.print_exc()

def fetch_queries(queries):
    for query in queries:
        fetch_query(query)


def fetch_cache(dir):
    for file in os.listdir(dir):
        users, tweets, hashtags, urls, mentions = fetch_from_cache(os.path.join(dir, file))
        print('stats for %s' % file)
        print('users', len(users))
        print('tweets', len(tweets))
        print('hashtags', len(hashtags))
        print('urls', len(urls))
        print('mentions', len(mentions))
        try:
            dao.add_bulk_objects(users, tweets, hashtags, urls, mentions)
        except Exception:
            traceback.print_exc()


def main():
    hashtags = [
        'BritishIndependence',
        'Brexit',
        'WithdrawalAgreementBill',
        'BrexitVote',
        'GetBrexitDone',
        'letsgetbrexitdone',
        'BrexitDeal',
        'StandUp4Brexit',
        'BrexitBill',
        'TakeBackControl',
        'DemocracyBlockers',
        'NoDeal',
        'CleanBreakBrexit',
        'BREXITCAST',
        'VoteTheDealDown',
        'LeaveOct31st',
        'Resister',
        'StopBrexit',
        'SpentLonger',
        'SellOutDeal',
        'VoteDownTheDeal',
    ]
    hastag_queries = ['#%s' % hashtag for hashtag in hashtags]
    users = [
        'brexitparty_uk',
        'Michael_Heaver',
        'drdavidbull',
        'Nigel_Farage',
        'Daily_Express',
        'LBC',
        'jeremycorbyn',
        'Conservatives',
        'JackieDP',
        'Mark_J_Harper',
        'piersmorgan',
        'CamillaTominey',
        'StandUp4Brexit',
        'BrexitCentral',
        'RobertBuckland',
        'SkyNews',
        'RichardBurgon',
        'CommonsJustice',
        'bernardjenkin',
        'eucopresident',
        'JustinTrudeau',
        'AWMurrison',
        'darrengrimes_',
        'MoggMentum',
        'CarolineFlintMP',
        'RupertLowe10',
        'KateHoeyMP',
        'johnredwood',
        'MartinDaubney',
        'ManfredWeber',
        'bbcnews',
        'BBCPolitics',
        'TiceRichard',
        'georgegalloway',
        'LeaveEUOfficial',
        'MelanieLatest',
        'BorisJohnson',
        'theresa_may',
        'DominicRaab',
        'spaceangel1964',
        'UKLabour',
        'Another_Europe',
        'SteveBarclay',
        'CatMcKinnell',
        'Marcus4Nuneaton',
        'Royston_Smith',
        'benhowlettuk',
        'CamillaTominey',
        'Michael_Heaver',
        'benhabib6',
        'zatzi',
        'MartinDaubney',
        'SteveBakerHW',
        'DavidDavisMP',
        'Nikkipage44',
        'KateHoeyMP',
        'LanceForman',
        'BrexitAlex',
        'june_mummery',
        'JkmMikke',
    ]
    user_queries = ['brexit from:%s' % user for user in users]
    fetch_queries(hastag_queries)
    fetch_queries(user_queries)


if __name__ == '__main__':
    main()
    # fetch_cache('../cache')
