import os
from core_bloc.utils import TwitterSentimentAnalyzer
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    args = request.args
    ticker = args.get('ticker')
    twitter_sentiment_analyzer = TwitterSentimentAnalyzer(ticker)
    positive, negative, neutral, total_count = twitter_sentiment_analyzer.get_scores()
    return jsonify({'positive': positive, 'negative': negative, 'neutral': neutral, 'total_count': total_count}), 200


if __name__ == '__main__':
    app.run()