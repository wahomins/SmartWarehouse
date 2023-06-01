from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import random
import string

class DeviceModel:
    def __init__(self):
        # MongoDB connection
        mongodb_uri = os.getenv("MONGODB_URI")
        client = MongoClient(mongodb_uri)
        self.db = client.get_default_database()
        self.devices_collection = self.db['devices']

    def create_device(self, device_data):
        # Generate a random secret for the device
        device_data['secret'] = self._generate_device_secret()

        # Create a new device in the MongoDB collection
        device_id = self.devices_collection.insert_one(device_data).inserted_id
        return device_id

    def get_device_by_id(self, device_id):
        # Retrieve a device by its ID from the MongoDB collection
        device = self.devices_collection.find_one({"_id": ObjectId(device_id)})
        return device

    def get_all_devices(self):
        # Retrieve all devices from the MongoDB collection
        devices = list(self.devices_collection.find())
        return devices

    def update_device_secret(self, device_id):
        # Generate a new secret for the device
        new_secret = self._generate_device_secret()

        # Update the device's secret in the MongoDB collection
        self.devices_collection.update_one(
            {"_id": ObjectId(device_id)},
            {"$set": {"secret": new_secret}}
        )

        return new_secret

    def _generate_device_secret(self):
        # Generate a random device secret (6 characters)
        secret_characters = string.ascii_letters + string.digits
        secret = ''.join(random.choices(secret_characters, k=6))
        return secret
