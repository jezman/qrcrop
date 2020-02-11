import os
import splitter
from app import app
from flask import flash, request, redirect, render_template, send_file
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['pdf'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the files part
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File(s) successfully uploaded')
        return redirect('/')


@app.route('/return-files/')
def return_files_tut():
    try:
        archive = splitter.processingUploadFolder()
        return send_file(archive, as_attachment=True, cache_timeout=-1)
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
