from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import current_app
from cryptography.fernet import Fernet
from werkzeug.local import LocalProxy
import base64
import random
import string
from app.config import app_config


logger = LocalProxy(lambda: current_app.logger)

class DeviceModel:
    def __init__(self):
        # MongoDB connection
        mongodb_uri = app_config.MONGODB_URI
        mongodb_name = app_config.MONGODB_NAME
        client = MongoClient(mongodb_uri)
        self.db = client[mongodb_name]
        self.devices_collection = self.db['devices']
        # Encryption key
        encryption_key = app_config.ENCRYPTION_KEY

        self.fernet = Fernet(base64.urlsafe_b64decode(encryption_key))

    def create_device(self, device_data):
        # Generate a random secret for the device
        secret = self.generate_device_secret()
        device_data['secret'] = self.encrypt_device_secret(secret)
        

        # Create a new device in the MongoDB collection
        device_id = self.devices_collection.insert_one(device_data).inserted_id
        return device_id
    def update_device(self, device_id, data):
            # Update the device in the MongoDB collection and return the updated device
            filter = {"_id": ObjectId(device_id)}
            update = {"$set": data}
            updated_device = self.devices_collection.find_one_and_update(
                filter,
                update
            )
            return updated_device
    def delete_device(self, device_id):
        # Delete a device by its ID from the MongoDB collection
        result = self.devices_collection.delete_one({"_id": ObjectId(device_id)})
        return result.deleted_count

    def get_device_by_id(self, device_id):
        # Retrieve a device by its ID from the MongoDB collection
        device = self.devices_collection.find_one({"_id": ObjectId(device_id)})
        return device

    def get_device_by_id_and_secret(self, device_id, secret):
        # Retrieve a device by its ID and secret from the MongoDB collection
        device = self.devices_collection.find_one(
            {"_id": ObjectId(device_id)})
        if device:
            logger.debug(f'{secret} - device')
            device_data = self._decrypt_data(device)
            dbSec = device_data.get('secret')
            logger.debug(f'{dbSec} - device_data')

            if device_data.get('secret') == secret:
                return device_data
            else:
                return None
        else:
            return None

    def get_all_devices(self):
        # Retrieve all devices from the MongoDB collection
        devices = list(self.devices_collection.find())
        return devices

    def update_device_secret(self, device_id):
        # Generate a new secret for the device
        new_secret = self.generate_device_secret()
        encrypted = self.encrypt_device_secret(new_secret)
        # Update the device's secret in the MongoDB collection
        self.devices_collection.update_one(
            {"_id": ObjectId(device_id)},
            {"$set": {"secret": encrypted}}
        )

        return new_secret

    def generate_device_secret(self):
        # Generate a random device secret (6 characters)
        secret_characters = string.ascii_letters + string.digits
        secret = ''.join(random.choices(secret_characters, k=6))
        return secret

    def encrypt_device_secret(self, device_secret):
        return self.fernet.encrypt(device_secret.encode())

    def decrypt_device_secret(self, device_secret):
        return self.fernet.decrypt(device_secret.encode())
    
    def _decrypt_data(self, encrypted_user):
        # Decrypt the password and full name fields in the user data retrieved from MongoDB
        decrypted_data = encrypted_user.copy()

        if 'secret' in decrypted_data:
            encrypted = decrypted_data['secret']
            decrypted = self.fernet.decrypt(encrypted).decode()
            decrypted_data['secret'] = decrypted

        return decrypted_data