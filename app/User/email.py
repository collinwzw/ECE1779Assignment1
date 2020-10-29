from app import app
from flask import render_template
from flask_mail import Message,Mail

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'ece1779group@gmail.com',
    MAIL_PASSWORD = 'Toronto1779'
))
mail = Mail(app)


def send_email(subject, sender, recipients, text_body):
    """method send_mail is using the model Mail in Flask-Mail to send a E-mail """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    mail.send(msg)



def send_password_reset_email(email, new_password):
    """method send_password_reset_email is used in reset_password function, it will get a new_password and
    put it in the body of Email. It uses a template email.txt to format the email body"""
    send_email('[No reply] Your New Password',
               sender='ece1779group@gmail.com',
               recipients=[email],
               text_body=render_template('email.txt', newpsw=new_password))