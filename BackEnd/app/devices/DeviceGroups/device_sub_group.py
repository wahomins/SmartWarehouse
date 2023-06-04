from datetime import datetime
from mongoengine import Document, StringField, ReferenceField, DateTimeField, signals
from .device_group import DeviceGroup


class DeviceSubGroup(Document):
    name = StringField(required=True)
    description = StringField()
    group = ReferenceField(DeviceGroup, required=True)
    created_on = DateTimeField(default=datetime.now)

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.created_on = datetime.now()

    meta = {
        "collection": "device_subgroups",
         'indexes': [
            {'fields': ['name', 'group'], 'unique': True}
        ]
    }

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "group_name": self.group.name,
            "created_on": self.created_on,
        }

signals.pre_save.connect(DeviceSubGroup.pre_save, sender=DeviceSubGroup)
