from datetime import datetime
from mongoengine import Document, StringField, DateTimeField, signals


class DeviceGroup(Document):
    name = StringField(required=True, unique=True)
    description = StringField()
    created_on = DateTimeField(default=datetime.now)

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.created_on = datetime.now()

    meta = {
        "collection": "device_groups",
        "indexes": ["name"],
    }

signals.pre_save.connect(DeviceGroup.pre_save, sender=DeviceGroup)
