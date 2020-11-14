from app import app
import sys
from ec2_metadata import ec2_metadata
sys.path.insert(1, './FaceMaskDetection')
sys.path.insert(1, './FaceMaskDetection/models')
sys.path.insert(1, './FaceMaskDetection/load_model')
sys.path.insert(1, './FaceMaskDetection/utils')

app.config["IMAGE_UPLOADS"]="./app/static/img/uploads"
app.config["IMAGE_PROCESSED"]="./app/static/img/processed"
app.config["IMAGE_SEND"]="./static/img/processed"
app.config["API_IMAGE_UPLOADS"]="./app/static/img/api_upload"
instanceID = ec2_metadata.instance_id