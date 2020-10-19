from app import app
import sys
db_config = {'user': 'root',
             'password': 'ece1779',
             'host': '127.0.0.1',
             'database': 'ece1779'}



sys.path.insert(1, 'C:/Users/ASUS/python-workspace/ECE1779Assignment1/FaceMaskDetection')
sys.path.insert(1, 'C:/Users/ASUS/python-workspace/ECE1779Assignment1/FaceMaskDetection/models')
sys.path.insert(1, 'C:/Users/ASUS/python-workspace/ECE1779Assignment1/FaceMaskDetection/load_model')
sys.path.insert(1, 'C:/Users/ASUS/python-workspace/ECE1779Assignment1/FaceMaskDetection/utils')

app.config["IMAGE_UPLOADS"]="C:/Users/ASUS/python-workspace/ECE1779Assignment1/app/static/img/uploads"
app.config["IMAGE_PROCESSED"]="C:/Users/ASUS/python-workspace/ECE1779Assignment1/app/static/img/processed"
app.config["API_IMAGE_UPLOADS"]="/home/ubuntu/Desktop/ECE1779Assignment1/app/static/img/api_upload"