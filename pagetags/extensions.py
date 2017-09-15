from flask_admin import Admin

from pagetags import login_manager
from pagetags.models import db
from pagetags.authentication import (load_user, authenticate, identity,
                                     payload_handler, request_handler)
from pagetags import jwt
from pagetags.admin import (UserModelView, AuthenticatedIndexView,
                            TagModelView, UrlModelView, PostModelView,
                            CategoryModelView)


def initialize_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.user_callback = load_user
    login_manager.login_view = "login"

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
