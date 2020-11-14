from flask import g,render_template
from app.database.db_config import db_config
import mysql.connector
from app.database import db_config
import sys
from app.database.db_config import db_config


class dbManager:

    @staticmethod
    def get_db():
        #access to database
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = dbManager.connect_to_database()
        return db

    @staticmethod
    def teardown_db(exception):
        #close the database
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    @staticmethod
    def connect_to_database():
        #Connect database
        return mysql.connector.connect(user=db_config['user'],
                                       password=db_config['password'],
                                       host=db_config['host'],
                                       database=db_config['database'])



    @staticmethod
    def update_data(table, key, new_value, conditionKey, condition, returnHTML):
        '''update date in the table with target condition'''
        db = dbManager.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            query = "update "+table+" set "+key+" = %s WHERE "+conditionKey+" = %s"
            cursor.execute(query, (new_value, condition))
            cursor.execute("commit")
        except:
            e = sys.exc_info()
            db.rollback()
            dbManager.teardown_db(e)
            return render_template(returnHTML, message="database error: " + str(e))



    @staticmethod
    def delete_data(table, target_key, condition, returnHTML):
        '''method delete data in SQL with target condition'''
        db = dbManager.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            query = "Delete from "+table+" WHERE "+target_key+" = %s"
            cursor.execute(query, (condition))
            cursor.execute("commit")
        except:
            e = sys.exc_info()
            db.rollback()
            dbManager.teardown_db(e)
            return render_template(returnHTML, message="database error: " + str(e))


    @staticmethod
    def search_data(table, target_key, condition, singleResult = True ):
        '''method search data in SQL with target condition'''
        db = dbManager.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            query = "SELECT * FROM " + table + " WHERE " + target_key + " = %s "
            cursor.execute(query, (condition,))
            if singleResult:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
            return result
        except:
            e = sys.exc_info()
            db.rollback()
            dbManager.teardown_db(e)
            return render_template("error.html", message="database error: " + str(e))

    @staticmethod
    def check_email(user_email):
        db = dbManager.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            query = "SELECT * FROM accounts WHERE email= %s"
            cursor.execute(query, (user_email,))
            mail_exist = cursor.fetchone()
            return mail_exist
        except:
            e = sys.exc_info()
            db.rollback()
            dbManager.teardown_db(e)
            return render_template("error.html", message="database error: " + str(e))

    @staticmethod
    def check_username(username):
        db = dbManager.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            query = "SELECT * FROM accounts WHERE username = %s"
            cursor.execute(query, (username,))
            account = cursor.fetchone()
            return account
        except:
            e = sys.exc_info()
            db.rollback()
            dbManager.teardown_db(e)
            return render_template("error.html", message="database error: " + str(e))

    @staticmethod
    def check_exist(username,email):
        db = dbManager.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            query = "SELECT * FROM accounts WHERE username = %s or email = %s"
            cursor.execute(query, (username, email))
            account = cursor.fetchone()
            return account
        except:
            e = sys.exc_info()
            db.rollback()
            dbManager.teardown_db(e)
            return render_template("error.html", message="database error: " + str(e))


    @staticmethod
    def update_password_mail(new_password_hash,user_email):
        db = dbManager.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            query = "update accounts set password_hash= %s WHERE email= %s"
            cursor.execute(query, (new_password_hash, user_email))
            cursor.execute("commit")
        except:
            e = sys.exc_info()
            db.rollback()
            dbManager.teardown_db(e)
            return render_template("error.html", message="database error: " + str(e))


    @staticmethod
    def update_password_username(new_password_hash,username):
        db = dbManager.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            query = "update accounts set password_hash= %s WHERE username= %s"
            cursor.execute(query, (new_password_hash, username))
            cursor.execute("commit")
        except:
            e = sys.exc_info()
            db.rollback()
            dbManager.teardown_db(e)
            return render_template("error.html", message="database error: " + str(e))


    @staticmethod
    def add_user(username, password_hash, email, admin_auth):
        db = dbManager.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("Insert into accounts (username, password_hash, email,admin_auth) "
                           "values (%s, %s, %s, %s)", (username, password_hash, email, admin_auth))
            cursor.execute("commit")
        except:
            e = sys.exc_info()
            db.rollback()
            dbManager.teardown_db(e)
            return render_template("error.html", message="database error: " + str(e))



    @staticmethod
    def show_account():
        db = dbManager.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute('Select  id, username , email  from accounts')
            user_table = cursor.fetchall()
            return user_table
        except:
            e = sys.exc_info()
            db.rollback()
            dbManager.teardown_db(e)
            return render_template("error.html", message="database error: " + str(e))


    @staticmethod
    def delete_user(userid):
        """method delete user is to access to the database and find userid and delete this row"""
        db = dbManager.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            query = "Delete from accounts WHERE id = %s"
            cursor.execute(query, (userid,))
            cursor.execute("commit")
        except:
            e = sys.exc_info()
            db.rollback()
            dbManager.teardown_db(e)
            return render_template("error.html", message="database error: " + str(e))

    @staticmethod
    def insert_data(self,table, row1, row2, row3, row4, value1, value2, value3, value4):
        '''method insert data into table of SQL'''
        db = dbManager.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            query = "Insert into " + table + " (%s, %s, %s, %s) values (%s, %s, %s, %s)"
            cursor.execute(query, (table, row1, row2, row3, row4, value1, value2, value3, value4))
            cursor.execute("commit")
        except:
            e = sys.exc_info()
            db.rollback()
            dbManager.teardown_db(e)
            return render_template("error.html", message="database error: " + str(e))


    @staticmethod
    def insert_data_image(value1, value2, value3, value4, returnHTML):
        '''method insert data into table of SQL'''
        db = dbManager.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            query = "Insert into images  values (%s, %s, %s, %s)"
            cursor.execute(query, ( value1, value2, value3, value4))
            cursor.execute("commit")
        except:
            e = sys.exc_info()
            db.rollback()
            dbManager.teardown_db(e)
            return render_template(returnHTML, message="database error: " + str(e))

    @staticmethod
    def insert_date_time(instanceID, datetime, returnHTML):
        '''method insert data into table of SQL'''
        db = dbManager.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            #query = "Insert into requests_table  values (%s, %s)"
            #cursor.execute(query, ( instanceID, datetime,))
            #cursor.execute("commit")
            query = "select * from requests_table"
            cursor.execute(query)
            print(cursor)
        except:
            e = sys.exc_info()
            db.rollback()
            dbManager.teardown_db(e)
            return render_template(returnHTML, message="database error: " + str(e))