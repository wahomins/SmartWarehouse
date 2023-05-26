from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MongoDB connection details
mongodb_uri = os.getenv("MONGODB_URI")

# Define routes and middleware here

if __name__ == '__main__':
    app.run()
