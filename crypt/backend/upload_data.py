import rss
import mongodb as mdb
import logging

# Error Handling
try:
    rekt_news_articles = rss.get_rekt_news_articles()
    crypto_news_articles = rss.get_crypto_news_articles()
except Exception as e:
    logging.error(f"Error fetching news articles: {e}")
    raise

# Logging
logging.basicConfig(level=logging.INFO)

# Code Reusability
def upload_articles_to_db(collection_name, article_data):
    if article_data:
        mdb.upload_to_mongodb(collection_name=collection_name, article_data=article_data)
    else:
        print(f"No new {collection_name} articles")

# Upload rekt news articles
upload_articles_to_db(
    collection_name="rekt_news",
    article_data=rekt_news_articles
)

# Upload crypto news articles
upload_articles_to_db(
    collection_name="crypto_news", 
    article_data=crypto_news_articles
)
