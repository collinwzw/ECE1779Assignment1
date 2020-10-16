from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo,Length
from wtforms.validators import email_validator
from app.login import User


class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired(message='Not Allowed Empty Password')])
    password2 = PasswordField('Please Repeat Password', validators=[DataRequired(), EqualTo('password1')])
    admin_auth = BooleanField('Admin')
    submit = SubmitField('Add a new User')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Empty Username')])
    password = PasswordField('Password', validators=[DataRequired(message='Empty Password')])
    submit = SubmitField('Login')


class ChangePassword(FlaskForm):
    username = StringField('Please input your Username', validators=[DataRequired(message='Empty Username')])
    password = PasswordField('Old Password', validators=[DataRequired(message='Empty Password')])
    password1 = PasswordField('New Password', )
    password2 = PasswordField('Please Repeat Password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField('Reset your Password')


class Forgot(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset your Password')