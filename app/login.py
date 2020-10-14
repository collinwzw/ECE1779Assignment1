import random
import string
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from flask_mail import Message
from app import app, mail
from app.form import LoginForm, AddUser, ForgetPassword
from app.model import User


def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    mail.send(msg)


def send_password_reset_email(user, new_psw):
    send_email('[Face Mask Detection Password Recovery] Your New Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email.txt',
                                         user=user, newpswd=new_psw))


def gen_password():
    chars = string.ascii_letters + string.digits
    return ''.join([random.choice(chars) for i in range(10)])


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


@app.route('/adduser', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated and User.username != 'admin':
        flash('You are not admin')
        return redirect(url_for('index'))
    form = AddUser()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        flash('ADD USER SUCCESS')
        return redirect(url_for('usermanage'))
    return render_template('register.html', title='Register', form=form)

@app.route('/usermanager',methods=['GET','POST'])
def usermanager():
    if current_user.is_authenticated and User.username != 'admin':
        flash('You are not admin')
        return redirect(url_for('index'))





@app.route('/forgot', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ForgetPassword()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            new_password = gen_password()
            user.set_password(new_password)
            send_password_reset_email(user, new_password)
        flash('Your new password has been sent to your mailbox')
        return redirect(url_for('login'))
    return render_template('forgot.html', form=form)
