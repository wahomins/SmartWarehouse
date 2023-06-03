import logging.config
from os import environ

from celery import Celery
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from flask_mongoengine import MongoEngine

from .config import config as configs
from .config import app_config
from .utils.utils import CustomJSONEncoder


celery = Celery(__name__)

db =MongoEngine()

def create_app():
    # loading env vars from .env file
    load_dotenv()
    APPLICATION_ENV = get_environment()
    logging.config.dictConfig(configs[APPLICATION_ENV].LOGGING)
    app = Flask(configs[APPLICATION_ENV].APP_NAME)
    app.config.from_object(configs[APPLICATION_ENV])
    app.config['PYDANTIC_ERROR_RESPONSE'] = True  # Enable error response formatting
    app.json_encoder = CustomJSONEncoder
    app.config['MONGODB_SETTINGS'] = {
        'db': configs[APPLICATION_ENV].MONGODB_NAME,
        'host': f'{configs[APPLICATION_ENV].MONGODB_URI_FULL}'
    }
    app.config['MONGODB_ALIAS'] = {
        'test': configs[APPLICATION_ENV].MONGODB_NAME,
        configs[APPLICATION_ENV].MONGODB_NAME: configs[APPLICATION_ENV].MONGODB_NAME
    }

    db.init_app(app)

    # Connect to MongoDB using pymongo
    mongo_client = MongoClient(configs[APPLICATION_ENV].MONGODB_URI)
    app.mongo_db = mongo_client[configs[APPLICATION_ENV].MONGODB_NAME]
    CORS(app, resources={r'/api/*': {'origins': '*'}})

    celery.config_from_object(app.config, force=True)
    # celery is not able to pick result_backend and hence using update
    celery.conf.update(result_backend=app.config['RESULT_BACKEND'])

    # ROUTES
    from .core.views import core as core_blueprint
    from .users.routes import user_bp as user_blueprint
    from .devices.routes import device_bp as device_blueprint
    from .warehouses.routes import warehouses_bp as warehouse_blueprint

    app.register_blueprint(
        core_blueprint,
        url_prefix='/api/core'
    )
    app.register_blueprint(
        user_blueprint,
        url_prefix='/api/users'
    )
    app.register_blueprint(
        device_blueprint,
        url_prefix='/api/devices'
    )
    app.register_blueprint(
        warehouse_blueprint,
        url_prefix='/api/warehouses'
    )

    return app


def get_environment():
    return environ.get('APPLICATION_ENV') or 'development'
