import math

from flask import Flask, jsonify, request
from pymongo import MongoClient
import feedparser
from bs4 import BeautifulSoup

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['news_aggregator']
news_collection = db['news']


@app.route('/fetch_news')
def fetch_news():
    rss_feeds = [
        'https://www.thehindu.com/news/feeder/default.rss',
        'https://www.moneycontrol.com/rss/MCtopnews.xml',
        'https://economictimes.indiatimes.com/rssfeedsdefault.cms',
        'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
        # Add more RSS feed URLs here
    ]

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            published = entry.published
            summary = BeautifulSoup(entry.summary, 'html.parser').get_text()

            news_article = {
                'title': title,
                'link': link,
                'published': published,
                'summary': summary,
                'source': feed.feed.title,
            }

            # Upsert the news article to avoid duplicates
            news_collection.update_one(
                {'link': link},
                {'$set': news_article},
                upsert=True
            )

    return jsonify({'message': 'News articles fetched and stored successfully.'})


@app.route('/get_news')
def get_news():
    articles = list(news_collection.find({}, {'_id': 0}))
    return jsonify(articles)


if __name__ == '__main__':
    app.run(debug=True)
