import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_restful import Api
from flask_admin import Admin
from flask_restful_swagger import swagger

from pagetags import login_manager
from pagetags.models import db
from pagetags.views import posts, tags, authentication
from pagetags.authentication import (load_user, authenticate, identity,
                                     payload_handler, request_handler)
from pagetags.api.resources import (TagsResource, TagPostsResource,
                                    PostsResource, UrlResource, PostResource)
from pagetags import jwt
from pagetags.admin import (UserModelView, AuthenticatedIndexView,
                            TagModelView, UrlModelView, PostModelView,
                            CategoryModelView)


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

    app.add_url_rule("/", view_func=posts.index)
    app.add_url_rule("/tag/<name>", view_func=tags.tag)
    app.add_url_rule("/tags", view_func=tags.tags)
    app.add_url_rule(
        "/login", view_func=authentication.login, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=authentication.logout)

    api = swagger.docs(Api(app), apiVersion="1")

    api.add_resource(TagsResource, "/api/v1/tags")
    api.add_resource(TagPostsResource, "/api/v1/tag/<tag>")
    api.add_resource(PostsResource, "/api/v1/posts")
    api.add_resource(UrlResource, "/api/v1/url")
    api.add_resource(PostResource, "/api/v1/post/<int:post_id>")

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
