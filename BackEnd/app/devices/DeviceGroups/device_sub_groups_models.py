from app import db
from datetime import datetime
from .device_group import DeviceGroup
from .device_sub_group import DeviceSubGroup
from app.utils.utils import format_mongo_response


def create_device_subgroup(data):
    group = DeviceGroup.objects(name=data['group']).first()
    if group:
        device_subgroup = DeviceSubGroup(name=data['name'], description=data.get('description'), group=group)
        device_subgroup.save()
        return format_mongo_response(device_subgroup)
    return None


def get_device_subgroup_by_name(name):
    device_subgroup = DeviceSubGroup.objects(name=name).first()
    return format_mongo_response(device_subgroup)

def get_device_subgroup_by_id(device_subgroup_id):
    device_subgroup = DeviceSubGroup.objects(id=device_subgroup_id).first()
    return format_mongo_response(device_subgroup)

def get_device_subgroups_by_group_id(device_group_id):
    device_subgroups = DeviceSubGroup.objects(group=device_group_id).all()
    result = []
    for subgroup in device_subgroups:
        subgroup_data = format_mongo_response(subgroup)
        subgroup_data['group_name'] = subgroup.group.name
        result.append(subgroup_data)
    return result

def fetch_device_subgroups():
    device_subgroups = DeviceSubGroup.objects().all()
    return format_mongo_response(device_subgroups)


def update_device_subgroup(device_subgroup_id, data):
    device_subgroup = DeviceSubGroup.objects(id=device_subgroup_id).first()
    if device_subgroup:
        group = DeviceGroup.objects(name=data['group']).first()
        if group:
            device_subgroup.name = data['name']
            device_subgroup.description = data.get('description')
            device_subgroup.group = group
            device_subgroup.save()
    return format_mongo_response(device_subgroup)


def delete_device_subgroup(device_subgroup_id):
    device_subgroup = DeviceSubGroup.objects(id=device_subgroup_id).first()
    if device_subgroup:
        device_subgroup.delete()
    return format_mongo_response(device_subgroup)
