from os import environ, path
import datetime

from dotenv import load_dotenv

basedir = path.abspath(path.join(path.dirname(__file__), '..'))
# loading env vars from .env file
load_dotenv()
APPLICATION_ENV = environ.get('APPLICATION_ENV')


class BaseConfig(object):
    ''' Base config class. '''

    APP_NAME = environ.get('APP_NAME') or 'SmartWareHouse'
    ORIGINS = ['*']
    EMAIL_CHARSET = 'UTF-8'
    API_KEY = environ.get('API_KEY')
    broker = environ.get('BROKER_URL')
    # backend = environ.get('RESULT_BACKEND')
    RESULT_BACKEND = environ.get('RESULT_BACKEND')
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    LOG_INFO_FILE = path.join(basedir, 'log', f'{current_date}-INFO.log')
    LOG_CELERY_FILE = path.join(basedir, 'log', f'{current_date}-celery.log')
    MONGODB_URI = environ.get('MONGODB_URI')    
    MONGODB_URI_FULL= environ.get('MONGODB_TEST_URI_FULL') if APPLICATION_ENV == 'test' else environ.get('MONGODB_URI_FULL')
    MONGODB_NAME = environ.get(
        'MONGOTESTDB_NAME') if APPLICATION_ENV == 'test' else environ.get('MONGODB_NAME')
    MONGOTESTDB_NAME = environ.get('MONGOTESTDB_NAME')
    MQTT_BROKER = environ.get('MQTT_BROKER')
    MQTT_BROKER_PORT = environ.get('MQTT_BROKER_PORT')
    MQTT_USERNAME = environ.get('MQTT_USERNAME')
    MQTT_PASSWORD = environ.get('MQTT_PASSWORD')
    PORT = environ.get('PORT')
    ENCRYPTION_KEY = environ.get('ENCRYPTION_KEY')
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '[%(asctime)s] - %(name)s - %(levelname)s - '
                '%(message)s',
                'datefmt': '%b %d %Y %H:%M:%S'
            },
            'simple': {
                'format': '%(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'log_info_file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOG_INFO_FILE,
                'maxBytes': 16777216,  # 16megabytes
                'formatter': 'standard',
                'backupCount': 5
            },
        },
        'loggers': {
            APP_NAME: {
                'level': 'DEBUG',
                'handlers': ['log_info_file'],
            },
        },
    }

    CELERY_LOGGING = {
        'format': '[%(asctime)s] - %(name)s - %(levelname)s - '
        '%(message)s',
        'datefmt': '%b %d %Y %H:%M:%S',
        'filename': LOG_CELERY_FILE,
        'maxBytes': 10000000,  # 10megabytes
        'backupCount': 5
    }


class Development(BaseConfig):
    ''' Development config. '''

    DEBUG = True
    ENV = 'dev'


class Staging(BaseConfig):
    ''' Staging config. '''

    DEBUG = True
    ENV = 'staging'


class Production(BaseConfig):
    ''' Production config '''

    DEBUG = False
    ENV = 'production'


class Test(BaseConfig):
    ''' Tets config. '''

    DEBUG = True
    ENV = 'test'

config = {
    'development': Development,
    'staging': Staging,
    'production': Production,
    'test': Test,
}

# Determine the environment based on the current settings


def get_environment():
    if environ.get('FLASK_ENV') == 'production':
        return 'production'
    elif environ.get('FLASK_ENV') == 'staging':
        return 'staging'
    else:
        return 'development'

# Load the appropriate configuration based on the environment


def load_config():
    environment = get_environment()
    return config[environment]


# Load the configuration
app_config = load_config()
