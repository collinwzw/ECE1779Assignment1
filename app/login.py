from app import app
from flask import render_template, g, request, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from flask_mail import Message
from app import mail
from wtforms import Form, StringField, PasswordField, validators, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from flask_login import UserMixin, login_user, logout_user, current_user, login_required
from flask_login import LoginManager
import mysql.connector
from app.config import db_config
from app.main import get_db


class User(UserMixin, db_config):
    username = db_config


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class RegisterForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password1 = PasswordField('Password', validators=[DataRequired(message='Not Allowed Empty Password')])
    password2 = PasswordField('Please Repeat Password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField('Register')

    def validate_username(self, username):  # validate if this username is occupied
        pass  # wait for mysql import

    def validate_email(self, email):  # validate if the email is used
        pass


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


class ForgetPassword(FlaskForm):
    username = StringField('Please input your Username', validators=[DataRequired(message='Empty Username')])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset your Password')

    def validate_username(self, username):  # validate if this username is in mysql
        pass  # wait for mysql import

    def validate_email(self, email):  # validate if the email is in mysql
        pass


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        db = get_db()
        cursor = db.cursor(dictionary=True)
        query = "SELECT username from accounts"  # Need to fix the query
        cursor.execute(query, username)
        user = cursor.fetchone()
        if user is None:
            flash("User doesn't exist")       # Need to fix the query
            return redirect(url_for('login'))
        else:
            query = "SELECT password from accounts"
            cursor.execute(query, user)
            password = cursor.fetchone()
            if User.check_password(password):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
