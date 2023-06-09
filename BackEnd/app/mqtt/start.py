import paho.mqtt.client as mqtt
import ssl
from app.config import app_config
from os import path
from werkzeug.local import LocalProxy
from flask import current_app
from .callbacks import on_subscribe, on_message, on_publish, on_connect
import logging.config


basedir = path.abspath(path.join(path.dirname(__file__), '../..'))

def setup_logger():
    # Create a logger
    # LOGGING = app_config.LOGGING
    # # LOGGING['handlers']['log_info_file']['filename'] = app_config.LOG_MQTT_FILE
    # logging.config.dictConfig(LOGGING)
    mqtt_logger = logging.getLogger(app_config.MQTT_BROKER_APP)
    logger = LocalProxy(lambda: mqtt_logger)
    return logger

def init_mqtt():
    logger = setup_logger()
    try:
        # Create a new MQTT client
        client = mqtt.Client()

        # Set the MQTT client callbacks
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_publish = on_publish
        client.on_subscribe = on_subscribe

        client.username_pw_set(app_config.MQTT_USERNAME, app_config.MQTT_PASSWORD)

        if app_config.MQTT_BROKER_PORT == 8883:
            ca_file = path.join(basedir, 'app/mqtt/certs/ca.crt')
            cert_file = path.join(path.dirname(__file__), 'certs/client.crt')
            key_file = path.join(path.dirname(__file__), 'certs/client.key')
            tls_context = ssl.create_default_context()
            tls_context.load_verify_locations(cafile=ca_file)
            tls_context.load_cert_chain(certfile=cert_file, keyfile=key_file)
            client.tls_set_context(tls_context)

        client.connect(app_config.MQTT_BROKER, int(app_config.MQTT_BROKER_PORT))

        # Start the MQTT client loop in a separate thread
        client.loop_start()
    except Exception as e:
        logger.info("Failed to start mqtt")
        logger.error(e)
