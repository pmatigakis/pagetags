from flask import Flask

from pagetags import login_manager
from pagetags.models import db
from pagetags.views import index, new_url, tag, login, logout
from pagetags.authentication import load_user


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

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.user_callback = load_user

    app.add_url_rule("/", view_func=index)
    app.add_url_rule("/new_url", view_func=new_url, methods=["GET", "POST"])
    app.add_url_rule("/tag/<name>", view_func=tag)
    app.add_url_rule("/login", view_func=login, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=logout)

    return app
