from app import app, mail
import random
import string
from flask import render_template, g, request, session, redirect, url_for, flash
from app.main import get_db
from flask_mail import Message
from app.form import LoginForm,ChangePassword, Forgot, AddUserForm
from werkzeug.security import generate_password_hash


def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    mail.send(msg)


def generate_password():
    chars=string.ascii_letters+string.digits
    key = random.sample(chars,10)
    keys = "".join(key)
    return keys


def send_password_reset_email(email, new_password):
    send_email('[Face Mask Detection] Your New Password',
               sender=app.config['ADMINS'][0],
               recipients=[email],
               text_body=render_template('email.txt', newpsw=new_password))


def is_admin(username):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    query = "SELECT count(1) FROM accounts WHERE username = %s and admin_auth = 1"
    cursor.execute(query, (username,))
    auth = cursor.fetchone()
    return bool(auth)


def delete_user(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    query = "Delete from accounts WHERE id = %s"
    cursor.execute(query, (id,))
    commit = "commit"
    cursor.execute(commit)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "GET":
        return render_template('login.html', title='Sign In', form=form)
    if request.method == "POST":
        if 'loggedin' in session:
            return redirect(url_for('index'))

        if form.validate_on_submit():
            username = form.username.data
            password_hash = form.password.data
            db = get_db()
            cursor = db.cursor(dictionary=True)
            query = "SELECT * FROM accounts WHERE username = %s AND password_hash = %s"
            cursor.execute(query, (username, password_hash))
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                session['admin_auth'] = is_admin(username)
            else:
                flash('Invalid username or password')
                return redirect(url_for('login'))
            # login_user(username, remember=form.remember_me.data)
            return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('message',None)
    session.pop('admin_auth',None)
    # Redirect to login page
    return redirect(url_for('login'))


@app.route('/forgot', methods=['GET', 'POST'])
def reset_password():
    form = Forgot()
    if form.validate_on_submit():
        useremail = form.email.data
        db = get_db()
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM accounts WHERE email"
        cursor.execute(query, useremail)
        mail_exist = cursor.fetchone()

        if mail_exist:
            new_password = generate_password()
            new_password_hash = generate_password_hash(new_password)
            db = get_db()
            cursor = db.cursor(dictionary=True)
            query = "update accounts set password_hash= %s WHERE email= %s"
            cursor.execute(query, (new_password_hash, useremail))
            send_password_reset_email(useremail,new_password)
            flash('Your new password has been sent to your mailbox')
            return redirect(url_for('login'))
        else:
            flash('This email address is not registered')
            return redirect('index')
    return render_template('forgot.html', form=form)


@app.route('/changemypassword', methods=['POST', 'GET'])
def change_my_password():
    form = ChangePassword()
    if form.validate_on_submit():
        username = form.username.data
        old_password_hash = generate_password_hash(form.password.data)
        new_password_hash = generate_password_hash(form.password1.data)
        db = get_db()
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM accounts WHERE username = %s AND password_hash = %s"
        cursor.execute(query, (username, old_password_hash))
        account = cursor.fetchone()

        if account:
            db= get_db()
            cursor = db.cursor(dictionary=True)
            query = "update accounts set password_hash= %s WHERE username= %s"
            cursor.execute(query, (new_password_hash, username))
            flash('Your password has been changed')
            return redirect(url_for('login'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('changemypassword'))
    return render_template('changemypassword.html', form = form)


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
                return redirect(url_for('login'))
            else:
                db = get_db()
                cursor = db.cursor(dictionary=True)
                cursor.execute("Insert into accounts (username, password_hash, email,admin_auth) "
                               "values (%s, %s, %s, %s)", (username, password_hash, email,admin_auth))
                cursor.execute("commit")
                flash("You have add a new user successfully")
                return redirect(url_for('index'))

    else:
        flash('You are not an admin')
        return redirect(url_for('login'))

    return render_template('adduser.html', title='Add New User', form=form)


@app.route('/admin/usermanager', methods =['GET','POST'])
def userManager():
    print(session)
    if session.get('admin_auth'):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute('Select  id, username , email  from accounts')
        user_table = cursor.fetchall()
        return render_template('usermanager.html', usertable=user_table)
    else:
        flash('You are not an admin')
        return redirect(url_for('login'))



@app.route('/admin/usermanager/deleteuser/<int:id>',methods =['GET'])
def deleteuser(id):
    if session.get('admin_auth'):
        delete_user(id)
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute('Select id, username, email from accounts')
        user_table = cursor.fetchall()
        return render_template('usermanager.html', usertable=user_table)


@app.route('/homeadmin')
def home():
    # Check if user is loggedin
    if 'loggedin' in session and session.get('admin_auth'):
        # User is loggedin show them the home page
        return render_template('homeadmin.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



