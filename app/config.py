# db_config = {'user': 'root',
#              'password': 'ece1779',
#              'host': '127.0.0.1',
#              'database': 'ece1779a1'}

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'ece1779a1.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = 'ece1779group'
    MAIL_PASSWORD = 'Toronto1779'
    ADMINS = ['ece1779group@gmail.com']