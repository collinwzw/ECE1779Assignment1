from flask import Flask # creates the application object as an instance of class Flask imported from the flask package.
from flask_mail import Mail
from flask_bootstrap import Bootstrap

app = Flask(__name__) #The __name__ variable passed to the Flask class is a Python predefined variable, which is set to the name of the module in which it is used.
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'ece1779group@gmail.com',
    MAIL_PASSWORD = 'ikztppjrmazekwly'
))
mail = Mail(app)
bootstrap = Bootstrap(app)

app.secret_key = 'ece1779a1'


from app import main
from app import image
from app import login
from app import config

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')

app.run('0.0.0.0',5000,debug=False)