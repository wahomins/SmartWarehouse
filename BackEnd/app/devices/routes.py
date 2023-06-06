from flask import Blueprint, request, jsonify
from werkzeug.local import LocalProxy
from flask_pydantic import validate
from .validations import CreateDeviceModel, UpdateDeviceModel, AuthModel
from .models import DeviceModel
from app.utils.auth import authenticate, generate_device_token
from datetime import datetime
from .DeviceGroups.device_groups_models import get_device_group_by_name, get_device_group_by_id, fetch_device_groups
from .DeviceGroups.device_sub_groups_models import get_device_subgroup_by_id, get_device_subgroups_by_group_id, get_device_subgroup_by_name
from .device_activity import DeviceActivityLog


device_bp = Blueprint('device', __name__)
device_model = DeviceModel()


@device_bp.route('/', methods=['POST'])
@validate(body=CreateDeviceModel)
@authenticate
def create_device(decoded_token):
    data = request.json
    device_secret = device_model.generate_device_secret()
    encrypted_secret = device_model.encrypt_device_secret(device_secret)

    data['secret'] = encrypted_secret
    data['created_by'] = decoded_token['user_id']
    data['created_on'] = f'{datetime.now()}'
    device_id = device_model.create_device(data)

    return jsonify({'message': 'Device created successfully', 'device_id': device_id, 'device_secret': device_secret}), 201


@device_bp.route('/<device_id>', methods=['PUT'])
@validate(body=UpdateDeviceModel)
@authenticate
def update_device(decoded_token, device_id):
    data = request.json
    data['updated_by'] = decoded_token['user_id']
    data['updated_on'] = f'{datetime.now()}'
    updated = device_model.update_device(device_id, data)

    if updated:
        return jsonify({'message': 'Device updated successfully'}), 200
    else:
        return jsonify({'error': 'Device not found'}), 404


@device_bp.route('/', methods=['GET'])
@authenticate
def get_all_devices(decoded_token):
    devices = device_model.get_all_devices()

    for device in devices:
        del device['secret']

    return jsonify({'devices': devices}), 200


@device_bp.route('/<device_id>', methods=['GET'])
@authenticate
def get_device(decoded_token, device_id):
    device = device_model.get_device_by_id(device_id)

    if device:
        del device['secret']
        return jsonify({'device': device}), 200
    else:
        return jsonify({'error': 'Device not found'}), 404


@device_bp.route('/<device_id>/fetchSecret', methods=['GET'])
@authenticate
def fetch_device_secret(decoded_token, device_id):
    device = device_model.get_device_by_id(device_id)

    if device:
        resp = device_model._decrypt_data(device) 
        return jsonify({'device_secret': resp['secret']}), 200
    else:
        return jsonify({'error': 'Device not found'}), 404


@device_bp.route('/<device_id>', methods=['DELETE'])
@authenticate
def delete_device(decoded_token, device_id):
    result = device_model.delete_device(device_id)
    if result == 1:
        return jsonify({'message': 'Device deleted successfully'}), 200
    else:
        return jsonify({'error': 'Device not found'}), 404


@device_bp.route('/auth', methods=['POST'])
@validate(body=AuthModel)
def device_authenticate():
    data = request.json
    device_id = data.get('device_id')
    secret = data.get('secret')

    device = device_model.get_device_by_id_and_secret(device_id, secret)

    if device is None:
        return jsonify({'error': 'Invalid device ID or secret'}), 401

    token = generate_device_token(device_id, device.get('name'))

    return jsonify({'token': token, 'device_id': device_id, 'name': device['name']}), 200

@device_bp.route('/<device_id>/secret', methods=['PUT'])
@authenticate
def update_device_secret(decoded_token, device_id):
    new_secret = device_model.generate_device_secret()
    encrypted = device_model.encrypt_device_secret(new_secret)
    data = {'secret': encrypted}
    data['updated_by'] = decoded_token['user_id']
    data['updated_on'] = f'{datetime.now()}'
    updated = device_model.update_device(device_id, data)

    if updated:
        return jsonify({'message': 'Device updated successfully'}), 200
    else:
        return jsonify({'error': 'Device not found'}), 404


@device_bp.route('/group/<group_name>', methods=['GET'])
def get_device_group_by_name(group_name):
    # Retrieve a device group by its name
    device_group = get_device_group_by_name(group_name)
    if device_group:
        return jsonify(device_group)
    return jsonify({'error': 'Device group not found'}), 404

@device_bp.route('/groups/', methods=['GET'])
def get_all_device_groups():
    # Retrieve all device groups
    device_groups = fetch_device_groups()
    return jsonify(device_groups)

@device_bp.route('/groups/<group_id>/', methods=['GET'])
def get_device_group_by_id_route(group_id):
    # Retrieve a device group by its ID
    device_group = get_device_group_by_id(group_id)
    if device_group:
        return jsonify(device_group)
    return jsonify({'error': 'Device group not found'}), 404

@device_bp.route('/subgroup/<subgroup_id>/', methods=['GET'])
def get_device_subgroup_by_id_route(subgroup_id):
    # Retrieve a device subgroup by its ID
    device_subgroup = get_device_subgroup_by_id(subgroup_id)
    if device_subgroup:
        return jsonify(device_subgroup)
    return jsonify({'error': 'Device subgroup not found'}), 404

@device_bp.route('/subgroup/group/<group_id>/', methods=['GET'])
def get_device_subgroups_by_group_id_route(group_id):
    # Retrieve all device subgroups of a specific device group
    device_subgroups = get_device_subgroups_by_group_id(group_id)
    return jsonify(device_subgroups)

@device_bp.route('/subgroup/<subgroup_name>/', methods=['GET'])
def get_device_subgroup_by_name_route(subgroup_name):
    # Retrieve a device subgroup by its name
    device_subgroup = get_device_subgroup_by_name(subgroup_name)
    if device_subgroup:
        return jsonify(device_subgroup)
    return jsonify({'error': 'Device subgroup not found'}), 404

@device_bp.route('/logs/activity/', methods=['GET'])
def get_all_device_activity_logs():
    activities = DeviceActivityLog.fetch_device_activities()
    return jsonify(activities)

@device_bp.route('/logs/activity/<device_id>/', methods=['GET'])
def get_device_activity_logs(device_id):
    activities = DeviceActivityLog.device_activities_by_device(device_id)
    return jsonify(activities)