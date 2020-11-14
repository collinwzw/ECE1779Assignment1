from app.api import bp
from app import app
from flask import request, jsonify, render_template,session,g
import mysql.connector
from app.database import db_config
from app.api.errors import error_response as api_error_response
import cv2
import os
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from app.CloudWatch import CloudWatch
from FaceMaskDetection.pytorch_infer import inference
from app.database.dbManager import dbManager

from app.ImageHandler.model import ImageHandler

app.config['MAX_CONTENT_LENGTH'] =  1024 * 1024




def getNumberOfFilesInDatabase():
    db = dbManager.get_db()
    cursor = db.cursor()
    query = '''select count(*) from images'''
    cursor.execute(query)
    numberOfFiles = cursor.fetchall()
    return numberOfFiles[0][0]
def allowedImageType(filename):
    '''
    method to check the type of file uploaded by user
    :param filename: the uploaded filename by user
    :return: boolean. True if the image is one of allowed type, else False.
    '''
    if not "." in filename:
        return False
    ext = filename.rsplit(".",1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXETENSIONS"]:
        return True
def allowedImageFilesize(filesize):
    '''
    method to check the filesize of the image uploaded by user
    :param filesize: the uploaded filename by user
    :return: boolean. True if the image size is under limit, else False.
    '''
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False



@bp.route('/upload', methods=['GET','POST'])
def upload():
    '''
    controller that allow user who log in to upload image.
    :return:json responses
    '''
    CloudWatch.putHttpRequestRateByID()

    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        db = dbManager.get_db()
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM accounts WHERE username = %s"
        cursor.execute(query, (username,))
        account = cursor.fetchone()

        if account:
            # Create session data, we can access this data in other routes
            if check_password_hash(str(account['password_hash']), password):
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                session['admin_auth'] = bool(account['admin_auth'])

                if request.files:
                    if "filesize" in request.cookies:
                        if not allowedImageFilesize(request.cookies["filesize"]):
                            msg ="Filesize exceeded maximum limit!"
                            return api_error_response(413, msg)
                    image = request.files['file']
                    # get the image object
                    # check image name
                    if image.filename == '':
                        msg="Image must have a file name"
                        return api_error_response(400, msg)
                    if not allowedImageType(image.filename):
                        msg="Image is not in valid type"
                        return api_error_response(400, msg)

                    else:

                        filename = secure_filename(image.filename)
                        savePath = os.path.join(app.config["API_IMAGE_UPLOADS"], image.filename)
                        image.save(savePath)
                        output_info, processedImage = ImageHandler.faceMaskDetection(savePath)
                        numberofFaces = len(output_info)
                        numberofMasks = ImageHandler.NumberOfMask(output_info)
                        return jsonify({
                            "success": True,
                            "payload": {
                            "num_faces":numberofFaces ,
                            "num_masked": numberofMasks,
                            "num_unmasked": numberofFaces-numberofMasks}})

            else:
                # Account doesnt exist or username/password incorrect
                msg = 'Incorrect username/password!'
                return api_error_response(401, msg)
        else:
            msg = 'Incorrect username/password!'
            return api_error_response(401, msg)
    return render_template('api/autoUpload.html')


