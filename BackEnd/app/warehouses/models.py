from datetime import datetime
from bson.objectid import ObjectId
from flask import current_app
from werkzeug.local import LocalProxy
from app import db
from app.config import app_config

logger = LocalProxy(lambda: current_app.logger)

class Warehouse(db.DynamicDocument):
    name = db.StringField(required=True)
    latitude = db.FloatField()
    longitude = db.FloatField()
    close_land_mark = db.StringField(required=True)
    town = db.StringField()
    description = db.StringField()
    manager_id = db.ObjectIdField()
    created_by = db.ObjectIdField(required=True)
    created_on = db.DateTimeField(default=datetime.now)
    updated_by = db.ObjectIdField()
    updated_on = db.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        self.updated_on = datetime.now()
        super().save(*args, **kwargs)

    meta = {
        'collection': 'warehouses',
        'indexes': [
            {'fields': ['name', 'town'], 'unique': True}
        ]
        }


def get_warehouse_by_id(warehouse_id):
    try:
        warehouse = Warehouse.objects.get(id=ObjectId(warehouse_id))
        return format_response(warehouse)
    except Warehouse.DoesNotExist:
        return None


# def get_all_warehouses():
#     warehouses = Warehouse.objects.all()
#     return [format_response(warehouse) for warehouse in warehouses]

from pymongo import MongoClient
from bson.objectid import ObjectId

def get_all_warehouses():
    warehouses = Warehouse.objects.all()
    
    # Fetch manager names from the users collection
    manager_ids = [str(warehouse.manager_id) for warehouse in warehouses]
    manager_names = {}
    
    with MongoClient(app_config.MONGODB_URI) as client:
        db = client[app_config.MONGODB_NAME]
        users_collection = db['users']
        
        managers = users_collection.find({'_id': {'$in': [ObjectId(manager_id) for manager_id in manager_ids]}})
        for manager in managers:
            manager_names[str(manager['_id'])] = manager['username']

    # Format the response for each warehouse, including the managerName
    formatted_warehouses = []
    for warehouse in warehouses:
        formatted_warehouse = format_response(warehouse)
        manager_id = str(warehouse.manager_id)
        manager_name = manager_names.get(manager_id)
        formatted_warehouse['manager_name'] = manager_name
        formatted_warehouses.append(formatted_warehouse)

    return formatted_warehouses

def create_warehouse(data):
    warehouse = Warehouse(**data)
    warehouse.save()
    return format_response(warehouse)


# def update_warehouse(warehouse_id, data):
#     warehouse = Warehouse.objects.get(id=ObjectId(warehouse_id))
#     logger.debug(f"warehouseData {warehouse}")

#     for key, value in data.items():
#         if key in warehouse:
#             setattr(warehouse, key, value)
#         else:
#             warehouse[key] = value

#     warehouse.save()
#     return format_response(warehouse)

def update_warehouse(warehouse_id, data):
    warehouse = Warehouse.objects.get(id=ObjectId(warehouse_id))
    for key, value in data.items():
        setattr(warehouse, key, value)
    warehouse.save()
    return format_response(warehouse)

def delete_warehouse(warehouse_id):
    try:
        warehouse = Warehouse.objects.get(id=ObjectId(warehouse_id))
        warehouse.delete()
        return True
    except Warehouse.DoesNotExist:
        return False


def format_response(doc):
    formatted_dict = {}
    for field_name, field_value in doc.to_mongo().items():
        if isinstance(field_value, ObjectId):
            formatted_dict[field_name] = str(field_value)
        elif isinstance(field_value, datetime):
            formatted_dict[field_name] = field_value.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            formatted_dict[field_name] = field_value
    return formatted_dict
