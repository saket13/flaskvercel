import constants
import datetime
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
    
    def search_tweets(self, keyword: str, days: int):
        max_tweets = 400
        all_results, last_two_days_tweets = [], []

        today = datetime.date.today()
        days_ago = today - datetime.timedelta(days=days)
        today_string = today.strftime("%Y-%m-%d")
        days_ago_string = days_ago.strftime("%Y-%m-%d")
        tweets = tweepy.Cursor(self.api.search_tweets, q=keyword, lang="en", until=days_ago_string).items(1)
        two_days_ago_tweet = next(tweets)
        since_id = two_days_ago_tweet.id

        while len(all_results) < max_tweets:
            tweets = self.api.search_tweets(q=keyword, lang="en", since_id=since_id, until=today_string, count=100)
            if not tweets:
                break
            all_results.extend(tweets)
            since_id = tweets[-1].id - 1
            if len(all_results) >= max_tweets:
                break
        for tweet in all_results:
            if hasattr(tweet, 'full_text'):
                last_two_days_tweets.append(tweet.full_text)
            else:
                last_two_days_tweets.append(tweet.text)
        return last_two_days_tweets

