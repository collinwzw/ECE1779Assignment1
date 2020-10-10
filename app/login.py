from app import app
from flask import render_template, g, request, session, redirect, url_for
from flask_wtf import FlaskForm
from flask_mail import Message
from app import mail
from wtforms import Form,StringField,PasswordField,validators,BooleanField,SubmitField
from wtforms.validators import ValidationError,DataRequired,Email,EqualTo,Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
import mysql.connector
from app.config import db_config


class User(UserMixin,db_config):
    username = db_config
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)


class RegisterForm(Form):
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Email Address',validators=[DataRequired(),Email()])
    password1 = PasswordField('Password',validators=[DataRequired(message='Not Allowed Empty Password')])
    password2 = PasswordField('Please Repeat Password',validators=[DataRequired(),EqualTo('password1')])
    submit = SubmitField('Register')

    def validate_username(self,username):  # validate if this username is occupied
        pass   # wait for mysql import

    def validate_email(self,email):  # validate if the email is used
        pass


class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(message='Empty Username')])
    password = PasswordField('Password',validators=[DataRequired(message='Empty Password')])
    submit = SubmitField('Login')


class ChangePassword(FlaskForm):
    username = StringField('Please input your Username',validators=[DataRequired(message='Empty Username')])
    password = PasswordField('Old Password',validators=[DataRequired(message='Empty Password')])
    password1 = PasswordField('New Password',)
    password2 = PasswordField('Please Repeat Password',validators=[DataRequired(),EqualTo('password1')])
    submit = SubmitField('Reset your Password')


class ForgetPassword(FlaskForm):
    username = StringField('Please input your Username', validators=[DataRequired(message='Empty Username')])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset your Password')

    def validate_username(self,username):  # validate if this username is in mysql
        pass   # wait for mysql import

    def validate_email(self,email):  # validate if the email is in mysql
        pass


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title='Sign In', form=LoginForm())








