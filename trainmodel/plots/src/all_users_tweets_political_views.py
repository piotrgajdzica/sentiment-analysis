import matplotlib.pyplot as plt
from trainmodel.plots.src.plots_helper import tweet_to_dict_political_views
import pandas as pd
from twitterapi.db.dao import Tweet
import datetime

# M - month W - week D - day
grouping_interval = 'W'
starting_date = datetime.date(2019, 11, 18)

if __name__ == '__main__':
    tweets = list(Tweet.select().where(Tweet.timestamp > starting_date))
    tweets_df = pd.DataFrame.from_records([tweet_to_dict_political_views(tweet) for tweet in tweets]).set_index('timestamp')
    tweets_grouped_mean = tweets_df.resample(grouping_interval).mean().dropna()

    tweets_grouped_mean.plot(style='.-')
    plt.ylim(-1, 1)
    plt.xlabel('Time')
    plt.ylabel('Left wing tendency')
    plt.title('All tweets political views, all time (%s)' % grouping_interval)
    plt.axhline(0, color='black')
    plt.savefig('all_users_tweets_political_views_(%s).png' % grouping_interval)



