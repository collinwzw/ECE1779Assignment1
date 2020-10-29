import random
import string
from app import app
from flask import render_template, g, request, session, redirect, url_for, send_from_directory, send_file
from app.main import get_db
import cv2
import os, sys
from werkzeug.utils import secure_filename
import requests
from FaceMaskDetection.pytorch_infer import inference

app.config["ALLOWED_IMAGE_EXETENSIONS"] = ["JPEG","JPG","PNG"]
app.config['MAX_IMAGE_FILESIZE'] = 512*512


def generate_filename():
    '''
    method to get filename that have not been saved in the database
    :return: integer that store number of files stored in database
    '''
    while 1:
        chars = string.ascii_letters + string.digits
        key = random.sample(chars, 10)
        keys = "".join(key)
        db = get_db()
        cursor = db.cursor()
        query = '''SELECT * FROM images WHERE filename = %s'''
        cursor.execute(query, (keys,))
        file = cursor.fetchone()
        if not file:
            return keys

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