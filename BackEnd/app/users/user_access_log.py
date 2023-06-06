from datetime import datetime
from mongoengine import Document, StringField, DateTimeField, signals


class UserAccessLog(Document):
    device_id = StringField(required=True)
    user_id = StringField(required=True)
    timestamp = DateTimeField(required=True)
    created_on = DateTimeField(default=datetime.now)
    status = StringField(required=True, default='FAIL')
    meta_data = StringField()

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.created_on = datetime.now()

    meta = {
        "collection": "user_access_logs"
    }

signals.pre_save.connect(UserAccessLog.pre_save, sender=UserAccessLog)