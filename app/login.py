from app import app, mail
import random
import string
from flask import render_template, g, request, session, redirect, url_for, flash
from app.main import get_db
from flask_mail import Message
from app.form import LoginForm, ChangePassword, ResetPassword, AddUserForm
from werkzeug.security import generate_password_hash, check_password_hash


def send_email(subject, sender, recipients, text_body):
    """method send_mail is using the model Mail in Flask-Mail to send a E-mail """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    mail.send(msg)


def generate_password():
    """method generate password will random a 10-length-string with numbers and letters,
    it will be used in reset_password function.
    """
    chars = string.ascii_letters + string.digits
    key = random.sample(chars, 10)
    keys = "".join(key)
    return keys


def send_password_reset_email(email, new_password):
    """method send_password_reset_email is used in reset_password function, it will get a new_password and
    put it in the body of Email. It uses a template email.txt to format the email body"""
    send_email('[No reply] Your New Password',
               sender='ece1779group@gmail.com',
               recipients=[email],
               text_body=render_template('email.txt', newpsw=new_password))


def delete_user(userid):
    """method delete user is to access to the database and find userid and delete this row"""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    query = "Delete from accounts WHERE id = %s"
    cursor.execute(query, (userid,))
    commit = "commit"
    cursor.execute(commit)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Controller that display the login page.controller that display the imageView page.
    This controller will assert if user is already logged in or not.
    If yes, it will redirect to home page.
    If no, it will show the login page and let user input username and password.
    Once user submit the username and password, it will go to dababase and verify them.
    If login success, user id, username, admin_auth will be save in session
    """
    form = LoginForm()
    if request.method == "GET":
        return render_template('login.html', title='Sign In', form=form)
    if request.method == "POST":
        if 'loggedin' in session:
            return redirect(url_for('home'))
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            db = get_db()
            cursor = db.cursor(dictionary=True)
            query = "SELECT * FROM accounts WHERE username = %s"
            cursor.execute(query, (username,))
            account = cursor.fetchone()
            if account:
                if check_password_hash(str(account['password_hash']), password):
                    session['loggedin'] = True
                    session['id'] = account['id']
                    session['username'] = account['username']
                    session['admin_auth'] = bool(account['admin_auth'])
                    flash('Login successfully!')
                    return redirect(url_for('home'))
                else:
                    flash('Invalid username or password')
                    return redirect(url_for('login'))
            flash('Invalid username or password')
            return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))


@app.route('/logout')
def logout():
    """Controller pop the login status and user information in session, then redirect to index page"""
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('message', None)
    session.pop('admin_auth', None)
    return redirect(url_for('index'))


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    """Controller that display the reset_password page. Only user_email is needed to be input.
    Controller will validate the email in database and try to """
    form = ResetPassword()
    if form.validate_on_submit():
        user_email = form.email.data
        db = get_db()
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM accounts WHERE email= %s"
        cursor.execute(query, (user_email,))
        mail_exist = cursor.fetchone()
        if mail_exist:
            new_password = generate_password()
            new_password_hash = generate_password_hash(new_password)
            db = get_db()
            cursor = db.cursor(dictionary=True)
            query = "update accounts set password_hash= %s WHERE email= %s"
            cursor.execute(query, (new_password_hash, user_email))
            cursor.execute("commit")
            flash('Your new password has been sent to your mailbox')
            redirect('login')
            send_password_reset_email(user_email, new_password)
            return redirect(url_for('login'))
        else:
            flash('This email address is not registered')
            return redirect('reset_password')
    return render_template('resetpassword.html', form=form)


@app.route('/change_my_password', methods=['POST', 'GET'])
def change_my_password():
    form = ChangePassword()
    if request.method == 'GET':
        return render_template('changemypassword.html', form=form)
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        old_password = form.password.data
        new_password_hash = generate_password_hash(form.password1.data)
        db = get_db()
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM accounts WHERE username = %s"
        cursor.execute(query, (username,))
        account = cursor.fetchone()
        if account:
            if check_password_hash(str(account['password_hash']), old_password):
                db = get_db()
                cursor = db.cursor(dictionary=True)
                query = "update accounts set password_hash= %s WHERE username= %s"
                cursor.execute(query, (new_password_hash, username))
                cursor.execute("commit")
                flash('Your password has been changed')
                return redirect(url_for('login'))
            else:
                flash('Invalid username or password')
                return redirect(url_for('change_my_password'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('change_my_password'))
    else:
        return render_template('changemypassword.html', form=form)


@app.route('/admin/adduser', methods=['GET', 'POST'])
def add_new_user():
    if session.get('admin_auth'):
        form = AddUserForm()
        if form.validate_on_submit():
            username = form.username.data
            password_hash = generate_password_hash(form.password1.data)
            email = form.email.data
            admin_auth = form.admin_auth.data
            db = get_db()
            cursor = db.cursor(dictionary=True)
            query = "SELECT * FROM accounts WHERE username = %s or email = %s"
            cursor.execute(query, (username, email))
            account = cursor.fetchone()
            if account:
                flash('This User name or Email is existing')
                return redirect(url_for('add_new_user'))
            else:
                db = get_db()
                cursor = db.cursor(dictionary=True)
                cursor.execute("Insert into accounts (username, password_hash, email,admin_auth) "
                               "values (%s, %s, %s, %s)", (username, password_hash, email, admin_auth))
                cursor.execute("commit")
                flash("You have add a new user successfully")
                return redirect(url_for('add_new_user'))

    else:
        flash('You are not an admin')
        return redirect(url_for('login'))

    return render_template('adduser.html', title='Add New User', form=form)


@app.route('/admin/usermanager', methods=['GET', 'POST'])
def userManager():
    if session.get('admin_auth'):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute('Select  id, username , email  from accounts')
        user_table = cursor.fetchall()
        return render_template('usermanager.html', usertable=user_table)
    else:
        flash('You are not an admin')
        return redirect(url_for('home'))


@app.route('/admin/usermanager/deleteuser/<int:id>', methods=['GET'])
def deleteuser(id):
    if session.get('admin_auth'):
        delete_user(id)
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute('Select id, username, email from accounts')
        user_table = cursor.fetchall()
        return render_template('usermanager.html', usertable=user_table)
