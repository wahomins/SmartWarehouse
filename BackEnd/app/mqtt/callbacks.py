from datetime import datetime as dt
from paho.mqtt.client import connack_string as ack
import json
from .handlers.main import handle_message
from .handlers.utils import get_logger

logger = get_logger()

def on_connect(client, userdata, flags, rc, v5config=None):    
    # Subscribe to the topics for each device TOHOST & TODEVICE topics
    # client.subscribe([('TO_HOST/#', 0), ('TO_DEVICE/#', 1), ('CLIENT_CONNECTIONS/#', 2)])
    client.subscribe([('TO_HOST/#', 0), ('CLIENT_CONNECTIONS/#', 2)])
    init_message = json.dumps({
        "data": {
            'name': 'server',
            'status': 'connected',
            'timestamp': dt.now().strftime("%H:%M:%S.%f")[:-2]
        }
    })
    client.publish("CLIENT_CONNECTIONS/activity/server", payload=init_message, retain=False)
    logger.info(dt.now().strftime("%H:%M:%S.%f")[:-2] + " Connection returned result: "+ack(rc))

def on_message(client, userdata, message,tmp=None):
    
    handle_message(client=client, message=message, tmp=tmp)
    logger.info(dt.now().strftime("%H:%M:%S.%f")[:-2] + " Received message " + str(message.payload) + " on topic '"
        + message.topic + "' with QoS " + str(message.qos) + "with client " + str(client._client_id))

def on_publish(client, userdata, mid,tmp=None):
    logger.info(dt.now().strftime("%H:%M:%S.%f")[:-2] + " Published message id: "+str(mid))
    
def on_subscribe(client, userdata, mid, qos,tmp=None):
    if isinstance(qos, list):
        qos_msg = str(qos[0])
    else:
        qos_msg = f"and granted QoS {qos[0]}"
    logger.info(dt.now().strftime("%H:%M:%S.%f")[:-2] + " Subscribed " + qos_msg)  