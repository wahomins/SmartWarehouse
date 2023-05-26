from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from pymongo import MongoClient
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
api = Api(app)

# MongoDB connection
mongodb_uri = os.getenv("MONGODB_URI")
app_port = os.getenv("PORT")
client = MongoClient(mongodb_uri)
db = client.get_default_database()

# Define routes and middleware here

if __name__ == '__main__':
    app.run(port=app_port)
