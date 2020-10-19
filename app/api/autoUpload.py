import requests
from app.api import bp
from app import app
from flask import Flask, request, jsonify, render_template,session,g, redirect
import mysql.connector
from app.config import db_config
from app.api.errors import error_response as api_error_response
import cv2
import os, sys
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.security import generate_password_hash,check_password_hash

from FaceMaskDetection.pytorch_infer import inference
from FaceMaskDetection.utils import anchor_decode,anchor_generator

#app.config['MAX_CONTENT_LENGTH'] = 0.01 * 1024 * 1024


def connect_to_database():
    return mysql.connector.connect(user=db_config['user'],
                                   password=db_config['password'],
                                   host=db_config['host'],
                                   database=db_config['database'])

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db


def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def getNumberOfFilesInDatabase():
    db = get_db()
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

def faceMaskDetection(readFilePath):
    '''
    This method read the original image uploaded by user and return the processed image with
    data
    :param readFilePath:
    :return: information of # of faces/masks and image itself
    '''

    img = cv2.imread(readFilePath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    output_info, image = inference(img, show_result=False, target_shape=(360, 360))

    #cv2.imwrite(saveFilePath, image)
    return output_info,image

def NumberOfMask(outputList):
    '''
    This method read the raw data output from pytorch_infer.py and determine
    number of faces with masks
    :param outputList:
    :return:
    '''
    result = 0
    for outputInfor in outputList:
        if outputInfor[0] == 0:
            result = result + 1
    return result


@bp.route('/upload', methods=['GET','POST'])
def upload():
    '''
    controller that allow user who log in to upload image.
    :return:json responses
    '''
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        db = get_db()
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
                        output_info, processedImage = faceMaskDetection(savePath)
                        numberofFaces = len(output_info)
                        numberofMasks = NumberOfMask(output_info)
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


