import matplotlib.pyplot as plt

from trainmodel.plots.plots_helper import tweet_to_dict
from twitterapi.db.dao import select_all_tweets, select_sample_tweets
import pandas as pd

# M - month W - week D - day
grouping_interval = 'D'

if __name__ == '__main__':

    tweets = list(select_all_tweets())
    tweets_df = pd.DataFrame.from_records([tweet_to_dict(tweet) for tweet in tweets]).set_index('timestamp')

    del tweets_df['sentiment']
    tweets_grouped_mean = tweets_df.resample(grouping_interval).mean().dropna()

    tweets_grouped_mean.plot(style='.')
    plt.axhline(0, color='black')
    plt.savefig('all_users_tweets_political_views.png')
    plt.show()


