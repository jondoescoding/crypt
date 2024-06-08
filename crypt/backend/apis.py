# Imports 
from datetime import datetime, timedelta
from pprint import pprint
from dotenv import load_dotenv
from newscatcherapi_client import Newscatcher, ApiException
import os

# Environmental Variables
load_dotenv('.env')

def get_news_from_newscatcher() -> list:
    """
    Retrieves news articles from the Newscatcher API.

    Returns:
        A list of news articles.

    Raises:
        None.
    """
    
    # Newscatcher API
    newscatcher = Newscatcher(api_key=os.getenv('NEWS_API'))
    try:
        response = newscatcher.search.get(q="DeFi, Cryptocurrency, NFTs",
            search_in="content, summary, title",
            lang="af,ar,bg,bn,ca,cs,cy,cn,da,de,el,en,es,et,fa,fi,fr,gu,he,hi,hr,hu,id,it,ja,kn,ko,lt,lv,mk,ml,mr,ne,nl,no,pa,pl,pt,ro,ru,sk,sl,so,sq,sv,sw,ta,te,th,tl,tr,tw,uk,ur,vi",
            sort_by="date", # most recent articles are grabbed first
            page=1,
            countries="AD, AE, AF, AG, AI, AL, AM, AO, AQ, AR, AS, AT, AU, AW, AX, AZ, BA, BB, BD, BE, BF, BG, BH, BI, BJ, BL, BM, BN, BO, BQ, BR, BS, BT, BV, BW, BY, BZ, CA, CC, CD, CF, CG, CH, CI, CK, CL, CM, CN, CO, CR, CU, CV, CW, CX, CY, CZ, DE, DJ, DK, DM, DO, DZ, EC, EE, EG, EH, ER, ES, ET, FI, FJ, FK, FM, FO, FR, GA, GB, GD, GE, GF, GG, GH, GI, GL, GM, GN, GP, GQ, GR, GS, GT, GU, GW, GY, HK",
            from_= (datetime.now() - timedelta(days=30)).strftime('%Y/%m/%d'), # changed the timeframe to 30 days from 182 days
            is_paid_content= False,
        )
        
        if response.status == "ok":
            newscatcher_articles = [
                {
                    "article_id": article['id'],
                    "title": article['title'],
                    "author": article['author'],
                    "authors": article['authors'],
                    "journalists": article['journalists'],
                    "published_date": article['published_date'],
                    "published_date_precision": article['published_date_precision'],
                    "updated_date": article['updated_date'],
                    "updated_date_precision": article['updated_date_precision'],
                    "link": article['link'],
                    "domain_url": article['domain_url'],
                    "full_domain_url": article['full_domain_url'],
                    "name_source": article['name_source'],
                    "is_headline": article['is_headline'],
                    "paid_content": article['paid_content'],
                    "parent_url": article['parent_url'],
                    "country": article['country'],
                    "rights": article['rights'],
                    "rank": article['rank'],
                    "media": article['media'],
                    "language": article['language'],
                    "description": article['description'],
                    "content": article['content'],
                    "word_count": article['word_count'],
                    "is_opinion": article['is_opinion'],
                    "twitter_account": article['twitter_account'],
                    "all_links": article['all_links'],
                    "all_domain_links": article['all_domain_links'],
                    "score": article['score']
                } for article in response.articles
            ]
            return newscatcher_articles
    except ApiException as e:
        print(f"Error: {e}")
        if e.status in [422, 403]:
            pprint(e.body)
    
    return []

