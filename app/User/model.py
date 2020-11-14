from app.database.dbManager import dbManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, redirect, url_for, session
from app.database.dbManager import dbManager
import string, random


class LoginSystem:
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






