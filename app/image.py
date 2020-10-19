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
app.config['MAX_IMAGE_FILESIZE'] = 1024*1024

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

@app.route('/sendImages/<filename>/',methods = ["GET", "POST"])
def sendImages(filename):
    '''
    controller that takes filename as input, find the image in local file system
    and return the generated image by using function send_file.
    it's been called in imageUpload html file.
    :param filename: input filename
    :return: sends the contents of a file to the html
    '''
    image_path = os.path.join(app.config["IMAGE_PROCESSED"], filename)
    return send_file(image_path)

@app.route('/imageView')
def imageView():
    '''
    controller that display the imageView page.
    This controller will assert if user is already logged in or not.
    If yes, go to the database and find out all the images history belong to this user and display
    If no, it will redirect user to log in page.
    :return:
    '''
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page

        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            #db.start_transaction()
            query = '''SELECT * FROM images WHERE id = %s'''
            cursor.execute(query, (session['id'],))
        except:
            e = sys.exc_info()
            db.rollback()
            return render_template("imageUpload.html", message="database error: " + str(e))
        images = cursor.fetchall()
        noface = []
        allFaceWithMask = []
        allFaceNoMask = []
        someFaceWithMask = []
        for image in images:
            if image['numberofFaces'] == 0:
                noface.append(image)
            elif image['numberofFaces'] == image['numberofMasks']:
                allFaceWithMask.append((image))
            elif image['numberofMasks'] == 0:
                allFaceNoMask.append(image)
            else:
                someFaceWithMask.append(image)

        return render_template('imageView.html', message = "", noface = noface,allFaceWithMask = allFaceWithMask,allFaceNoMask=allFaceNoMask,someFaceWithMask=someFaceWithMask )
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



@app.route('/imageUpload', methods = ["GET", "POST"])
def imageUpload():
    '''
    controller that allow user upload image.
    This controller will assert if filesize, file type, filename and if the filename is secure.
    If it pass all assertion, the system will store the original file
    :return:
    '''
    if 'loggedin' in session:
        if request.method == "POST":
            if request.files:
                if "filesize" in request.cookies:
                    if not allowedImageFilesize(request.cookies["filesize"]):
                        print("Filesize exceeded maximum limit")
                        return render_template("imageUpload.html", message = "Filesize exceeded maximum limit")
                    #get the image object
                    image = request.files['image']
                    #check image name
                    if image.filename == '':
                        print("Image must have a file name")
                        return render_template("imageUpload.html", message = "Image must have a file name")
                    if not allowedImageType(image.filename):
                        print("Image is not in valid type")
                        return render_template("imageUpload.html", message = "Image is not in valid type")
                    else:
                        filename = secure_filename(image.filename)
                        savePath = os.path.join(app.config["IMAGE_UPLOADS"], image.filename)
                        image.save(savePath)
                        try:
                            output_info, processedImage = faceMaskDetection(savePath)
                        except:
                            e = sys.exc_info()
                            return render_template("imageUpload.html",
                                                   message="Image could not be processed correctly" + str(e))
                        numberofFaces = len(output_info)
                        numberofMasks = NumberOfMask(output_info)
                        finafilename = generate_filename()
                        finafilename =  finafilename + '.' + filename.rsplit(".",1)[1]
                        db = get_db()
                        cursor = db.cursor(dictionary=True)
                        try:
                            #db.start_transaction()
                            query ='''insert into images values (%s,%s,%s,%s)'''
                            cursor.execute(query, (session['id'],finafilename, numberofFaces,numberofMasks, ))
                            db.commit()
                            processedSavePath = os.path.join(app.config["IMAGE_PROCESSED"], finafilename)
                            cv2.imwrite(processedSavePath, cv2.cvtColor(processedImage, cv2.COLOR_RGB2BGR))
                            os.remove(savePath)
                        except:
                            e = sys.exc_info()
                            db.rollback()
                            os.remove(savePath)
                            return render_template("imageUpload.html", message="database error: " + str(e))

                    return redirect("imageView")
            elif request.form['url'] != "":
                url = request.form['url']
                if not allowedImageType(url):
                    print("Image is not in valid type")
                    return render_template("imageUpload.html", message="Image is not in valid type")
                filename = os.path.join(app.config["IMAGE_UPLOADS"], 'temp.jpeg')
                try:
                    with open(filename, 'wb') as f:
                        response = requests.get(url, stream=True)
                        for block in response.iter_content(1024):
                            if not block:
                                break
                            f.write(block)
                    print('Image sucessfully Downloaded: ')
                except:
                    e = sys.exc_info()
                    return render_template("imageUpload.html", message="Image could not be downloaded from url. Error: " + str(e))
                try:
                    output_info,processedImage = faceMaskDetection(filename)
                except:
                    e = sys.exc_info()
                    return render_template("imageUpload.html", message="Image could not be processed correctly" + str(e))
                numberofFaces = len(output_info)
                numberofMasks = NumberOfMask(output_info)
                finafilename = generate_filename()
                finafilename = finafilename + '.' + filename.rsplit(".", 1)[1]
                db = get_db()
                cursor = db.cursor(dictionary=True)
                try:
                    #db.start_transaction()
                    query ='''insert into images values (%s,%s,%s,%s)'''
                    cursor.execute(query, (session['id'],finafilename, numberofFaces,numberofMasks, ))
                    db.commit()
                    processedSavePath = os.path.join(app.config["IMAGE_PROCESSED"], finafilename)
                    cv2.imwrite(processedSavePath, cv2.cvtColor(processedImage, cv2.COLOR_RGB2BGR))
                    os.remove(filename)
                except:
                    e = sys.exc_info()
                    db.rollback()
                    return render_template("imageUpload.html", message="database error: " + str(e))

                return redirect("imageView")
            else:
                print('No file or url selected.')
                return render_template("imageUpload.html", message='No file or url selected')
        return render_template("imageUpload.html",message = "please select image")
    return redirect(url_for('login'))

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