
from twitterapi.db.dao import select_sample_tweets, select_all_tweets, Tweet, fn, User
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    tweets = select_sample_tweets()
    day = fn.date(Tweet.timestamp)
    res = (Tweet
        .select(day.alias('day'), fn.COUNT(Tweet.id).alias('count'), fn.COUNT(Tweet.user_id.distinct()).alias('user_count'))
        .where(day > '2019-10-21')
        .group_by(day)
        .order_by(day)
           )

    print(res.count)

    days = [str(row.day)[-2:] for row in res]
    counts = [row.count for row in res]
    user_counts = [row.user_count for row in res]



    x = np.arange(len(days))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, counts, width, label='Tweets')
    rects2 = ax.bar(x + width / 2, user_counts, width, label='Active users')
    # rects2 = ax.bar(x + width / 2, women_means, width, label='Women')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.set_xticks(x)
    ax.set_xticklabels(days)
    ax.legend()

    plt.ylabel('Number of tweets/users')
    plt.xlabel('Day of month')

    plt.title("Active users per day starting 22-10-2019")

    plt.legend()

    plt.show()