from app import app
import sys
db_config = {'user': 'root',
             'password': 'ece1779pass',
             'host': '127.0.0.1',
             'database': 'ece1779a1'}


class Config(object):
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = 'ece1779group'
    MAIL_PASSWORD = 'Toronto1779'
    ADMINS = ['ece1779group@gmail.com']


sys.path.insert(1, '/Users/qiweifu/Documents/GitHub/ECE1779Assignment1/FaceMaskDetection/FaceMaskDetection')
sys.path.insert(1, '/Users/qiweifu/Documents/GitHub/ECE1779Assignment1/FaceMaskDetection/models')
sys.path.insert(1, '/Users/qiweifu/Documents/GitHub/ECE1779Assignment1/FaceMaskDetection/load_model')
sys.path.insert(1, '/Users/qiweifu/Documents/GitHub/ECE1779Assignment1/FaceMaskDetection/utils')

app.config["IMAGE_UPLOADS"]="/Users/qiweifu/Documents/GitHub/ECE1779Assignment1/app/static/img/uploads"
app.config["IMAGE_PROCESSED"]="/Users/qiweifu/Documents/GitHub/ECE1779Assignment1/app/static/img/processed"
app.config["API_IMAGE_UPLOADS"]="/Users/qiweifu/Documents/GitHub/ECE1779Assignment1/app/static/img/api_upload"