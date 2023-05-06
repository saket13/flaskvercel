import constants
import tweepy

class TwitterAPIHandler():

    def __init__(self):
        self.consumer_key = constants.TWITTER_CONSUMER_KEY
        self.consumer_secret = constants.TWITTER_CONSUMER_SECRET
        self.access_token = constants.TWITTER_ACCESS_TOKEN
        self.access_token_secret = constants.TWITTER_ACCESS_TOKEN_SECRET
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(self.auth)
    
    def search_tweets(self, keyword: str, no_of_tweets: int):
        return tweepy.Cursor(self.api.search_tweets, q=keyword).items(no_of_tweets)
    

