from app import app
from flask import render_template, g, request, session, redirect, url_for, send_from_directory, send_file
from app.main import get_db
import cv2
import os, sys
from werkzeug.utils import secure_filename
import requests
import shutil
sys.path.insert(1, 'C:/Users/ASUS/python-workspace/ECE1779Assignment1/FaceMaskDetection')
sys.path.insert(1, 'C:/Users/ASUS/python-workspace/ECE1779Assignment1/FaceMaskDetection/models')
sys.path.insert(1, 'C:/Users/ASUS/python-workspace/ECE1779Assignment1/FaceMaskDetection/load_model')
from FaceMaskDetection.pytorch_infer import inference
from FaceMaskDetection.utils import anchor_decode,anchor_generator

app.config["IMAGE_UPLOADS"]="C:/Users/ASUS/python-workspace/ECE1779Assignment1/app/static/img/uploads"
app.config["IMAGE_PROCESSED"]="C:/Users/ASUS/python-workspace/ECE1779Assignment1/app/static/img/processed"
app.config["ALLOWED_IMAGE_EXETENSIONS"] = ["JPEG"]
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

def getNumberOfFilesInDatabase():
    db = get_db()
    cursor = db.cursor()
    query = '''select count(*) from images'''
    cursor.execute(query)
    numberOfFiles = cursor.fetchall()
    return numberOfFiles[0][0]
#method to check the type of file uploaded by user
def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".",1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXETENSIONS"]:
        return True

@app.route('/sendImages/<filename>',methods = ["GET", "POST"])
def sendImages(filename):
    #print(filename)
    image_path = os.path.join(app.config["IMAGE_PROCESSED"], filename)
    print(image_path)
    return send_file(image_path)

@app.route('/imageView')
def imageView():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page

        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            db.start_transaction()
            query = '''SELECT * FROM images WHERE username = %s for update'''
            cursor.execute(query, (session['username'],))
        except:
            e = sys.exc_info()
            db.rollback()
        images = cursor.fetchall()

        return render_template('imageView.html', images = images)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



@app.route('/imageUpload', methods = ["GET", "POST"])
def imageUpload():
    if request.method == "POST":
        if request.files:
            #get the image object
            image = request.files['image']
            #check image name
            if image.filename == '':
                print("Image must have a file name")
                return redirect(request.url)
            if not allowed_image(image.filename):
                print("Image is not in valid type")
                return redirect(request.url)
            else:
                filename = secure_filename(image.filename)
                savePath = os.path.join(app.config["IMAGE_UPLOADS"], image.filename)
                image.save(savePath)
                output_info,processedImage = faceMaskDetection(savePath)
                numberofFaces = len(output_info)
                numberofMasks = NumberOfMask(output_info)
                numberOfFileInDatabase = getNumberOfFilesInDatabase()
                finafilename = 'processed' + str(numberOfFileInDatabase) + '.' + filename.rsplit(".",1)[1]
                db = get_db()
                cursor = db.cursor(dictionary=True)
                try:
                    db.start_transaction()
                    query ='''insert into images values (%s,%s,%s,%s) for update'''
                    cursor.execute(query, (session['username'],finafilename, numberofFaces,numberofMasks, ))
                    db.commit()
                    processedSavePath = os.path.join(app.config["IMAGE_PROCESSED"], finafilename)
                    cv2.imwrite(processedSavePath, cv2.cvtColor(processedImage, cv2.COLOR_RGB2BGR))
                    os.remove(savePath)
                except:
                    e = sys.exc_info()
                    db.rollback()

            return redirect("imageView")
        if request.form['url'] != "":
            url = request.form['url']

            filename = os.path.join(app.config["IMAGE_UPLOADS"], 'temp.jpeg')
            with open(filename, 'wb') as f:
                response = requests.get(url, stream=True)
                for block in response.iter_content(1024):
                    if not block:
                        break
                    f.write(block)
            print('Image sucessfully Downloaded: ')
            output_info,processedImage = faceMaskDetection(filename)
            numberofFaces = len(output_info)
            numberofMasks = NumberOfMask(output_info)
            numberOfFileInDatabase = getNumberOfFilesInDatabase()
            finafilename = 'processed' + str(numberOfFileInDatabase) + '.' + filename.rsplit(".",1)[1]
            db = get_db()
            cursor = db.cursor(dictionary=True)
            try:
                db.start_transaction()
                query ='''insert into images values (%s,%s,%s,%s)'''
                cursor.execute(query, (session['username'],finafilename, numberofFaces,numberofMasks, ))
                db.commit()
                processedSavePath = os.path.join(app.config["IMAGE_PROCESSED"], finafilename)
                cv2.imwrite(processedSavePath, cv2.cvtColor(processedImage, cv2.COLOR_RGB2BGR))
                os.remove(filename)
            except:
                e = sys.exc_info()
                db.rollback()

            return redirect("imageView")
        else:
            print('Image Couldn\'t be retreived')

    return render_template("imageUpload.html")


@app.route('/imageDelete/<filename>', methods=['POST'])
# Delete an object from a bucket
def imageDelete(filename):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    query = '''DELETE FROM images WHERE filename=%s'''
    cursor.execute(query, (filename,))
    db.commit()
    savePath = os.path.join(app.config["IMAGE_PROCESSED"], filename)
    os.remove(savePath)
    return redirect(url_for('imageView'))

def faceMaskDetection(readFilePath):
    img = cv2.imread(readFilePath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    output_info, image = inference(img, show_result=False, target_shape=(360, 360))

    #cv2.imwrite(saveFilePath, image)
    return output_info,image

def NumberOfMask(outputList):
    result = 0
    for outputInfor in outputList:
        if outputInfor[0] == 0:
            result = result + 1
    return result