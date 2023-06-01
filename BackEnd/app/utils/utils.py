
from bson import ObjectId
import json


# Custom JSON encoder to handle ObjectId serialization
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

def formart_mongo_response(result):
    updated_data = {}
    # Convert bytes to string and then to dictionary
    for key, value in result.items():
        if isinstance(value, bytes):
            updated_data[key] = value.decode('utf-8')
        else:
            updated_data[key] = value
    return updated_data