""""
Main application directory module
"""
import os
from flask import Flask, jsonify
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from dotenv import load_dotenv
from pathlib import Path
from flask_cors import CORS


load_dotenv()


sqlalchemy = SQLAlchemy()
migrate = Migrate(compare_type=True)
jwt = JWTManager()
bcrypt = Bcrypt()

config = Config()
load_dotenv()


"""
Create a flask app instance with given
configuration object, initialize extentions
and register flask blueprints
"""


def create_app(config_obj=None):
    app = Flask(__name__)

    if config_obj is None:
        app.config.from_object(config)
    else:
        app.config.from_object(config_obj)
    initialize_extensions(app)
    register_blueprints(app)

    # Create database tables if they do not exist
    # within flask application context
    with app.app_context():
        sqlalchemy.create_all()

    return app


def initialize_extensions(app):
    # Initialize flask-extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    sqlalchemy.init_app(app)
    migrate.init_app(app, sqlalchemy)
    CORS(app, resources={r"/api/*": {"origins": "*"}})


def register_blueprints(app):
    from app.api import api

    # Register Blueprints
    app.register_blueprint(api)
