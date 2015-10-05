from __future__ import print_function
import csv
import sys
import os


from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from flask import send_from_directory
from urllib2 import urlopen

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(file_name):
    return '.' in file_name and \
           file_name.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def upload_file(file):
    if file and allowed_file(file.filename):
        file_name = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
        result = open((os.path.join(app.config['UPLOAD_FOLDER'], file_name)))
        return result

def upload_p(file):
    if file and allowed_file(file.filename):
        file_name = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))

def delete_file(file):
    file_name = secure_filename(file.filename)
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
