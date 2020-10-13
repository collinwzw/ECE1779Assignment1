from app import app, mail
from flask import render_template, g, request, session, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.main import get_db
from app import db
from flask_mail import Message
from app.model import User
from app.form import LoginForm,RegisterForm,ForgetPassword


def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    mail.send(msg)

def send_password_reset_email(user):
    newpsw = "YUIOhfo33f3"
    send_email('[Face Mask Detection] Your New Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email.txt',
                                         user=user, newpsw='YUIOhfo33f3'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
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
        flash('Add USER SUCESS')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/forgot', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ForgetPassword()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            user.set_password('YUIOhfo33f3')
        flash('Your new password has been sent to your mailbox')
        return redirect(url_for('login'))
    return render_template('forgot.html', form=form)
