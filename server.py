import os
from flask import Flask, flash, request, redirect, url_for,make_response, render_template, send_from_directory, send_file
from werkzeug.utils import secure_filename
from tempfile import NamedTemporaryFile
from shutil import copyfileobj
from os import remove

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = 'some_secret'

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
            # return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'No file selected'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(filename)
            return redirect(url_for('uploaded_image',
                                    filename=filename))
            
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload New Image</h1>
        <form method=post enctype=multipart/form-data>
        <input type=file name=file accept=".jpeg,.jpg,.png">
        <input type=submit value=Submit>
        </form>
        '''

@app.route('/img/<filename>')
def uploaded_image(filename):
    tempFileObj = NamedTemporaryFile(mode='w+b',suffix='jpg')
    pilImage = open(filename,'rb')
    copyfileobj(pilImage,tempFileObj)
    pilImage.close()
    remove(filename)
    tempFileObj.seek(0,0)
    response = send_file(tempFileObj, mimetype='image/jpeg')
    return response