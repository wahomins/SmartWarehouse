from datetime import datetime as dt
from .authentication import nfc_authentication
from app.devices.device_activity import DeviceActivityLog
from app.utils.utils import CustomJSONEncoder
import json
from .utils import  get_logger

logger = get_logger()

def handle_message(client, message, tmp):
    # Parse the topic and extract relevant information
    try:
        if not tmp:
            tmp =dt.now().strftime("%H:%M:%S.%f")[:-2]
        
        response = json.dumps({'status': 'FAILED', 'message': 'Server Error'}, cls=CustomJSONEncoder)
        topic_parts = message.topic.split("/")
        if len(topic_parts) >= 4 and topic_parts[0] == "TO_HOST":
            route = topic_parts[1]
            handler = topic_parts[2]
            device_id = topic_parts[3]
            payload = message.payload.decode("utf-8")  # Decode the payload from bytes to string
            payload_data = json.loads(payload)  # Parse the JSON payload

            # Call the appropriate handler based on the route
            if route == "Authentication":
                if handler == "nfc":
                    response = nfc_authentication(device_id, payload_data['data'], tmp)
                    DeviceActivityLog.log_device_activity(f'{route}/{handler}', device_id, 'nfc scan', payload_data['data'])
                elif handler == "bio":
                    response = nfc_authentication(device_id, payload_data['data'], tmp)
                # Add more handlers for different authentication methods

            if route == "Environment":
                if handler == "mq2":
                    DeviceActivityLog.log_device_activity(f'{route}/{handler}', device_id, 'mq2 smoke/co/lpg detected', payload_data['data'])
                    response = json.dumps({
                                    'status_code': 200,
                                    'status': "processed"
                                })
            
            if route == "Security":
                if handler == "Intrusion":
                    DeviceActivityLog.log_device_activity(f'{route}/{handler}', device_id, 'Intrusion log created', payload_data['data'])
                    response = json.dumps({
                                    'status_code': 200,
                                    'status': "processed"
                                }) 

            client.publish(message.topic.replace('HOST', 'DEVICE'), response)
            # Add more conditional statements for other routes
        elif len(topic_parts) >= 4 and topic_parts[0] == "CLIENT_CONNECTIONS":
            route = topic_parts[1]
            device_id = topic_parts[2]
            payload = message.payload.decode("utf-8")  # Decode the payload from bytes to string
            payload_data = json.loads(payload)  # Parse the JSON payload
            data = payload_data['data']
            if route == "activity":
                name = data['name']
                meta_data = data['meta_data']
                action = data['action']
                DeviceActivityLog.log_device_activity(name, device_id, action, meta_data)

    except Exception as e:
        logger.info("Failed to handle mqtt message")
        logger.error(e)