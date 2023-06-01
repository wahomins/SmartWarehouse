from flask import Blueprint, request, jsonify
from validations.device import validate_create_device_data, validate_update_device_data
from models.device_model import DeviceModel
from utils.auth import authenticate


device_bp = Blueprint('device', __name__)
device_model = DeviceModel()

@device_bp.route('/devices', methods=['POST'])
@authenticate
def create_device():
    data = request.json
    
    # Validate the received device data for creating a device
    valid, error = validate_create_device_data(data)
    if not valid:
        return jsonify({'error': error}), 400
    
    # Generate a new device secret
    device_secret = device_model.generate_device_secret()
    
    # Encrypt the device secret
    encrypted_secret = device_model.encrypt_device_secret(device_secret)
    
    # Add the encrypted secret to the device data
    data['secret'] = encrypted_secret
    
    # Create a new device using the DeviceModel
    device_id = device_model.create_device(data)
    
    return jsonify({'message': 'Device created successfully', 'device_id': str(device_id), 'device_secret': device_secret}), 201

@device_bp.route('/devices/<device_id>', methods=['PUT'])
@authenticate
def update_device(device_id):
    data = request.json
    
    # Validate the received device data for updating a device
    valid, error = validate_update_device_data(data)
    if not valid:
        return jsonify({'error': error}), 400
    
    # Update the device using the DeviceModel
    updated = device_model.update_device(device_id, data)
    
    if updated:
        return jsonify({'message': 'Device updated successfully'}), 200
    else:
        return jsonify({'error': 'Device not found'}), 404

@device_bp.route('/devices', methods=['GET'])
@authenticate
def get_all_devices():
    devices = device_model.get_all_devices()
    
    # Remove the secret from the device data before returning
    for device in devices:
        del device['secret']
    
    return jsonify({'devices': devices}), 200

@device_bp.route('/devices/<device_id>', methods=['GET'])
def get_device(device_id):
    device = device_model.get_device_by_id(device_id)
    
    if device:
        # Remove the secret from the device data before returning
        del device['secret']
        return jsonify({'device': device}), 200
    else:
        return jsonify({'error': 'Device not found'}), 404

@device_bp.route('/devices/<device_id>/fetchSecret', methods=['GET'])
@authenticate
def fetch_device_secret(device_id):
    device = device_model.get_device_by_id(device_id)
    
    if device:
        # Decrypt the device secret
        decrypted_secret = device_model.decrypt_device_secret(device['secret'])
        
        return jsonify({'device_secret': decrypted_secret}), 200
    else:
        return jsonify({'error': 'Device not found'}), 404
