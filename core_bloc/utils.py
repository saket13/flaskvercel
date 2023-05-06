import constants

from api_integrations.twitter.public import TwitterAPIHandler
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob


def percentage(part,whole):
    return 100 * float(part)/float(whole)

class TwitterSentimentAnalyzer():

    def __init__(self, keyword):
        self.keyword = keyword
        self.no_of_tweets = constants.DEFAULT_NO_OF_TWEETS
        self.positive, self.negative, self.neutral, self.polarity = 0, 0, 0, 0
        self.tweet_list, self.neutral_list, self.negative_list, self.positive_list = [], [], [], []

    def get_scores(self):
        twitter_api_handler = TwitterAPIHandler()
        tweets = twitter_api_handler.search_tweets(self.keyword, self.no_of_tweets)
        for tweet in tweets:
            self.tweet_list.append(tweet.text)
            analysis = TextBlob(tweet.text)
            score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
            neg = score['neg']
            neu = score['neu']
            pos = score['pos']
            comp = score['compound']
            self.polarity += analysis.sentiment.polarity
            if neg > pos:
                self.negative_list.append(tweet.text)
                self.negative += 1
            elif pos > neg:
                self.positive_list.append(tweet.text)
                self.positive += 1
            elif pos == neg:
                self.neutral_list.append(tweet.text)
                self.neutral += 1
        self.positive = percentage(self.positive, self.no_of_tweets)
        self.negative = percentage(self.negative, self.no_of_tweets)
        self.neutral = percentage(self.neutral , self.no_of_tweets)
        self.polarity = percentage(self.polarity, self.no_of_tweets)
        self.positive = format(self.positive, '.1f')
        self.negative = format(self.negative, '.1f')
        self.neutral = format(self.neutral, '.1f')
        return self.positive, self.negative, self.neutral