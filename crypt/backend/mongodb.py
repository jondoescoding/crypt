# MongoDB
from pymongo.errors import PyMongoError
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Imports for the environmental variables
from dotenv import load_dotenv
import os

# Environmental Variables
load_dotenv('.env')

# MongoDB
atlas_user = os.environ['ATLAS_USER']
atlas_pass = os.environ['ATLAS_PASS']

URI = f"mongodb+srv://{atlas_user}:{atlas_pass}@serverlessinstance1.2pjfhb1.mongodb.net/?retryWrites=true&w=majority&appName=ServerlessInstance1"

# Create a new client and connect to the server
client = MongoClient(URI, server_api=ServerApi('1'))
    
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Setting up the database
db = client['crypt']

def upload_to_mongodb(collection_name: str, article_data: list):
    """
    Uploads a list of article data to a specified MongoDB collection, avoiding duplicates based on article_id.

    Args:
        collection_name (str): The name of the MongoDB collection to upload to.
        article_data (list): A list of dictionaries, each containing article data with an 'article_id' field.

    Returns:
        None
    """
    mongodb_collection = db[collection_name]
    
    existing_article_ids = set(mongodb_collection.distinct("article_id"))
    
    print(f"DEBUG: Inserting articles into {collection_name}...")
    articles_to_insert = [article for article in article_data if article["article_id"] not in existing_article_ids]
    
    if articles_to_insert:
        try:
            mongodb_collection.insert_many(articles_to_insert)
            print(f"Inserted {len(articles_to_insert)} articles.")
        except PyMongoError as e:
            print(f"PyMongo error: {e}")
        except Exception as e:
            print(f"General error: {e}")
    else:
        print("No new articles to insert.")
