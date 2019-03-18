""" Module contains post related forms """
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import (StringField, SubmitField, TextAreaField)
from wtforms.validators import DataRequired
from flaskblog.models import User


class PostForm(FlaskForm):
    title = StringField('TItle', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
