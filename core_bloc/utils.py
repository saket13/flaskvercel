import constants

from api_integrations.twitter.public import TwitterAPIHandler
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob


def percentage(part,whole):
    return 100 * float(part)/float(whole)

class TwitterSentimentAnalyzer():

    def __init__(self, keyword):
        self.keyword = keyword
        self.positive, self.negative, self.neutral, self.polarity, self.no_of_tweets = 0, 0, 0, 0, 0
        self.tweet_list, self.neutral_list, self.negative_list, self.positive_list = [], [], [], []

    def get_scores(self):
        twitter_api_handler = TwitterAPIHandler()
        tweets = twitter_api_handler.search_tweets(keyword=self.keyword, days=2)
        for tweet in tweets:
            self.no_of_tweets += 1
            self.tweet_list.append(tweet)
            analysis = TextBlob(tweet)
            score = SentimentIntensityAnalyzer().polarity_scores(tweet)
            neg = score['neg']
            neu = score['neu']
            pos = score['pos']
            comp = score['compound']
            self.polarity += analysis.sentiment.polarity
            if neg > pos:
                self.negative_list.append(tweet)
                self.negative += 1
            elif pos > neg:
                self.positive_list.append(tweet)
                self.positive += 1
            elif pos == neg:
                self.neutral_list.append(tweet)
                self.neutral += 1
        self.positive = percentage(self.positive, self.no_of_tweets)
        self.negative = percentage(self.negative, self.no_of_tweets)
        self.neutral = percentage(self.neutral , self.no_of_tweets)
        self.polarity = percentage(self.polarity, self.no_of_tweets)
        self.positive = format(self.positive, '.1f')
        self.negative = format(self.negative, '.1f')
        self.neutral = format(self.neutral, '.1f')
        return self.positive, self.negative, self.neutral, self.no_of_tweets