from app import app
from flask import render_template, request, redirect, url_for, session
import app.model as m
from app.CloudWatch import CloudWatch
@app.route('/')
@app.route('/index')
def index():
    """Controller will assert user status, if user is already login, it will redirect to /home,
    else Controller will return the mail.html"""
    #m.record_requests()
    CloudWatch.putHttpRequestRateByID()
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return redirect('home')
    # User is not loggedin redirect to login pa ge
    return render_template("main.html")


@app.route('/home')
def home():
    # Check if user is admin
    CloudWatch.putHttpRequestRateByID()
    if "loggedin" in session:
        # User is loggedin show them the homeadmin page
        return render_template('home.html', username=session['username'],auth=session['admin_auth'])
    # User is not loggedin redirect to login page
    else:
        return redirect(url_for('login'))

