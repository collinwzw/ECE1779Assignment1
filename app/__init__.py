from flask import Flask # creates the application object as an instance of class Flask imported from the flask package.
from flask_bootstrap import Bootstrap

app = Flask(__name__) #The __name__ variable passed to the Flask class is a Python predefined variable, which is set to the name of the module in which it is used.

bootstrap = Bootstrap(app)

app.secret_key = 'ece1779a1'


from app import main
from app import config
from app.ImageHandler import view

from app.User import login
from app.api import bp as api_bp



app.register_blueprint(api_bp, url_prefix='/api')



app.run('0.0.0.0',5000,debug=True)