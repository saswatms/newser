# curate_news.py
import feedparser
from pymongo import MongoClient
import datetime

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['news_db']
news_collection = db['news']


# Function to parse RSS feed and insert articles
def curate_news():
    rss_feed = feedparser.parse('rss_feed.xml')  # Update with your RSS feed path or URL
    articles = []
    for entry in rss_feed.entries:
        article = {
            'title': entry.title,
            'link': entry.link,
            'published': entry.published if 'published' in entry else str(datetime.datetime.now()),
            'summary': entry.summary,
            'source': rss_feed.feed.title
        }
        articles.append(article)

    if articles:
        news_collection.insert_many(articles)
        print(f'Inserted {len(articles)} new articles.')


if __name__ == '__main__':
    curate_news()
