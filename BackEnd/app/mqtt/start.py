import paho.mqtt.client as mqtt
import ssl
from app.config import app_config
from os import path
from werkzeug.local import LocalProxy
from flask import current_app
from .callbacks import on_subscribe, on_message, on_publish, on_connect


basedir = path.abspath(path.join(path.dirname(__file__), '../..'))

def init_mqtt():
    # Create a new MQTT client
    client = mqtt.Client()
    ca_file = path.join(basedir, 'app/mqtt/certs/ca.crt')
    cert_file = path.join(path.dirname(__file__), 'certs/client.crt')
    key_file = path.join(path.dirname(__file__), 'certs/client.key')
    tls_context = ssl.create_default_context()
    tls_context.load_verify_locations(cafile=ca_file)
    tls_context.load_cert_chain(certfile=cert_file, keyfile=key_file)

    # Set the MQTT client callbacks
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe

    client.username_pw_set(app_config.MQTT_USERNAME, app_config.MQTT_PASSWORD)
    client.tls_set_context(tls_context)
    client.connect(app_config.MQTT_BROKER, int(app_config.MQTT_BROKER_PORT))

    # Start the MQTT client loop in a separate thread
    client.loop_start()
