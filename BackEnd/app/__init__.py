import logging.config
from os import environ

from celery import Celery
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

from .config import config as app_config
from .utils.utils import CustomJSONEncoder



celery = Celery(__name__)


def create_app():
    # loading env vars from .env file
    load_dotenv()
    APPLICATION_ENV = get_environment()
    logging.config.dictConfig(app_config[APPLICATION_ENV].LOGGING)
    app = Flask(app_config[APPLICATION_ENV].APP_NAME)
    app.config.from_object(app_config[APPLICATION_ENV])
    app.config['PYDANTIC_ERROR_RESPONSE'] = True  # Enable error response formatting
    app.json_encoder = CustomJSONEncoder

    # Connect to MongoDB
    mongo_client = MongoClient(app_config[APPLICATION_ENV].MONGODB_URI)
    app.mongo_db = mongo_client[app_config[APPLICATION_ENV].MONGODB_NAME]
    CORS(app, resources={r'/api/*': {'origins': '*'}})

    celery.config_from_object(app.config, force=True)
    # celery is not able to pick result_backend and hence using update
    celery.conf.update(result_backend=app.config['RESULT_BACKEND'])

    #ROUTES
    from .core.views import core as core_blueprint
    from .users.routes import user_bp as user_blueprint


    app.register_blueprint(
        core_blueprint,
        url_prefix='/api/core'
    )
    app.register_blueprint(
        user_blueprint,
        url_prefix='/api/users'
    )

    return app


def get_environment():
    return environ.get('APPLICATION_ENV') or 'development'
