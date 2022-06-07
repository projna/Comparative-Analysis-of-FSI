from flask import flash
from flask import render_template, request
from werkzeug.utils import secure_filename
import os
from controller import utils
from flask import current_app


def index():
    current_app.config['SECRET_KEY'] = 'your secret key'
    # print(current_app.config['SECRET_KEY'])
    form = utils.FormValidator()
    return render_template('index.html', form=form)


def savefile():
    current_app.config['SECRET_KEY'] = 'your secret key'
    if request.method == 'GET':
        return "We are not using this get method! Sorry"
    if request.method == 'POST':
        comparative_type = request.form['group']
        print(comparative_type)
        current_app.config['COMPARATIVE_TYPE'] = comparative_type
        indicator_validation = utils.IndicatorValidator()
        for f in os.listdir(current_app.config['UPLOAD_FOLDER']):
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], f))
        if comparative_type == 'intra':
            validate = utils.FormValidator()
            if validate.validate_on_submit():
                files = request.files['owlfile']
                filename = secure_filename(files.filename)
                files.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                flash('File Uploaded!')
                return render_template('indicator.html', form=indicator_validation)
            return render_template('index.html', form=validate)
        else:
            doublevalidate = utils.DoubleFormValidator()
            if doublevalidate.validate_on_submit():
                files1 = request.files['owlfile1']
                files2 = request.files['owlfile2']
                filename1 = secure_filename(files1.filename)
                filename2 = secure_filename(files2.filename)
                files1.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename1))
                files2.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename2))
                return render_template('indicator.html', form=indicator_validation)

            return render_template('index.html', form=doublevalidate)
