from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask_login import current_user
from flask import redirect, url_for


class AuthenticatedModelView(ModelView):
    """MovelView that can be accessed when the user is authenticated"""

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))


class UserModelView(AuthenticatedModelView):
    """ModelView object for the user model"""
    can_create = False
    can_edit = False
    can_delete = True
    column_exclude_list = ['password', "jti"]


class AuthenticatedIndexView(AdminIndexView):
    """Admin index view object that required authentication to access"""

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return super(AuthenticatedIndexView, self).index()