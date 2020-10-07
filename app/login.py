from app import app
from flask import render_template, g, request, session, redirect, url_for
import mysql.connector
from app.config import db_config

class login:
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        msg = ''
        # Output message if something goes wrong...
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            db = get_db()
            cursor = db.cursor(dictionary=True)
            query = "SELECT * FROM accounts WHERE username = %s AND password = %s"
            cursor.execute(query,(username,password))
            account = cursor.fetchone()

            if account:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                # Redirect to home page
                return redirect(url_for('home'))
            else:
                # Account doesnt exist or username/password incorrect
                msg = 'Incorrect username/password!'
        # Show the login form with message (if any)
        return render_template('login.html', msg=msg)