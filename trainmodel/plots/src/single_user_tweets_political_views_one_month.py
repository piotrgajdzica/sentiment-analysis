import matplotlib.pyplot as plt
from trainmodel.plots.src.plots_helper import tweet_to_dict_political_views
import pandas as pd
from twitterapi.db.dao import User, Tweet
import datetime

# M - month W - week D - day
grouping_interval = 'D'
starting_date = datetime.date(2019, 11, 18)
ending_data = starting_date + datetime.timedelta(1*365/12)

users_names = ['_Max_Baring_', '_chancer_', '_FinancialWorld']

if __name__ == '__main__':

    for user_name in users_names:
        user = User.select(User.id, User.username).where((User.username == user_name.lower()) | (User.username == user_name))[0]

        tweets = list(Tweet.select().where(Tweet.timestamp > starting_date, Tweet.timestamp < ending_data, Tweet.user == user))
        tweets_df = pd.DataFrame.from_records([tweet_to_dict_political_views(tweet) for tweet in tweets]).set_index('timestamp')
        tweets_grouped_mean = tweets_df.resample(grouping_interval).mean().dropna()

        tweets_grouped_mean.plot(style='.-')
        plt.ylim(-1, 1)
        plt.xlabel('Time')
        plt.ylabel('Left wing tendency')
        plt.title('%s political views, one month (%s)' % (user_name, grouping_interval))
        plt.axhline(0, color='black')
        plt.savefig('%s_tweets_political_views_one_month_(%s).png' % (user_name, grouping_interval))
        plt.clf()