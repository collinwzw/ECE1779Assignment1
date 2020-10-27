from app import app
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


class emailManager:
    def send_email(subject, sender, recipients, text_body):
        """method send_mail is using the model Mail in Flask-Mail to send a E-mail """
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = text_body
        mail.send(msg)