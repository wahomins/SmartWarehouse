from flask import Blueprint, request, jsonify
from app.validations.user import validate_create_user_data, validate_update_user_data
from app.models.user_model import UserModel

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

# Other user routes...
