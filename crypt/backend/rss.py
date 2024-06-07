import feedparser

def get_rekt_news_articles() -> list:
    rekt_news = 'https://rekt.news/rss/feed.xml'
    feed = feedparser.parse(url_file_stream_or_string=rekt_news)
    
    rekt_articles = [
        {
            'title': article.title,
            'publication_date': article.published,
            'summary': article.summary,
            'link': article.link,
            'image': [link['href'] for link in article.links if link.get('rel') == 'enclosure'][0] if any(link.get('rel') == 'enclosure' for link in article.links) else None
        } for article in feed.entries
    ]
    
    return rekt_articles


def get_crypto_news_articles():
    feed = feedparser.parse(url_file_stream_or_string='https://crypto.news/feed/')
    article_data = [
        {
            'title': article.title,
            'link': article.link,
            'author_detail': article.author_detail,
            'published': article.published,
            'tags': [tag['term'] for tag in article.tags],
            'id': article.id,
            'summary': article.summary,
            'media_thumbnail': article.media_thumbnail[0]['url'] if 'media_thumbnail' in article else None
        } for article in feed.entries
    ]
    return article_data
