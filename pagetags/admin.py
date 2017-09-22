from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask_login import current_user
from flask import redirect, url_for

from pagetags.models import User, Tag, Url, Post, Category


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

    def __init__(self, session, *args, **kwargs):
        super(AuthenticatedModelView, self).__init__(
            User, session, *args, **kwargs)


class AuthenticatedIndexView(AdminIndexView):
    """Admin index view object that required authentication to access"""

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return super(AuthenticatedIndexView, self).index()


class TagModelView(AuthenticatedModelView):
    form_columns = ["name"]
    can_create = False
    can_edit = True
    can_delete = True

    def __init__(self, session, *args, **kwargs):
        super(TagModelView, self).__init__(Tag, session, *args, **kwargs)


class UrlModelView(AuthenticatedModelView):
    form_columns = ["url"]
    can_create = False
    can_edit = True
    can_delete = True

    def __init__(self, session, *args, **kwargs):
        super(UrlModelView, self).__init__(Url, session, *args, **kwargs)


class PostModelView(AuthenticatedModelView):
    form_excluded_columns = ["post_categories", "added_at"]
    can_create = False
    can_edit = True
    can_delete = True

    def __init__(self, session, *args, **kwargs):
        super(PostModelView, self).__init__(Post, session, *args, **kwargs)


class CategoryModelView(AuthenticatedModelView):
    form_columns = ["name"]
    can_create = True
    can_edit = True
    can_delete = True

    def __init__(self, session, *args, **kwargs):
        super(CategoryModelView, self).__init__(
            Category, session, *args, **kwargs)
