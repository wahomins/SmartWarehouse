
from bson import ObjectId
import json
from datetime import datetime
from mongoengine import Document, QuerySet


# Custom JSON encoder to handle ObjectId serialization
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

def format_mongo_response(doc):
    def format_field_value(field_value):
        if isinstance(field_value, ObjectId):
            return str(field_value)
        elif isinstance(field_value, datetime):
            return field_value.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            return field_value
    if doc is None:
        return None
    elif isinstance(doc, QuerySet):
        formatted_list = []
        for document in doc:
            formatted_dict = {field_name: format_field_value(field_value)
                              for field_name, field_value in document.to_mongo().items()}
            formatted_list.append(formatted_dict)
        return formatted_list
    elif isinstance(doc, Document):
        formatted_dict = {field_name: format_field_value(field_value)
                          for field_name, field_value in doc.to_mongo().items()}
        return formatted_dict
    else:
        formatted_dict = {field_name: format_field_value(field_value)
                          for field_name, field_value in doc.to_mongo().items()}
        return formatted_dict