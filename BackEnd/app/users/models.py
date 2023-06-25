from pymongo import MongoClient, ASCENDING
from pymongo.errors import OperationFailure
from bson.binary import Binary
from bson.objectid import ObjectId
from werkzeug.local import LocalProxy
from flask import current_app
from cryptography.fernet import Fernet
import base64
from app.config import app_config
from .user_access_log import UserAccessLog
from app.devices.models import DeviceModel
from app.utils.utils import format_mongo_response

logger = LocalProxy(lambda: current_app.logger)
device_model = DeviceModel()

class UserModel:
    def __init__(self):
        # MongoDB connection
        mongodb_uri = app_config.MONGODB_URI
        mongodb_name = app_config.MONGODB_NAME
        client = MongoClient(mongodb_uri)
        self.db = client[mongodb_name]
        self.users_collection = self.db['users']

        # Encryption key
        encryption_key = app_config.ENCRYPTION_KEY
        # print(base64.urlsafe_b64decode(encryption_key), 'WW')
        # self.fernet = Fernet(base64.urlsafe_b64decode(encryption_key))
        self.fernet = Fernet(b'960WaV-GWbrJ2h-ZJK4UsF8K80--Id7MGXwcMwtiFKI=')
        
               # Create a unique index for name and warehouse_id
        try:
            self.users_collection.create_index([('email', ASCENDING)], unique=True)
            self.users_collection.create_index([('card_number', ASCENDING)], unique=True)
        except OperationFailure as e:
            logger.error(f"Failed to create unique index: {str(e)}")

    def create_user(self, user_data):
        # Encrypt password and full name before storing in MongoDB
        encrypted_user_data = self._encrypt_user_data(user_data)

        # Create a new user in the MongoDB collection
        user_id = self.users_collection.insert_one(encrypted_user_data).inserted_id
        return str(user_id)

    def update_user(self, user_id, updated_data):
        # Encrypt password and full name before storing in MongoDB
        encrypted_user_data = self._encrypt_user_data(updated_data)
        filter = {'_id': ObjectId(user_id)}
        update = {'$set': encrypted_user_data}
        encrypted_user = self.users_collection.find_one_and_update(
            filter, update, return_document=True)

        if encrypted_user:
            # Decrypt the user data before returning
            user_data = self._decrypt_user_data(encrypted_user)
            return user_data
        else:
            return None
        # return formart_mongo_response(result)

    def get_user_by_id(self, user_id):
        # Retrieve a user by their ID from the MongoDB collection
        encrypted_user = self.users_collection.find_one({"_id": ObjectId(user_id)})

        if encrypted_user:
            # Decrypt the user data before returning
            user_data = self._decrypt_user_data(encrypted_user)
            return user_data
        else:
            return None

    def get_user_by_id_card(self, user_id):
        # Retrieve a user by their ID or cardNumber
        try:
            if isinstance(user_id, ObjectId):
                query = {"_id": ObjectId(user_id)}
            else:
                query = {"card_number": user_id}

            encrypted_user = self.users_collection.find_one(query)

            if encrypted_user:
                # Decrypt the user data before returning
                user_data = self._decrypt_user_data(encrypted_user)
                return user_data
            else:
                return None
        except Exception as e:
            logger.error(f'Error fetching user:')
            logger.exception(e)
            
            return None
            


    def get_user_by_username(self, username_or_email):
        # Retrieve a user by their username or email from the MongoDB collection
        encrypted_user = self.users_collection.find_one(
            {"$or": [{"username": username_or_email}, {"email": username_or_email}]})

        if encrypted_user:
            # Decrypt the user data before returning
            user_data = self._decrypt_user_data(encrypted_user)
            return user_data
        else:
            return None
        
    def get_user_by_card(self, card_number):
        # Encrypt the card number
        # encrypted_card = self.fernet.encrypt(card_number.encode())
        # encrypted_card = self.fernet.decrypt(card_number.encode())
        # Retrieve a user by their encrypted card number from the MongoDB collection
        encrypted_user = self.users_collection.find_one({"card_number": card_number})
        
        if encrypted_user:
            # Decrypt the user data before returning
            user_data = self._decrypt_user_data(encrypted_user)
            return user_data
        else:
            return None


    def get_all_users(self):
        # Retrieve all users from the MongoDB collection
        encrypted_users = list(self.users_collection.find())

        decrypted_users = []
        for encrypted_user in encrypted_users:
            # Decrypt each user data before adding to the list
            user_data = self._decrypt_user_data(encrypted_user)
            decrypted_users.append(user_data)

        return decrypted_users

    def delete_user(self, user_id):
        # Delete a user by their ID from the MongoDB collection
        result = self.users_collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count

    def authenticate_user(self, username_or_email, password):
        # Authenticate a user by their username or email and password
        encrypted_user = self.users_collection.find_one(
            {"$or": [{"username": username_or_email}, {"email": username_or_email}]})

        if encrypted_user:
            # Decrypt the user data
            user_data = self._decrypt_user_data(encrypted_user, True)

            # Check if the decrypted password matches the provided password
            if user_data.get('password') == password:
                return user_data
            else:
                return None
        else:
            return None

    def _encrypt_user_data(self, user_data):
        # Encrypt the password and full name fields in the user data using Fernet encryption
        encrypted_data = user_data.copy()

        if 'password' in encrypted_data:
            password = encrypted_data['password']
            encrypted_password = self.fernet.encrypt(password.encode())
            encrypted_data['password'] = Binary(encrypted_password)

        if 'full_name' in encrypted_data:
            full_name = encrypted_data['full_name']
            encrypted_full_name = self.fernet.encrypt(full_name.encode())
            encrypted_data['full_name'] = Binary(encrypted_full_name)        
        
        # if 'card_number' in encrypted_data:
        #     card_number = encrypted_data['card_number']
        #     encrypted_card_number = self.fernet.encrypt(card_number.encode())
        #     encrypted_data['card_number'] = Binary(encrypted_card_number)

        return encrypted_data

    def _decrypt_user_data(self, encrypted_user, retain_password = False):
        # Decrypt the password and full name fields in the user data retrieved from MongoDB
        decrypted_data = encrypted_user.copy()

        if 'password' in decrypted_data:
            encrypted_password = decrypted_data['password']
            decrypted_password = self.fernet.decrypt(encrypted_password).decode()
            decrypted_data['password'] = decrypted_password

        if 'full_name' in decrypted_data:
            encrypted_full_name = decrypted_data['full_name']
            decrypted_full_name = self.fernet.decrypt(encrypted_full_name).decode()
            decrypted_data['full_name'] = decrypted_full_name
        
        # if 'card_number' in decrypted_data:
        #     encrypted_card_number = decrypted_data['card_number']
        #     decrypted_card_number = self.fernet.decrypt(encrypted_card_number).decode()
        #     decrypted_data['card_number'] = decrypted_card_number

        if not retain_password:
            decrypted_data.pop('password', None)
        return decrypted_data


    def create_log(self, device_id, user_id, timestamp, status, meta=None):
        access_log = UserAccessLog(device_id=device_id, user_id=user_id, timestamp=timestamp, status=status, meta_data=meta)
        access_log.save()
        return access_log

    def logs_by_device_or_user_id(self, identifier):
        access_logs = UserAccessLog.objects(device_id=identifier) | UserAccessLog.objects(user_id=identifier)
        return format_mongo_response(access_logs)

    def fetch_all_logs(self):
        # access_logs = UserAccessLog.objects()
        access_logs = format_mongo_response(UserAccessLog.objects())
        formatted_logs = []
        for log in access_logs:
            logger.info(log)
            device_name = device_model.get_device_by_id(log['device_id'])
            user = self.get_user_by_id_card(log['user_id'])
            full_name = user['full_name'] if user else "Unknown User"

            formatted_log = {
                "device_id": log['device_id'],
                "user_id": log['user_id'],
                "device_name": device_name['name'] if device_name else "Unknown Device",
                "user_name": full_name,
                "timestamp": log['timestamp'],
                "created_on": log['created_on'],
                "status": log['status'],
                "meta_data": log.get('meta_data', {}),
            }

            formatted_logs.append(formatted_log)

        return formatted_logs