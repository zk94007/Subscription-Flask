"""Base classes and utilities for models to inherit or use"""
from flask import current_app
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
