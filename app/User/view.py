from app import app
from flask import render_template, request, session, redirect, url_for, flash
from app.database.dbManager import  dbManager
from flask_mail import Message
from app.User.form import LoginForm, ChangePassword, ResetPassword, AddUserForm
from werkzeug.security import generate_password_hash, check_password_hash
from app.User.model import LoginSystem
from app.User.email import send_password_reset_email
from app.CloudWatch import CloudWatch

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
    CloudWatch.putHttpRequestRateByID()
    form = LoginForm()
    if request.method == "GET":
        return render_template('userManager/login.html', title='Sign In', form=form)
    if request.method == "POST":
        if 'loggedin' in session:
            return redirect(url_for('home'))
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            account = dbManager.check_username(username)
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
    CloudWatch.putHttpRequestRateByID()
    LoginSystem.logout_user()
    """Controller pop the login status and user information in session, then redirect to index page"""
    return redirect(url_for('index'))


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    """Controller that display the reset_password page. Only user_email is needed to be input.
    Controller will validate the email in database and generate a new password 10-lenght-random string.
    Then it will try to send a email with new password to user's mailbox by gmail.
    Email template is email.txt"""
    CloudWatch.putHttpRequestRateByID()
    form = ResetPassword()
    database = dbManager()
    if form.validate_on_submit():
        user_email = form.email.data
        mail_exist = database.check_email(user_email)
        if mail_exist:
            new_password = LoginSystem.generate_password()
            new_password_hash = generate_password_hash(new_password)
            dbManager.update_password_mail(new_password_hash,user_email)
            flash('Your new password has been sent to your mailbox')
            redirect('login')
            send_password_reset_email(user_email, new_password)
            return redirect(url_for('login'))
        else:
            flash('This email address is not registered')
            return redirect('reset_password')
    return render_template('userManager/resetpassword.html', form=form)


@app.route('/change_my_password', methods=['POST', 'GET'])
def change_my_password():
    """Controller is allow user to change their password if they have valid username and password.
    It will generate the new password hash and write into the database.
    If username not exist, or wrong password, controller will not allow user change password.
     """
    CloudWatch.putHttpRequestRateByID()
    form = ChangePassword()
    if request.method == 'GET':
        return render_template('changemypassword.html', form=form)
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        old_password = form.password.data
        new_password_hash = generate_password_hash(form.password1.data)
        account=dbManager.check_username(username)
        if account:
            if check_password_hash(str(account['password_hash']), old_password):
                dbManager.update_password_username(new_password_hash,username)
                flash('Your password has been changed')
                return redirect(url_for('login'))
            else:
                flash('Invalid username or password')
                return redirect(url_for('change_my_password'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('change_my_password'))
    else:
        return render_template('userManager/changemypassword.html', form=form)


@app.route('/admin/adduser', methods=['GET', 'POST'])
def add_new_user():
    """controller will allow admin user to add new user.
    It will assert if user is admin by admin_auth. if it is normal user, it will redirect to login page
    When admin add new user, if same username or email in database, it will refuse to create new user
    Admin also allow to create another admin by input admin_auth True"""
    CloudWatch.putHttpRequestRateByID()
    if session.get('admin_auth'):
        form = AddUserForm()
        if form.validate_on_submit():
            username = form.username.data
            password_hash = generate_password_hash(form.password1.data)
            email = form.email.data
            admin_auth = form.admin_auth.data
            account = dbManager.check_exist(username,email)
            if account:
                flash('This User name or Email is existing')
                return redirect(url_for('add_new_user'))
            else:
                dbManager.add_user(username,password_hash,email,admin_auth)
                flash("You have add a new user successfully")
                return redirect(url_for('add_new_user'))
    else:
        flash('You are not an admin')
        return redirect(url_for('login'))
    return render_template('userManager/adduser.html', title='Add New User', form=form)


@app.route('/admin/usermanager', methods=['GET', 'POST'])
def userManager():
    """Controller allows admin user to review all users in system.
    Controller will go to database and show all users by user_table:(id ,username ,email)
    Botton on the html will allow admin to delete users.
    """
    CloudWatch.putHttpRequestRateByID()
    if session.get('admin_auth'):
        user_table = dbManager.show_account()
        return render_template('userManager/usermanager.html', usertable=user_table)
    else:
        flash('You are not an admin')
        return redirect(url_for('home'))


@app.route('/admin/usermanager/deleteuser/<int:id>', methods=['GET'])
def deleteuser(id):
    """Controller allows admin to delect users
    Controller get the user's id by GET method <int:id>
    Controller will access to database and delete the row of user by using delete_user(id)"""
    CloudWatch.putHttpRequestRateByID()
    if session.get('admin_auth'):
        dbManager.delete_user(id)
        user_table = dbManager.show_account()
        return render_template('userManager/usermanager.html', usertable=user_table)
