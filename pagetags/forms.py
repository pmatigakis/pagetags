from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, URL


class Url(Form):
    title = StringField("title", validators=[DataRequired()])
    url = StringField("url", validators=[DataRequired(), URL()])
    tags = StringField("tags", validators=[DataRequired()])


class Login(Form):
    username = StringField("username", validators=[DataRequired()])
    password = StringField("password", validators=[DataRequired()])
