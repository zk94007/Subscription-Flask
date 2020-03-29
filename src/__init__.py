"""Flask app config and initialization"""
import logging.config

from flask import Flask
from sqlalchemy import orm
from celery import Celery
import config

celery = Celery(__name__, backend= config.DevelopmentConfig.CELERY_RESULT_BACKEND, 
                    broker= config.DevelopmentConfig.CELERY_BROKER_URL)

def create_app(config_obj=None):
    """Sets config from passed in config object,
    initializes Flask modules, registers blueprints (routes)

    Args:
        config_obj (class): config class to apply to app

    Returns:
        app: configured and initialized Flask app object

    """
    app = Flask(__name__, static_folder=None)

    if not config_obj:
        logging.warning(
            "No config specified; defaulting to development"
        )
        config_obj = config.DevelopmentConfig

    app.config.from_object(config_obj)

    from src.models.base import db, migrate

    db.init_app(app)
    db.app = app

    migrate.init_app(app, db)

    celery.conf.update(app.config)

    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask

    from src.routes import register_routes
    register_routes(app)

    return app
