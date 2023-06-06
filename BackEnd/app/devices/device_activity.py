from datetime import datetime
from mongoengine import Document, StringField, DateTimeField, DictField
from app.utils.utils import format_mongo_response

class DeviceActivity(Document):
    name = StringField(required=True)
    device_id = StringField(required=True)
    action = StringField(required=True)
    meta_data = DictField()
    timestamp = DateTimeField(default=datetime.now)

class DeviceActivityLog:
    @staticmethod
    def log_device_activity(name, device_id, action, meta_data=None):
        activity = DeviceActivity(name=name, device_id=device_id, action=action, meta_data=meta_data)
        activity.save()

    @staticmethod
    def fetch_device_activities():
        activities = DeviceActivity.objects().order_by('-timestamp')
        return format_mongo_response(activities)

    @staticmethod
    def device_activities_by_device(device_id):
        activities = DeviceActivity.objects(device_id=device_id).order_by('-timestamp')
        return format_mongo_response(activities)
