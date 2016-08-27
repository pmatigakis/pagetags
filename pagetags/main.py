import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_restful import Api

from pagetags import login_manager
from pagetags.models import db
from pagetags.views import index, new_url, tag, login, logout
from pagetags.authentication import load_user, authenticate, identity
from pagetags.api import TagsResource, TagPostingsResource
from pagetags import jwt


def initialize_logging(app):
    log_file = app.config["LOG_FILE"]
    log_file_size = app.config["LOG_FILE_SIZE"]
    log_file_count = app.config["LOG_FILE_COUNT"]
    log_level = app.config["LOG_LEVEL"]

    handler = RotatingFileHandler(log_file,
                                  maxBytes=log_file_size,
                                  backupCount=log_file_count)

    app.logger.addHandler(handler)
    if app.config["DEBUG"]:
        handler.setLevel(logging.DEBUG)
        app.logger.setLevel(logging.DEBUG)
    else:
        handler.setLevel(log_level)
        app.logger.setLevel(log_level)


def create_app(settings_file, environment_type=None):
    """Create the application object

    :param settings_file: the path to the configuration file
    :param environment_type: the environment type. Available options are
        development, production and testing
    :return: the Flask application object
    """
    app = Flask(__name__)

    app.config.from_object("pagetags.configuration.default")

    environment_configurations = {
        "production": "pagetags.configuration.production",
        "development": "pagetags.configuration.development",
        "testing": "pagetags.configuration.testing"
    }

    if environment_type is None:
        environment_type = "production"

    app.config.from_object(environment_configurations[environment_type])

    app.config.from_pyfile(settings_file, silent=False)

    if app.config["ENABLE_LOGGING"]:
        initialize_logging(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.user_callback = load_user

    app.add_url_rule("/", view_func=index)
    app.add_url_rule("/new_url", view_func=new_url, methods=["GET", "POST"])
    app.add_url_rule("/tag/<name>", view_func=tag)
    app.add_url_rule("/login", view_func=login, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=logout)

    api = Api(app)

    api.add_resource(TagsResource, "/api/v1/tags")
    api.add_resource(TagPostingsResource, "/api/v1/tag/<tag>")

    jwt.authentication_callback = authenticate
    jwt.identity_callback = identity
    jwt.init_app(app)

    return app
