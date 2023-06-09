from app.users.models import UserModel
import json
from datetime import datetime as dt
from app.utils.utils import CustomJSONEncoder

user_model = UserModel()

def nfc_authentication(device_id, payload, tmp):
    card_number = payload['card_number']
    user_raw = user_model.get_user_by_card(card_number)
    status = 'FAILED'
    resp_payload = json.dumps({'status_code': 500, 'status': status, 'tmp': dt.now().strftime("%H:%M:%S.%f")[:-2], 'message': 'User not found'})
    if user_raw:
        user_p = json.dumps(user_raw, cls=CustomJSONEncoder)
        user = json.loads(user_p)
        status = 'SUCCESS'
        resp_payload = json.dumps({
            'status_code': 200,
            'name': user['full_name'],
            'user_id': user['_id'],
            'status': status
        })        
        user_model.create_log(device_id, user['_id'], tmp, status)
    else:
        user_model.create_log(device_id, card_number, tmp, status)
    return resp_payload
