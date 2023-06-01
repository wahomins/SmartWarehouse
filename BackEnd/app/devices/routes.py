from flask import Blueprint, request, jsonify
from werkzeug.local import LocalProxy
from flask_pydantic import validate
from .validations import CreateDeviceModel, UpdateDeviceModel, AuthModel
from models.device_model import DeviceModel
from utils.auth import authenticate, generate_token


device_bp = Blueprint('device', __name__)
device_model = DeviceModel()

@device_bp.route('/devices', methods=['POST'])
@validate(body=CreateDeviceModel)
@authenticate
def create_device():
    data = request.json
    device_secret = device_model.generate_device_secret()
    encrypted_secret = device_model.encrypt_device_secret(device_secret)
    
    data['secret'] = encrypted_secret    
    device_id = device_model.create_device(data)
    
    return jsonify({'message': 'Device created successfully', 'device_id': str(device_id), 'device_secret': device_secret}), 201

@device_bp.route('/devices/<device_id>', methods=['PUT'])
@validate(body=UpdateDeviceModel)
@authenticate
def update_device(device_id):
    data = request.json
    updated = device_model.update_device(device_id, data)
    
    if updated:
        return jsonify({'message': 'Device updated successfully'}), 200
    else:
        return jsonify({'error': 'Device not found'}), 404

@device_bp.route('/devices', methods=['GET'])
@authenticate
def get_all_devices():
    devices = device_model.get_all_devices()
    
    for device in devices:
        del device['secret']
    
    return jsonify({'devices': devices}), 200

@device_bp.route('/devices/<device_id>', methods=['GET'])
@authenticate
def get_device(device_id):
    device = device_model.get_device_by_id(device_id)
    
    if device:
        del device['secret']
        return jsonify({'device': device}), 200
    else:
        return jsonify({'error': 'Device not found'}), 404

@device_bp.route('/devices/<device_id>/fetchSecret', methods=['GET'])
@authenticate
def fetch_device_secret(device_id):
    device = device_model.get_device_by_id(device_id)
    
    if device:
        decrypted_secret = device_model.decrypt_device_secret(device['secret'])
        
        return jsonify({'device_secret': decrypted_secret}), 200
    else:
        return jsonify({'error': 'Device not found'}), 404
    
@device_bp.route('/devices/<device_id>/<secret>', methods=['GET'])
@authenticate
def get_device(device_id, secret):
    device = device_model.get_device_by_id_and_secret(device_id, secret)
    if device:
        return jsonify(device), 200
    else:
        return jsonify({'error': 'Device not found'}), 404

@device_bp.route('/devices/<device_id>', methods=['DELETE'])
@authenticate
def delete_device(device_id):
    result = device_model.delete_device(device_id)
    if result == 1:
        return jsonify({'message': 'Device deleted successfully'}), 200
    else:
        return jsonify({'error': 'Device not found'}), 404
    
@device_bp.route('/devices/authenticate', methods=['POST'])
@validate(body=AuthModel)
def device_authenticate():
    data = request.json
    device_id = data.get('_id')
    secret = data.get('secret')

    device = DeviceModel.get_device_by_id_and_secret(device_id, secret)

    if device is None:
        return jsonify({'error': 'Invalid device ID or secret'}), 401

    token = generate_token(device_id, secret)

    return jsonify({'token': token.decode('utf-8')}), 200
