from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt import JWT


db = SQLAlchemy()

login_manager = LoginManager()

jwt = JWT()
