from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, URL


class Url(Form):
    url = StringField("url", validators=[DataRequired(), URL()])
    tags = StringField("tags", validators=[DataRequired()])
