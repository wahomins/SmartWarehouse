from werkzeug.local import LocalProxy
import logging.config
from app.config import app_config


def get_logger():
    # Create a logger
    # LOGGING = app_config.LOGGING
    # # LOGGING['handlers']['log_info_file']['filename'] = app_config.LOG_MQTT_FILE
    # logging.config.dictConfig(LOGGING)
    mqtt_logger = logging.getLogger(app_config.MQTT_BROKER_APP)
    logger = LocalProxy(lambda: mqtt_logger)
    return logger