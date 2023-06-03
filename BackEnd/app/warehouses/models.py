from datetime import datetime
from bson.objectid import ObjectId
from flask import current_app
from app import db
from app.config import app_config


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


def get_all_warehouses():
    warehouses = Warehouse.objects.all()
    return [format_response(warehouse) for warehouse in warehouses]


def create_warehouse(data):
    warehouse = Warehouse(**data)
    warehouse.save()
    return format_response(warehouse)


def update_warehouse(warehouse, data):
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
