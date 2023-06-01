from pymongo import MongoClient
from app.config import app_config

# Connect to MongoDB
client = MongoClient(app_config.MONGODB_URI)
db = client[app_config.MONGODB_NAME]
collection = db["users"]

# Add a unique index to a field
collection.create_index("username", unique=True)
collection.create_index("email", unique=True)

# Close MongoDB connection
client.close()