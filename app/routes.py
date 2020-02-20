import os
from app import splitter
from app import app
from shutil import rmtree
from flask import flash, request, redirect, render_template, send_file
from werkzeug.utils import secure_filename


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/upload-files', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the files part
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        if os.path.exists(app.config['UPLOAD_PATH']):
            rmtree(app.config['UPLOAD_PATH'])

        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                if not os.path.exists(app.config['UPLOAD_PATH']):
                    os.makedirs(app.config['UPLOAD_PATH'])
                file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('File(s) successfully uploaded')
        return redirect('/')


@app.route('/vertical-split')
def vertical_split():
    try:
        archive = splitter.processingUploadFolder(True)
        return send_file(archive, as_attachment=True, cache_timeout=-1)
    except Exception as e:
        return str(e)


@app.route('/horizontal-split')
def horizontal_split():
    try:
        archive = splitter.processingUploadFolder(False)
        return send_file(archive, as_attachment=True, cache_timeout=-1)
    except Exception as e:
        return str(e)
