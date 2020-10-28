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


def update_data(table, row, new_value, target_key, condition):
    '''update date in the table with target condition'''
    db = get_db()
    cursor = db.cursor(dictionary=True)
    query = "update %s set %s = %s WHERE %s = %s"
    cursor.execute(query, (table,row, new_value, target_key,condition ))
    cursor.execute("commit")
    teardown_db()


def delete_data(table, target_key, condition):
    '''method delete data in SQL with target condition'''
    db = get_db()
    cursor = db.cursor(dictionary=True)
    query = "Delete from %s WHERE %s = %s"
    cursor.execute(query, (table, target_key, condition))
    cursor.execute("commit")
    teardown_db()


def search_data(row, table, target_key, condition ):
    '''method search data in SQL with target condition'''
    db = get_db()
    cursor = db.cursor(dictionary=True)
    query = "SELECT %s FROM accounts WHERE username = %s"
    cursor.execute(query, (row,table,target_key,condition))
    result = cursor.fetchone()
    teardown_db()
    return result


def insert_data(table, row1, row2, row3, row4, value1, value2, value3, value4):
    '''method insert data into table of SQL'''
    db = get_db()
    cursor = db.cursor(dictionary=True)
    query = "Insert into %s (%s, %s, %s, %s) values (%s, %s, %s, %s)"
    cursor.execute(query, (table, row1, row2, row3, row4, value1, value2, value3, value4))
    cursor.execute("commit")



