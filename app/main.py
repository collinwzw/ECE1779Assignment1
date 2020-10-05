from app import app
from flask import render_template, g
import mysql.connector
from app.config import db_config

def connect_to_database():
    return mysql.connector.connect(user=db_config['user'],
                                   password=db_config['password'],
                                   host=db_config['host'],
                                   database=db_config['database'])

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db


def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/') 
@app.route('/index')
def index():
    cnx = get_db()
    cursor = cnx.cursor()
    query = "SELECT UserID FROM users"
    cursor.execute(query)
    usersID = []
    for i in cursor:
        usersID.append(i)
    return usersID.__str__()

