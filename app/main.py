from app import app
from flask import render_template, request, redirect, url_for, session
from app.User.model import User

@app.route('/')
@app.route('/index')
def index():
    """Controller will assert user status, if user is already login, it will redirect to /home,
    else Controller will return the mail.html"""

        # User is loggedin show them the home page

    # User is not loggedin redirect to login pa ge
    return render_template("main.html")


@app.route('/home')
def home():
    # Check if user is admin
    user = User.getUser(session['id'])
    if user:
        # User is loggedin show them the homeadmin page
        return render_template('home.html', username=user['username'],auth=user['admin_auth'])
    # User is not loggedin redirect to login page
    else:
        return redirect(url_for('login'))


