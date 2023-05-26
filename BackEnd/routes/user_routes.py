from flask import Blueprint, request, jsonify
from validations.user import validate_create_user_data, validate_update_user_data, validate_login_data
from models.user_model import UserModel
from utils.auth import generate_token

user_bp = Blueprint('user', __name__)
user_model = UserModel()

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    
    # Validate the received user data for creating a user
    valid, error = validate_create_user_data(data)
    if not valid:
        return jsonify({'error': error}), 400
    
    # Create a new user using the UserModel
    user_id = user_model.create_user(data)
    
    return jsonify({'message': 'User created successfully', 'user_id': str(user_id)}), 201

@user_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    
    # Validate the received user data for updating a user
    valid, error = validate_update_user_data(data)
    if not valid:
        return jsonify({'error': error}), 400
    
    # Update the user using the UserModel
    updated = user_model.update_user(user_id, data)
    
    if updated:
        return jsonify({'message': 'User updated successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    
    # Validate the received login data
    valid, error = validate_login_data(data)
    if not valid:
        return jsonify({'error': error}), 400
    
    # Authenticate the user
    user = user_model.authenticate_user(data['email'], data['password'])
    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Generate a JSON Web Token (JWT) for the authenticated user
    token = generate_token(user['_id'], user['email'], user['full_name'])
    
    return jsonify({'token': token, 'user_id': str(user['_id']), 'email': user['email'], 'full_name': user['full_name']}), 200

@user_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    
    # Reset the user's password
    reset_successful = user_model.reset_password(data['email'], data['new_password'])
    
    if reset_successful:
        return jsonify({'message': 'Password reset successful'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@user_bp.route('/users', methods=['GET'])
def get_all_users():
    # Get all users from the UserModel
    users = user_model.get_all_users()

    # Remove the password field from each user
    for user in users:
        user.pop('password', None)

    return jsonify(users), 200

@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    # Get a user by their ID from the UserModel
    user = user_model.get_user_by_id(user_id)

    if user:
        # Remove the password field from the user
        user.pop('password', None)
        return jsonify(user), 200
    else:
        return jsonify({'error': 'User not found'}), 404
