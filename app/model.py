from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from app.main import get_db


class User(UserMixin):
    pass

# @login.user_loader
# def load_user(id):
#     return User.get_id(id)
