from flask import Flask, render_template, send_file
from flask_wtf import FlaskForm
from wtforms import FileField
import shutil
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aasd4asd63ghdfsd'

def extract_zip(file_name):
    os.makedirs('Extracted', exist_ok=True)
    shutil.rmtree('Extracted')
    shutil.unpack_archive(file_name,'Extracted')

class upload_zip(FlaskForm):
    file = FileField(label="Upload file:")

@app.route("/", methods=['GET', 'POST'])
def upload():
    base_form = upload_zip()
    if base_form.validate():
        zip_file = base_form.file.data
        extract_zip(zip_file)
        return render_template("showunzippedfiles.html", files=os.listdir("Extracted"))
    else:
        return render_template("uploadfile.html", form=base_form)


@app.route("/<fname>", methods=['GET', 'POST'])
def download_individual(fname):
    return send_file('Extracted/'+fname, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
