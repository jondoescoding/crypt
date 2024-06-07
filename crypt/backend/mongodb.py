# MongoDB
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Imports for the environmental variables
from dotenv import load_dotenv
import os

# Requests
import requests


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

def upload_to_mongodb(collection_name: str, data):
    mongodb_collection = db[collection_name]