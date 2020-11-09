import random
import string
from app import app
from flask import render_template, g, request, session, redirect, url_for, send_from_directory, send_file
from app.database.dbManager import dbManager
import cv2

import os, sys, shutil
from FaceMaskDetection.pytorch_infer import inference
import os, shutil
app.config["ALLOWED_IMAGE_EXETENSIONS"] = ["JPEG","JPG","PNG"]
app.config['MAX_IMAGE_FILESIZE'] = 512*512

class ImageHandler:
    @staticmethod
    def generate_filename():
        '''
        method to get filename that have not been saved in the database
        :return: integer that store number of files stored in database
        '''
        while 1:
            chars = string.ascii_letters + string.digits
            key = random.sample(chars, 10)
            keys = "".join(key)
            dbm = dbManager();
            db = dbm.get_db()
            cursor = db.cursor()
            query = '''SELECT * FROM images WHERE filename = %s'''
            cursor.execute(query, (keys,))
            file = cursor.fetchone()
            if not file:
                return keys

    @staticmethod
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

    @staticmethod
    def processImage(filename):
        try:
            output_info, processedImage = ImageHandler.faceMaskDetection(filename)
        except:
            e = sys.exc_info()
            return render_template("imageManager/imageUpload.html",
                                   message="Image could not be processed correctly" + str(e))
        numberofFaces = len(output_info)
        numberofMasks = ImageHandler.NumberOfMask(output_info)
        finafilename = ImageHandler.generate_filename()
        finafilename = finafilename + '.' + filename.rsplit(".", 1)[1]
        return numberofFaces, numberofMasks, finafilename, processedImage
    @staticmethod
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

    @staticmethod
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

    @staticmethod
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


@staticmethod
def deleteAllImages():
    folder = app.config["IMAGE_PROCESSED"]
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))