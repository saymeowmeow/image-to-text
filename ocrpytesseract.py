from flask import Flask, render_template, request, url_for, Response
from flask_restful import Api, Resource, reqparse
import pytesseract
import cv2
from PIL import Image
import os
from matplotlib import pyplot as plt
import numpy as np
from logging import FileHandler,WARNING
import re
from werkzeug.utils import secure_filename
#from ocr_core import ocr_core

#specify and change the path to where your tesseract.exe file is stored:
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\HP\Desktop\ocrproject\ocrpyt\Tesseract-OCR\tesseract.exe'

#function to open file and search for a specific CR number from the doctor's prescription
def ocr_core(filename):
    text = pytesseract.image_to_string(Image.open(filename))
    try:
    	result=re.search(r"([0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9])",text).group(0)
    #lst=re.findall("\d",result)
    #s = [str(i) for i in lst]
    #crno = int("".join(s))
    	return result
    except:
    	return "Image is not clear. Rescan the image"

#flask code for HTML template and file handling
app=Flask(__name__, template_folder='templates')
file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'uploads\\')
#newfilename=os.path.join(UPLOAD_FOLDER, ocr_core(filename)+'.jpg')
#os.rename(filename,newfilename)

#create upload folder that will store uploaded files
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#routing the flask application
#upload an image file and send to python code. The uploaded image will be saved in uploads folder and will be renamed as CR number.
@app.route('/', methods = ['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload.html', msg = 'No file selected')
        file = request.files['file']
        if file.filename == '':
        	return render_template('upload.html', msg = 'No file')
        if file and allowed_file(file.filename):
        	# file.filename=extracted
        	filename = str(secure_filename(file.filename))
        	file.save(os.path.join(app.config['UPLOAD_FOLDER'])+file.filename)
        	extracted = ocr_core(file)
        	extension=filename.split(".")
        	extension=str(extension[1])
        	source=UPLOAD_FOLDER+"/"+filename
        	destination=UPLOAD_FOLDER+extracted+"."+extension
            # file.save(UPLOAD_FOLDER+=file.filename)
        	#source=UPLOAD_FOLDER+"/"+file.filename
        	#destination=UPLOAD_FOLDER+"\"+extracted+'.jpg'
        	os.rename(source,destination) #renaming the uploaded file
        	return render_template('upload.html',
        							extracted = extracted, 
        							img_src = UPLOAD_FOLDER + file.filename)
    else:
        return render_template('upload.html')
if __name__ == '__main__':
    app.run(debug=True) #debug to find errors while running application

