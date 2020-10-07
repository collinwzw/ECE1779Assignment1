from flask import Flask # creates the application object as an instance of class Flask imported from the flask package.


app = Flask(__name__) #The __name__ variable passed to the Flask class is a Python predefined variable, which is set to the name of the module in which it is used.


from app import main