from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from pymongo import MongoClient
from flask_cors import CORS
from flask_talisman import Talisman
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
api = Api(app)

# Enable CORS for all routes
CORS(app)

# Add security headers with Flask-Talisman
# Talisman(app)

# ...
# MongoDB connection
mongodb_uri = os.getenv("MONGODB_URI")
app_port = os.getenv("PORT")
client = MongoClient(mongodb_uri)
db = client.get_default_database()

# Import the routes folder
from routes import *

# Register route blueprints with the Flask application
app.register_blueprint(user_bp)
app.register_blueprint(device_bp)

if __name__ == '__main__':
    app.run(port=app_port)