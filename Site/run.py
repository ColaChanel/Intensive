from flask import Flask, render_template, request, flash, redirect, url_for, session, abort, send_from_directory
from werkzeug.utils import secure_filename
import secrets
from flask_wtf import FlaskForm
from wtforms import FileField
from flask_uploads import configure_uploads, IMAGES, UploadSet
import os

app = Flask(__name__)

UPLOAD_FOLDER = "upload"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

images = UploadSet('images', IMAGES)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = str(secrets.SystemRandom().getrandbits(128))
app.config['UPLOADED_IMAGES_DEST'] = "uploads/images"
configure_uploads(app, images)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Нейросеть")

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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

'''@app.post("/upload")
def upload():
    if "photo" in request.files:
        images.save(request.files["photo"])
        flash("Успешно загружено.")
        return redirect(url_for("index"))'''



'''@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            print(1)
            flash('Нету файла')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print(2)
            flash('Не выбран файл')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print(3)
            filename = secure_filename(file.filename)
            session["id"] = filename
            file.save(os.path.join('upload', filename))
            return redirect(url_for('uploaded',
                                    filename=filename))
    return render_template('upload.html')'''

if __name__ == '__main__':
    app.run(debug=True)
