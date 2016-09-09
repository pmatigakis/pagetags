from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, URL, Length

from pagetags.models import Post, Url


class Url(Form):
    title = StringField("title", validators=[DataRequired(),
                                             Length(max=Post.TITLE_LENGTH)])
    url = StringField("url", validators=[DataRequired(), URL(),
                                         Length(max=Url.URL_LENGTH)])
    tags = StringField("tags", validators=[DataRequired()])


class Login(Form):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
