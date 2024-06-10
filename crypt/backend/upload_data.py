import rss
import mongodb as mdb
import apis
import logging

# Error Handling
try:
    rekt_news_articles = rss.get_rekt_news_articles()
    crypto_news_articles = rss.get_crypto_news_articles()
    newscatcher_news_articles = apis.get_news_from_newscatcher()
    youtube_videos = apis.extract_youtube_videos()
except Exception as e:
    logging.error(f"Error fetching news articles: {e}")
    raise

# Logging
logging.basicConfig(level=logging.INFO)

# Code Reusability
def upload_articles_to_db(collection_name, article_data):
    if article_data:
        mdb.upload_to_mongodb(collection_name=collection_name, data=article_data)
    else:
        print(f"No new {collection_name} data can be found")

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

# Upload newscatcher news articles
upload_articles_to_db(
    collection_name="newscatcher_news",
    article_data=newscatcher_news_articles
)

# Upload youtube videos
upload_articles_to_db(
    collection_name="youtube_news",
    article_data=youtube_videos
)

