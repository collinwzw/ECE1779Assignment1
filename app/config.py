from app import app
import sys



sys.path.insert(1, './FaceMaskDetection')
sys.path.insert(1, './FaceMaskDetection/models')
sys.path.insert(1, './FaceMaskDetection/load_model')
sys.path.insert(1, './FaceMaskDetection/utils')

app.config["IMAGE_UPLOADS"]="C:/Users/ASUS/python-workspace/ECE1779Assignment1/app/static/img/uploads"
app.config["IMAGE_PROCESSED"]="C:/Users/ASUS/python-workspace/ECE1779Assignment1/app/static/img/processed"
app.config["API_IMAGE_UPLOADS"]="C:/Users/ASUS/python-workspace/ECE1779Assignment1/app/static/img/api_upload"