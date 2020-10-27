from flask import g
from app.database.db_config import db_config
import mysql.connector



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


def connect_to_database():
    #Connect database
    return mysql.connector.connect(user=db_config['user'],
                                   password=db_config['password'],
                                   host=db_config['host'],
                                   database=db_config['database'])