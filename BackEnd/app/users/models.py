from pymongo import MongoClient
from bson.binary import Binary
from bson.objectid import ObjectId
from cryptography.fernet import Fernet
import base64
from app.config import app_config

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
         
        self.fernet = Fernet(base64.urlsafe_b64decode(encryption_key))

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
        encrypted_user = self.users_collection.find_one_and_update(filter, update, return_document=True)
        
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

    def get_user_by_username(self, username_or_email):
        # Retrieve a user by their username or email from the MongoDB collection
        encrypted_user = self.users_collection.find_one({"$or": [{"username": username_or_email}, {"email": username_or_email}]})
        
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

    def authenticate_user(self, username_or_email, password):
        # Authenticate a user by their username or email and password
        encrypted_user = self.users_collection.find_one({"$or": [{"username": username_or_email}, {"email": username_or_email}]})
        
        if encrypted_user:
            # Decrypt the user data
            user_data = self._decrypt_user_data(encrypted_user)
            
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
        
        return encrypted_data
    
    def _decrypt_user_data(self, encrypted_user):
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
        
        return decrypted_data
