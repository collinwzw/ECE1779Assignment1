from app.database.dbManager import dbManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, redirect, url_for, session
from app.database.dbManager import dbManager
import string, random


class User:

    @staticmethod
    def getUser(userID):
        db = dbManager()
        account = db.search_data('accounts','id' , userID)
        if account:
            return account
        return None


class LoginSystem:
    #singleton class
    __instance__ = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if LoginSystem.__instance__ == None:
            LoginSystem()
        return LoginSystem.__instance__

    def __init__(self):
        """ Virtually private constructor. """
        if LoginSystem.__instance__ != None:
            raise Exception("This class is a singleton!")
        else:
            LoginSystem.__instance__ = self
            self.db = dbManager()
            self.table = 'accounts'

    @staticmethod
    def logout_user():
        """Pop out all user status in session to logout user
        """
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)
        session.pop('message', None)
        session.pop('admin_auth', None)

    @staticmethod
    def generate_password():
        """method generate password will random a 10-length-string with numbers and letters,
        it will be used in reset_password function.
        """
        chars = string.ascii_letters + string.digits
        key = random.sample(chars, 10)
        keys = "".join(key)
        return keys

    @staticmethod
    def login_user(user):
        session['loggedin'] = True
        session['id'] = user['id']
        session['username'] = user['username']
        session['admin_auth'] = bool(user['admin_auth'])





    def verifyLogin(self, username, password):
        account = self.db.search_data(self.table,'username' , username)
        if account:
            if check_password_hash(str(account['password_hash']), password):
                # the account exist
                return account
                # if bool(account['admin_auth']):
                #     # if the user is Admin user
                #     #create Admin Object
                #     return AdminUser(account['username'], account['id'],bool(account['admin_auth']))
                # else:
                #     # if the user is Normal user
                #     #create NormalUser Object
                #     return NormalUser(account['username'], account['id'],bool(account['admin_auth']))

        return None





