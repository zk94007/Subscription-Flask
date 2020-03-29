import logging
import os

logger = logging.getLogger(__name__)
from datetime import timedelta

class BaseConfig:
    DEBUG = False

    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR}/db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    CELERYBEAT_SCHEDULE = {
        'check_subscriptions_overflow': {
            'task': 'usage_celery.check_subscriptions_overflow',
            'schedule': timedelta(seconds=30)
        }
    }


class DevelopmentConfig(BaseConfig):

    ENV = 'development'
    DEBUG = True
    HOST = "localhost"
    PORT = "5000"
    SECRET_KEY = "test"
    ENCRYPTION_KEY = "test"

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


class TestConfig(BaseConfig):

    ENV = 'testing'
    TESTING = True
    DOMAIN = 'http://testserver'
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
