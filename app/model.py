from app import app
from datetime import datetime
from app.database.dbManager import dbManager
import app.config
def record_requests():
    try:
        dbManager.insert_date_time(app.config.instanceID,datetime.now(),returnHTML=None)
    except Exception as e:
        print(e)