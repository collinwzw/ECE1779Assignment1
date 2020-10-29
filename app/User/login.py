from app import app
from flask import render_template, request, session, redirect, url_for, flash
from app.database.dbManager import  dbManager
from flask_mail import Message
from app.User.form import LoginForm, ChangePassword, ResetPassword, AddUserForm
from werkzeug.security import generate_password_hash, check_password_hash
from app.User.LoginSystem import LoginSystem

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Controller that display the login page.controller that display the imageView page.
    This controller will assert if user is already logged in or not.
    If yes, it will redirect to home page.
    If no, it will show the login page and let user input username and password.
    Once user submit the username and password, it will go to dababase and verify them.
    If login success, user id, username, admin_auth will be save in session
    account: assert if username is in database.
    """
    form = LoginForm()
    if request.method == "GET":
        return render_template('userManager/login.html', title='Sign In', form=form)
    if request.method == "POST":
        if 'loggedin' in session:
            return redirect(url_for('home'))
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            loginsystem = LoginSystem.getInstance()
            user = loginsystem.verifyLogin(username,password)
            session['loggedin'] = True
            session['id'] = user['id']
            session['username'] = user['username']
            session['admin_auth'] = bool(user['admin_auth'])
            if user:
                flash('Login successfully!')
                return redirect(url_for('home'))
            else:
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
    Controller will validate the email in database and generate a new password 10-lenght-random string.
    Then it will try to send a email with new password to user's mailbox by gmail.
    Email template is email.txt"""
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
    """Controller is allow user to change their password if they have valid username and password.
    It will generate the new password hash and write into the database.
    If username not exist, or wrong password, controller will not allow user change password.
     """
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
    """controller will allow admin user to add new user.
    It will assert if user is admin by admin_auth. if it is normal user, it will redirect to login page
    When admin add new user, if same username or email in database, it will refuse to create new user
    Admin also allow to create another admin by input admin_auth True"""
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
    """Controller allows admin user to review all users in system.
    Controller will go to database and show all users by user_table:(id ,username ,email)
    Botton on the html will allow admin to delete users.
    """
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
    """Controller allows admin to delect users
    Controller get the user's id by GET method <int:id>
    Controller will access to database and delete the row of user by using delete_user(id)"""
    if session.get('admin_auth'):
        delete_data('account', 'id', id)
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute('Select id, username, email from accounts')
        user_table = cursor.fetchall()
        return render_template('usermanager.html', usertable=user_table)
