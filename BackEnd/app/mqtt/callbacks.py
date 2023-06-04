from datetime import datetime as dt
from paho.mqtt.client import connack_string as ack
import json

def on_connect(client, userdata, flags, rc, v5config=None):    
    # Subscribe to the topics for each device TOHOST & TODEVICE topics
    client.subscribe([('TO_HOST/#', 0), ('TO_DEVICE/#', 1), ('CLIENT_CONNECTIONS/#', 2)])
    init_message = json.dumps({
        'name': 'server',
        'status': 'connected',
        'timestamp': dt.now().strftime("%H:%M:%S.%f")[:-2]
    })
    client.publish("CLIENT_CONNECTIONS/server", payload=init_message, retain=False)
    print(dt.now().strftime("%H:%M:%S.%f")[:-2] + " Connection returned result: "+ack(rc))

def on_message(client, userdata, message,tmp=None):
    print(dt.now().strftime("%H:%M:%S.%f")[:-2] + " Received message " + str(message.payload) + " on topic '"
        + message.topic + "' with QoS " + str(message.qos))

def on_publish(client, userdata, mid,tmp=None):
    print(dt.now().strftime("%H:%M:%S.%f")[:-2] + " Published message id: "+str(mid))
    
def on_subscribe(client, userdata, mid, qos,tmp=None):
    if isinstance(qos, list):
        qos_msg = str(qos[0])
    else:
        qos_msg = f"and granted QoS {qos[0]}"
    print(dt.now().strftime("%H:%M:%S.%f")[:-2] + " Subscribed " + qos_msg)  