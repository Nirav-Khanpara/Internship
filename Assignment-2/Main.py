import json
from flask import Flask, render_template, send_file, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import FileField
import os
from patoolib import extract_archive


app = Flask(__name__)
app.config['SECRET_KEY'] = 'aasd4asd63ghdfsd'

# Global variables
subfolder_path=''
temp=False
file_path=''

def extract_zip(file_name):
    global subfolder_path

    # creating 'Extracted' if not exists
    if not os.path.isdir('Extracted'):
        os.mkdir('Extracted')
    subfolder_path = os.path.join('Extracted/', file_name.filename)

    # if subfolder exists then removing its contents
    try:
        os.mkdir(subfolder_path)
    except:
        for file in os.scandir(subfolder_path):
            os.remove(file.path)

    # Extracting Files
    extract_archive(os.path.join('ZipFile_Storage/',file_name.filename), outdir=subfolder_path)
    os.remove(os.path.join('ZipFile_Storage/',file_name.filename))

class upload_zip(FlaskForm):
    file_name = FileField(label="Upload file:", validators=[FileRequired(), FileAllowed(['zip', 'rar'])])

@app.route("/", methods=['GET', 'POST'])
def upload():
    global subfolder_path
    global temp

    base_form = upload_zip()

    # validating form and storing zip file in 'ZipFile_Storage' folder
    if base_form.validate_on_submit():
        file = base_form.file_name.data
        if not os.path.isdir('ZipFile_Storage'):
            os.mkdir('ZipFile_Storage')
        file.save(os.path.join('ZipFile_Storage/', file.filename))
        extract_zip(file)
        file_names=[]

        # iterating through all files available in zip
        for i in os.walk(subfolder_path):
            if i[-1]:
                for file in i[-1]:
                    file_names.append(file)

        json_files = json.dumps(file_names)
        return render_template("showunzippedfiles.html", files=file_names, json_files=json_files)

    else:
        if temp:
            flash('Please upload .zip or .rar file')
        temp=True
        return render_template("uploadfile.html", form=base_form)


@app.route("/<fname>", methods=['GET', 'POST'])
def download_individual(fname):
    global subfolder_path
    global file_path

    # Downloading file individually
    for i in os.walk(subfolder_path):
        if fname in i[-1]:
            file_path = i[0]
            return send_file(file_path+'/'+fname, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
