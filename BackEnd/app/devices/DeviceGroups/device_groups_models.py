from app import db
from datetime import datetime
from .device_group import DeviceGroup
from app.utils.utils import format_mongo_response

def create_device_group(data):
    device_group = DeviceGroup(name=data['name'], description=data.get('description'))
    device_group.save()
    return format_mongo_response(device_group)


def get_device_group_by_name(name):
    device_group = DeviceGroup.objects(name=name).first()
    return format_mongo_response(device_group)


def get_device_group_by_id(device_group_id):
    device_group = DeviceGroup.objects(id=device_group_id).first()
    return format_mongo_response(device_group)

def fetch_device_groups():
    device_groups = DeviceGroup.objects().all()
    return format_mongo_response(device_groups)


def update_device_group(device_group_id, data):
    device_group = DeviceGroup.objects(id=device_group_id).first()
    if device_group:
        device_group.name = data['name']
        device_group.description = data.get('description')
        device_group.save()
    return format_mongo_response(device_group)


def delete_device_group(device_group_id):
    device_group = DeviceGroup.objects(id=device_group_id).first()
    if device_group:
        device_group.delete()
    return format_mongo_response(device_group)
