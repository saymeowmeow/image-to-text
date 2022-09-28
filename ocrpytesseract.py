from flask import Flask, render_template, request, url_for, Response
from flask_restful import Api, Resource, reqparse
import pytesseract
import cv2
from PIL import Image
import os
from matplotlib import pyplot as plt
import numpy as np
from logging import FileHandler,WARNING
#from ocr_core import ocr_core

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr_core(filename):
    text = pytesseract.image_to_string(Image.open(filename))
    return text

app=Flask(__name__, template_folder='templates')
file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'uploads\\')
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods = ['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload.html', msg = 'No file selected')
        file = request.files['file']
        if file.filename == '':
        	return render_template('upload.html', msg = 'No file')
        if file and allowed_file(file.filename):
        	file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        	extracted = ocr_core(file)
        	return render_template('upload.html', 
        							msg = 'OCR completed',
        							extracted = extracted, 
        							img_src = UPLOAD_FOLDER + file.filename)
    else:
        return render_template('upload.html')
if __name__ == '__main__':
    app.run(debug=True)

