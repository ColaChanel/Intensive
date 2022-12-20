from flask import Flask, render_template, request, flash, redirect, url_for, session, abort, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '\\upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Нейросеть")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == "POST":
        if 'file' not in request.files:
            flash("Не могу прочитать файл")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash("Нет выбранного файла")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('/upload', filename))
            return render_template("index.html", title="Нейросеть")


if __name__ == '__main__':
    app.run(debug=True)
