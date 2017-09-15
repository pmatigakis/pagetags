import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_restful import Api
from flask_admin import Admin
from flask_restful_swagger import swagger

from pagetags import login_manager
from pagetags.models import db
from pagetags.authentication import (load_user, authenticate, identity,
                                     payload_handler, request_handler)
from pagetags.api.routes import add_api_routes
from pagetags import jwt
from pagetags.admin import (UserModelView, AuthenticatedIndexView,
                            TagModelView, UrlModelView, PostModelView,
                            CategoryModelView)
from pagetags.views.routes import add_view_routes


def initialize_logging(app):
    log_file = app.config["LOG_FILE"]
    log_file_size = app.config["LOG_FILE_SIZE"]
    log_file_count = app.config["LOG_FILE_COUNT"]
    log_level = app.config["LOG_LEVEL"]

    log_format = "%(asctime)s %(levelname)s [%(process)d:%(thread)d] " \
                 "%(name)s [%(pathname)s:%(funcName)s:%(lineno)d] %(message)s"
    formatter = logging.Formatter(log_format)

    handler = RotatingFileHandler(log_file,
                                  maxBytes=log_file_size,
                                  backupCount=log_file_count,
                                  encoding="utf8")

    handler.setFormatter(formatter)

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
    login_manager.login_view = "login"

    add_view_routes(app)

    api = swagger.docs(Api(app), apiVersion="1")
    add_api_routes(api)

    jwt.authentication_callback = authenticate
    jwt.identity_callback = identity
    jwt.jwt_payload_callback = payload_handler
    jwt.request_callback = request_handler
    jwt.init_app(app)

    admin = Admin(app, name='admin', template_mode='bootstrap3',
                  index_view=AuthenticatedIndexView())
    admin.add_view(TagModelView(db.session))
    admin.add_view(UrlModelView(db.session))
    admin.add_view(PostModelView(db.session))
    admin.add_view(UserModelView(db.session))
    admin.add_view(CategoryModelView(db.session))

    return app
