from flask import Flask, render_template, send_file, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import FileField
from zipfile import ZipFile
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aasd4asd63ghdfsd'
x=0
subfolder_path=''
temp=False

def extract_zip(file_name):
    global x
    global subfolder_path
    if not os.path.isdir('Extracted'):
        os.mkdir('Extracted')
    subfolder_path = os.path.join('Extracted', file_name.filename)
    if os.path.isdir(subfolder_path):
        x += 1
        subfolder_path = subfolder_path+'_'+str(x)
    os.mkdir(subfolder_path)
    with ZipFile(file_name, 'r') as zip:
        zip.extractall(subfolder_path)

class upload_zip(FlaskForm):
    file_name = FileField(label="Upload file:", validators=[FileRequired(), FileAllowed(['zip', 'rar'])])

@app.route("/", methods=['GET', 'POST'])
def upload():
    global subfolder_path
    global temp
    base_form = upload_zip()

    if base_form.validate_on_submit():
        file = base_form.file_name.data
        extract_zip(file)
        return render_template("showunzippedfiles.html", files=os.listdir(subfolder_path))
    else:
        if temp:
            flash('Please upload .zip or .rar file')
        temp=True
        return render_template("uploadfile.html", form=base_form)


@app.route("/<fname>", methods=['GET', 'POST'])
def download_individual(fname):
    global subfolder_path
    return send_file(subfolder_path+'/'+fname, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
