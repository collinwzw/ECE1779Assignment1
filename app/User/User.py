
from flask import render_template, request, redirect, url_for, session
from flask_classy import FlaskView,route

from app.database.dbManager import dbManager

class User:
    @staticmethod
    def getUser(userID):
        db = dbManager()
        account = db.search_data('accounts','id' , userID)
        if account:
            return account
        return None







    # def generate_password():
    #     """method generate password will random a 10-length-string with numbers and letters,
    #     it will be used in reset_password function.
    #     """
    #     chars = string.ascii_letters + string.digits
    #     key = random.sample(chars, 10)
    #     keys = "".join(key)
    #     return keys
    #
    #
    # def delete_user(userid):
    #     """method delete user is to access to the database and find userid and delete this row"""
    #     db = get_db()
    #     cursor = db.cursor(dictionary=True)
    #     query = "Delete from accounts WHERE id = %s"
    #     cursor.execute(query, (userid,))
    #     commit = "commit"
    #     cursor.execute(commit)