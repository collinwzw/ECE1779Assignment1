from app import app
from flask import render_template, g, request, session, redirect, url_for
import mysql.connector
from app.config import db_config
import re


def connect_to_database():
    #Connect database
    return mysql.connector.connect(user=db_config['user'],
                                   password=db_config['password'],
                                   host=db_config['host'],
                                   database=db_config['database'])


def get_db():
    #access to database
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db


def teardown_db(exception):
    #close the database
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/') 
@app.route('/index')
def index():
    """Controller will assert user status, if user is already login, it will redirect to /home,
    else Controller will return the mail.html"""
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return redirect('home')
    # User is not loggedin redirect to login pa ge
    return render_template("main.html")


@app.route('/home')
def home():
    # Check if user is admin
    if "loggedin" in session:
        # User is loggedin show them the homeadmin page
        return render_template('home.html', username=session['username'],auth=session['admin_auth'])
    # User is not loggedin redirect to login page
    else:
        return redirect(url_for('login'))


