import logging.config

from flask import Flask
from flask_restful import Api
from flask_restful_swagger import swagger

from pagetags.api.routes import add_api_routes
from pagetags.views.routes import add_view_routes
from pagetags.extensions import initialize_extensions


def initialize_logging(app):
    logging_configuration = app.config.get("LOGGING")
    if logging_configuration is not None:
        logging.config.dictConfig(logging_configuration)


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

    initialize_logging(app)

    initialize_extensions(app)
    add_view_routes(app)

    api = swagger.docs(Api(app), apiVersion="1")
    add_api_routes(api)

    return app
