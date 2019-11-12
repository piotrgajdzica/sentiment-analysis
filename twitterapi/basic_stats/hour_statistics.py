
from twitterapi.db.dao import select_sample_tweets, select_all_tweets, Tweet, fn, User
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    tweets = select_sample_tweets()
    hour = fn.hour(Tweet.timestamp)
    res = (Tweet
        .select(hour.alias('hour'), fn.COUNT(Tweet.id).alias('count'), fn.COUNT(Tweet.user_id.distinct()).alias('user_count'))
        .group_by(hour)
        .order_by(hour)
           )

    print(res.count)

    hours = [str(row.hour)[-2:] for row in res]
    counts = [row.count for row in res]
    user_counts = [row.user_count for row in res]

    x = np.arange(len(hours))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, counts, width, label='Tweets')
    rects2 = ax.bar(x + width / 2, user_counts, width, label='Active users')
    # rects2 = ax.bar(x + width / 2, women_means, width, label='Women')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.set_xticks(x)
    ax.set_xticklabels(hours)
    ax.legend()

    plt.ylabel('Number of tweets/users')
    plt.xlabel('Hour in UTC')

    plt.title("Active users per day starting 22-10-2019")

    plt.legend()

    plt.show()
