
from app import app
from flask import render_template, g, request, session, redirect, url_for, send_file
import cv2
import os, sys
from werkzeug.utils import secure_filename
import requests
from app.ImageHandler.model import ImageHandler
from app.database.dbManager import dbManager


@app.route('/sendImages/<filename>/', methods=["GET", "POST"])
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
        dbm = dbManager();
        images  = dbm.search_data('images', 'id', session['id'],singleResult=False )
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

        return render_template('imageManager/imageView.html', message="", noface=noface, allFaceWithMask=allFaceWithMask,
                               allFaceNoMask=allFaceNoMask, someFaceWithMask=someFaceWithMask)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/imageUpload', methods=["GET", "POST"])
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
                    if not ImageHandler.allowedImageFilesize(request.cookies["filesize"]):
                        print("Filesize exceeded maximum limit")
                        return render_template("imageManager/imageUpload.html", message="Filesize exceeded maximum limit")
                    # get the image object
                    image = request.files['image']
                    # check image name
                    if image.filename == '':
                        print("Image must have a file name")
                        return render_template("imageManager/imageUpload.html", message="Image must have a file name")
                    if not ImageHandler.allowedImageType(image.filename):
                        print("Image is not in valid type")
                        return render_template("imageManager/imageUpload.html", message="Image is not in valid type")
                    else:
                        filename = secure_filename(image.filename)
                        savePath = os.path.join(app.config["IMAGE_UPLOADS"], image.filename)
                        image.save(savePath)
                        try:
                            output_info, processedImage = ImageHandler.faceMaskDetection(savePath)
                        except:
                            e = sys.exc_info()
                            return render_template("imageManager/imageUpload.html",
                                                   message="Image could not be processed correctly" + str(e))
                        numberofFaces = len(output_info)
                        numberofMasks = ImageHandler.NumberOfMask(output_info)
                        finafilename = ImageHandler.generate_filename()
                        finafilename = finafilename + '.' + filename.rsplit(".", 1)[1]
                        dbm = dbManager();
                        dbm.insert_data_image(session['id'],finafilename,numberofFaces,numberofMasks,"imageManager/imageUpload.html")
                        processedSavePath = os.path.join(app.config["IMAGE_PROCESSED"], finafilename)
                        cv2.imwrite(processedSavePath, cv2.cvtColor(processedImage, cv2.COLOR_RGB2BGR))
                        os.remove(savePath)

                    return redirect("imageView")
            elif request.form['url'] != "":
                url = request.form['url']
                if not ImageHandler.allowedImageType(url):
                    print("Image is not in valid type")
                    return render_template("imageManager/imageUpload.html", message="Image is not in valid type")
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
                    return render_template("imageManager/imageUpload.html",
                                           message="Image could not be downloaded from url. Error: " + str(e))
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
                dbm = dbManager();
                dbm.insert_data_image(session['id'], finafilename, numberofFaces, numberofMasks,
                                      "imageManager/imageUpload.html")
                processedSavePath = os.path.join(app.config["IMAGE_PROCESSED"], finafilename)
                cv2.imwrite(processedSavePath, cv2.cvtColor(processedImage, cv2.COLOR_RGB2BGR))
                os.remove(filename)

                return redirect("imageView")
            else:
                print('No file or url selected.')
                return render_template("imageManager/imageUpload.html", message='No file or url selected')
        return render_template("imageManager/imageUpload.html", message="please select image")
    return redirect(url_for('login'))
