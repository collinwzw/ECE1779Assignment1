from app.api import bp
from flask import Flask, request, jsonify, render_template,g
import mysql.connector
from app.config import db_config
import re
from app.api.errors import error_response as api_error_response
def connect_to_database():
    return mysql.connector.connect(user=db_config['user'],
                                   password=db_config['password'],
                                   host=db_config['host'],
                                   database=db_config['database'])

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db


def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@bp.route('/register', methods=['GET'])
def auto_register():
    return render_template('api/autoRegister.html')

@bp.route('/register', methods=['POST'])
def registerResponse():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        cnx = get_db()
        cursor = cnx.cursor()
        query = '''SELECT * FROM accounts WHERE username = %s '''
        cursor.execute(query,(username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
            #return jsonify({"success": False,"errors":{"code":400,"message":msg}})
            return api_error_response(400,msg)

        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
            return api_error_response(400, msg)
        elif not username or not password:
            msg = 'Please fill out the form!'
            return api_error_response(400, msg)
        else:
            return jsonify({"success": True})
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
        return api_error_response(400, msg)
    # Show registration form with message (if any)

    return jsonify({"success": True})