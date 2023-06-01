from flask import Blueprint, request, jsonify, current_app
from werkzeug.local import LocalProxy
from flask_pydantic import validate
from .validations import CreateUserModel, UpdateUserModel, LoginModel
from .models import UserModel
from app.utils.auth import generate_token, authenticate
import json
from datetime import datetime

user_bp = Blueprint('user', __name__)
logger = LocalProxy(lambda: current_app.logger)
user_model = UserModel()

@user_bp.route('/', methods=['POST'])
@validate(body=CreateUserModel)
def create_user():
    data = request.json
    data['createdOn'] = f'{datetime.now()}'
    
    user_id = user_model.create_user(data)
    
    return jsonify({'message': 'User created successfully', 'user_id': str(user_id)}), 201

@user_bp.route('/<user_id>', methods=['PUT'])
@authenticate
@validate(body=UpdateUserModel)
def update_user(decoded_token, user_id):
    
    data = request.json
    data['updatedBy'] = decoded_token['user_id']
    data['updatedOn'] = f'{datetime.now()}'
    
    # Update the user using the UserModel
    updated = user_model.update_user(user_id, data)
    
    if updated:
        # updated_data = json.loads(updated.decode('utf-8'))  # Convert bytes to JSON-serializable format
        updated.pop('password', None)
        return jsonify({'message': 'User updated successfully', 'user': updated}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@user_bp.route('/login', methods=['POST'])
@validate(body=LoginModel)
def login():
    data = request.json
    
    # Authenticate the user
    user = user_model.authenticate_user(data['username'], data['password'])
    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Generate a JSON Web Token (JWT) for the authenticated user
    token = generate_token(user['_id'], user['email'], user['full_name'])
    
    return jsonify({'token': token, 'user_id': str(user['_id']), 'email': user['email'], 'full_name': user['full_name']}), 200

@user_bp.route('/reset-password', methods=['POST'])
@authenticate
def reset_password():
    data = request.json
    
    # Reset the user's password
    reset_successful = user_model.reset_password(data['email'], data['new_password'])
    
    if reset_successful:
        return jsonify({'message': 'Password reset successful'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@user_bp.route('/', methods=['GET'])
@authenticate
def get_all_users():
    # Get all users from the UserModel
    users = user_model.get_all_users()

    # Remove the password field from each user
    for user in users:
        user.pop('password', None)

    return jsonify(users), 200

@user_bp.route('/<user_id>', methods=['GET'])
@authenticate
def get_user(user_id):
    # Get a user by their ID from the UserModel
    user = user_model.get_user_by_id(user_id)

    if user:
        # Remove the password field from the user
        user.pop('password', None)
        return jsonify(user), 200
    else:
        return jsonify({'error': 'User not found'}), 404
    
@user_bp.route('/users/<user_id>', methods=['DELETE'])
@authenticate
def delete_user(user_id):
    result = user_model.delete_user(user_id)
    if result == 1:
        # User successfully deleted
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        # User not found
        return jsonify({'error': 'User not found'}), 404
