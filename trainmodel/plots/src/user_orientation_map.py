import datetime

import matplotlib.pyplot as plt
import numpy as np
from adjustText import adjust_text

from twitterapi.db.dao import User, Tweet

if __name__ == '__main__':
    starting_date = datetime.date(2019, 11, 18)
    delta = datetime.timedelta(days=14)

    for _ in range(5):
        ending_date = starting_date + delta
        date_string = '%d-%d-%d' % (starting_date.year, starting_date.month, starting_date.day)
        users_political_views = []
        users_sentiment = []
        usernames = []


        users = ['brexitparty_uk', 'Michael_Heaver', 'drdavidbull', 'Nigel_Farage', 'Daily_Express', 'LBC', 'jeremycorbyn',
                 'Conservatives', 'JackieDP', 'Mark_J_Harper', 'piersmorgan', 'CamillaTominey', 'StandUp4Brexit',
                 'BrexitCentral', 'RobertBuckland', 'SkyNews', 'RichardBurgon', 'CommonsJustice', 'bernardjenkin',
                 'eucopresident', 'JustinTrudeau', 'AWMurrison', 'darrengrimes_', 'MoggMentum', 'CarolineFlintMP',
                 'RupertLowe10', 'KateHoeyMP', 'johnredwood', 'MartinDaubney', 'ManfredWeber', 'bbcnews', 'BBCPolitics',
                 'TiceRichard', 'georgegalloway', 'LeaveEUOfficial', 'MelanieLatest', 'BorisJohnson', 'theresa_may',
                 'DominicRaab', 'spaceangel1964', 'UKLabour', 'Another_Europe', 'SteveBarclay', 'CatMcKinnell',
                 'Marcus4Nuneaton', 'Royston_Smith', 'benhowlettuk', 'CamillaTominey', 'Michael_Heaver', 'benhabib6',
                 'zatzi', 'MartinDaubney', 'SteveBakerHW', 'DavidDavisMP', 'Nikkipage44', 'KateHoeyMP', 'LanceForman',
                 'BrexitAlex', 'june_mummery', 'JkmMikke', ]

        # users = ['brexitparty_uk', 'Michael_Heaver', 'drdavidbull', 'Nigel_Farage', 'Daily_Express', 'LBC', 'jeremycorbyn',
        #          'Conservatives',]

        for user in users:
            try:
                user = User.select(User.id, User.username).where((User.username == user.lower()) | (User.username == user))[0]
            except IndexError:
                continue
            # noinspection PyComparisonWithNone
            tweets = \
                (Tweet
                 .select(Tweet.sentiment, Tweet.sentiment_confidence, Tweet.political_views_confidence, Tweet.political_views)
                 .where(Tweet.user == user, Tweet.sentiment != None, Tweet.timestamp > starting_date, Tweet.timestamp < ending_date)
                 )

            total_tweets = tweets.count()

            political_views = 0.0
            sentiment = 0.0

            for tweet in tweets:

                if tweet.sentiment == 'Positive':
                    sentiment += tweet.sentiment_confidence - 0.33
                elif tweet.sentiment == 'Negative':
                    sentiment -= tweet.sentiment_confidence - 0.33
                elif tweet.sentiment == 'Neutral':
                    pass
                else:
                    print(tweet.sentiment)
                    raise Exception("Invalid sentiment")

                if tweet.political_views == 'Democrat':
                    political_views += tweet.political_views_confidence - 0.5
                elif tweet.political_views == 'Republican':
                    political_views -= tweet.political_views_confidence - 0.5
                else:
                    raise Exception("Invalid political views")
            try:
                political_views /= total_tweets
                sentiment /= total_tweets
                users_political_views.append(political_views)
                users_sentiment.append(sentiment)
                usernames.append(user.username)
                if political_views < -0.5 or political_views > 0.4 or sentiment < -0.6 or sentiment > 0.2:
                    print('warning')
                print(user.username, ((political_views + 0.5) / 0.9), ((sentiment + 0.6) / 0.8))
            except ZeroDivisionError:
                pass

        colors = np.array([[max(min(1-((political_views + 0.5) / 0.9), 1), 0),
                            max(min(1-((users_sentiment[i] + 0.6) / 0.8), 1), 0),
                            max(min(((political_views + 0.5) / 0.9), 1), 0)]
                           for i, political_views in enumerate(users_political_views)])
        plt.scatter(users_sentiment, users_political_views, marker='o', c=colors, s=6)

        texts = []
        for i, username in enumerate(usernames):

            texts.append(plt.text(users_sentiment[i], users_political_views[i], username, ha='center', va='center', fontsize=4))
        adjust_text(texts)

        # Show the boundary between the regions:
        # plt.show()
        plt.ylim(-0.5, 0.4)
        plt.xlim(-0.6, 0.2)
        plt.xlabel('Sentiment positivity')
        plt.ylabel('Left wing tendency')
        plt.title('Political map of brexit activists in two weeks starting %s' % date_string)
        plt.savefig('political_map_%s.png' % date_string, dpi=600)
        plt.clf()
        starting_date = ending_date
