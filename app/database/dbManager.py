from flask import g,render_template
from app.database.db_config import db_config
import mysql.connector
from app.database import db_config
import sys


class dbManager:
    def __init__(self):
        self.dbconfig = db_config.db_config

    @staticmethod
    def get_db(self):
        #access to database
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = self.connect_to_database()
        return db

    @staticmethod
    def teardown_db(self,exception):
        #close the database
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    @staticmethod
    def connect_to_database(self):
        #Connect database
        return mysql.connector.connect(user=self.dbconfig['user'],
                                       password=self.dbconfig['password'],
                                       host=self.dbconfig['host'],
                                       database=self.dbconfig['database'])



    @staticmethod
    def update_data(self,table, key, new_value, conditionKey, condition, returnHTML):
        '''update date in the table with target condition'''
        db = self.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            query = "update "+table+" set "+key+" = %s WHERE "+conditionKey+" = %s"
            cursor.execute(query, (new_value, condition))
            cursor.execute("commit")
        except:
            e = sys.exc_info()
            db.rollback()
            self.teardown_db(e)
            return render_template(returnHTML, message="database error: " + str(e))



    @staticmethod
    def delete_data(self,table, target_key, condition, returnHTML):
        '''method delete data in SQL with target condition'''
        db = self.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            query = "Delete from "+table+" WHERE "+target_key+" = %s"
            cursor.execute(query, (condition))
            cursor.execute("commit")
        except:
            e = sys.exc_info()
            db.rollback()
            self.teardown_db(e)
            return render_template(returnHTML, message="database error: " + str(e))
        self.teardown_db()


    @staticmethod
    def search_data(self, table, target_key, condition, singleResult = True ):
        '''method search data in SQL with target condition'''
        db = self.get_db()
        cursor = db.cursor(dictionary=True)
        query ="SELECT * FROM " + table + " WHERE " + target_key + " = %s "
        cursor.execute(query, (condition,))
        if singleResult:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()
        return result

    @staticmethod
    def insert_data(self,table, row1, row2, row3, row4, value1, value2, value3, value4):
        '''method insert data into table of SQL'''
        db = self.get_db()
        cursor = db.cursor(dictionary=True)
        query = "Insert into "+table+" (%s, %s, %s, %s) values (%s, %s, %s, %s)"
        cursor.execute(query, (table, row1, row2, row3, row4, value1, value2, value3, value4))
        cursor.execute("commit")

    @staticmethod
    def insert_data_image(self, value1, value2, value3, value4, returnHTML):
        '''method insert data into table of SQL'''
        db = self.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            query = "Insert into images  values (%s, %s, %s, %s)"
            cursor.execute(query, ( value1, value2, value3, value4))
            cursor.execute("commit")
        except:
            e = sys.exc_info()
            db.rollback()
            self.teardown_db(e)
            return render_template(returnHTML, message="database error: " + str(e))

