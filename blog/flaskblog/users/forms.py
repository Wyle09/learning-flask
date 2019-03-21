""" Module contains User related forms. """
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import (
    DataRequired, Length, Email, EqualTo, ValidationError)
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    """ Registration form class """
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):  # username = form.username
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken, please choose another one')

    def validate_email(self, email):  # email = form.email
        user_email = User.query.filter_by(email=email.data).first()
        if user_email:
            raise ValidationError(
                'That username is taken, please choose another one')


class LoginForm(FlaskForm):
    """ Login Form class """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Rember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """ Account update form class """
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):  # username = form.username
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is taken, please choose another one')

    def validate_email(self, email):  # email = form.email
        if email.data != current_user.email:
            user_email = User.query.filter_by(email=email.data).first()
            if user_email:
                raise ValidationError(
                    'That username is taken, please choose another one')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first
        if user is None:
            raise ValidationError("There is no account with that email."
                                  "You must register first.")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                        DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
