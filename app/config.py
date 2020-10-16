from app import app
import sys
db_config = {'user': 'root',
             'password': 'ece1779pass',
             'host': '127.0.0.1',
             'database': 'ece1779a1'}

sys.path.insert(1, '/home/ubuntu/Desktop/ECE1779Assignment1/FaceMaskDetection')
sys.path.insert(1, '/home/ubuntu/Desktop/ECE1779Assignment1/FaceMaskDetection/models')
sys.path.insert(1, '/home/ubuntu/Desktop/ECE1779Assignment1/FaceMaskDetection/load_model')
sys.path.insert(1, '/home/ubuntu/Desktop/ECE1779Assignment1/FaceMaskDetection/utils')

app.config["IMAGE_UPLOADS"]="/home/ubuntu/Desktop/ECE1779Assignment1/app/static/img/uploads"
app.config["IMAGE_PROCESSED"]="/home/ubuntu/Desktop/ECE1779Assignment1/app/static/img/processed"