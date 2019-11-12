from peewee import fn
import matplotlib.pyplot as plt
import numpy as np
from twitterapi.db.dao import HashtagTweet, Hashtag

if __name__ == '__main__':

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


    query = (HashtagTweet
             .select(Hashtag.text.alias('text'), fn.COUNT(HashtagTweet.tweet).alias('count'))
             .join(Hashtag)
             .group_by(HashtagTweet.hashtag, Hashtag.text)
             .order_by(fn.COUNT(HashtagTweet.tweet))
            )
    print(query.count())

    query = [row for row in query if row.hashtag.text in hashtags]
    total_count = sum(row.count for row in query)
    other_count = sum(row.count for row in query if row.count < total_count * 0.02)
    query = [row for row in query if row.count >= total_count * 0.02]
    sizes = [hashtag.count for hashtag in query] + [other_count]
    labels = ['#' + hashtag.hashtag.text for hashtag in query] + ['Other']

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=-15)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Hashtag distribution\n Total hashtag occurences: %d\n' % total_count)

    plt.show()