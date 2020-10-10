from flask import Flask # acreates the application object as an instance of class Flask imported from the flask package.
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap

app = Flask(__name__) #The __name__ variable passed to the Flask class is a Python predefined variable, which is set to the name of the module in which it is used.
login = LoginManager(app)  #create and initialize login in app
mail = Mail(app)
bootstrap = Bootstrap(app)


app.secret_key = 'ece1779a1'

from app import main

from app import image

from app import login

from app import config
