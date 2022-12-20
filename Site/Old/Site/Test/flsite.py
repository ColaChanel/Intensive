from flask import Flask, render_template, request, flash, session, redirect, url_for, abort, make_response, g
# import sqlite3 # для прошлого метода
# from FDataBase import Database
#from flask_login import LoginManager, login_user, login_required, logout_user, current_user
#from UserLogin import UserLogin
#from forms import LoginForm
# для MYSQL Базы данных
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

# Config for our project for sqlite3
# DATABASE = '/tmp/site.db'
# DEBUG = True
# SECRET_KEY = '7f32a4c80cc877ca06cec1becf394a85505a4294'
app = Flask(__name__)
# app.config.from_object(__name__)
# app.config.update(dict(DATABASE=os.path.join(app.root_path, 'site.db')))

# #Config DATABASE for mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234567890admin'
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)

# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message = "Log in for access to closed pages "
# login_manager.login_message_category = 'success'

# для sqlite3
# @login_manager.user_loader
# def load_user(user_id):
#     print("load_user")
#     return UserLogin().fromDB(user_id, dbase)
# def connect_db():
#     conn = sqlite3.connect(app.config['DATABASE'])
#     conn.row_factory = sqlite3.Row
#     return conn
# def create_db():
#     db = connect_db()
#     with app.open_resource('sq_db.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()
#     db.close()
# def get_db():
#     if not hasattr(g, 'link_db'):
#         g.link_db = connect_db()
#     return g.link_db
# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'link_db'):
#         g.link_db.close()
# dbase = None
# @app.before_request
# def before_request():
#     global dbase
#     db = get_db()
#     dbase = Database(db)


@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/pages/internships")
def internships():
    return render_template('pages/internships.html', title="internships")


@app.route("/pages/europe")
def europe():
    return render_template('pages/europe.html')


@app.route("/pages/usa")
def usa():
    return render_template('pages/usa.html')


@app.route("/pages/canada")
def canada():
    return render_template('pages/canada.html')


@app.route("/pages/articles")
# @login_required # доступ только авторизованным
def articles():
    return render_template('pages/articles.html', title="Articles")


@app.route("/pages/america")
def america():
    return render_template('pages/america.html', title="Parts of the world | America")


@app.route("/pages/parts")
def parts():
    return render_template('pages/parts.html', title="Parts of the world")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        # print(request.form)
        if len(request.form['username']) > 2:
            flash('Sent', category='success')
        else:
            flash('Username too small', category='error')
        print(request.form['username'])
    return render_template('contact.html', title="Обратная связь")


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title="Page Not Found")


@app.route("/profile")
# @login_required # доступ только авторизованным
def profile():
    return render_template('profile.html', title="Profile")


@app.route("/login", methods=["GET", "POST"])
def login():
    # 1 way
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password,))
        users = cursor.fetchone()
        if users:
            session['loggedin'] = True
            session['id'] = users['id']
            session['username'] = users['username']
            msg = 'Logged in successfully !'
            return render_template('profile.html', msg=msg, title='Profile')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg, title='Login')
    # 2 way
    # if current_user.is_authenticated:
    #     return redirect(url_for('profile'))
    #
    # form = LoginForm()
    # if form.validate_on_submit():
    #     user = dbase.getUserByEmail(form.email.data)
    #     if user and check_password_hash(user['psw'], form.psw.data):
    #         userlogin = UserLogin().create(user)
    #         rm = form.remember.data
    #         login_user(userlogin, remember= rm)
    #         return redirect(request.args.get("next") or url_for('profile'))
    #
    #     flash("Incorrect Login/password", "error")
    # return render_template('login.html', title="authorization", form=form)
    # 3 way
    # if request.method == "POST":
    #     user = dbase.getUserByEmail(request.form['email'])
    #     if user and check_password_hash(user['psw'], request.form['psw']):
    #         userlogin = UserLogin().create(user)
    #         rm = True if request.form.get('remain_me') else False
    #         login_user(userlogin, remember= rm)
    #         return redirect(request.args.get("next") or url_for('profile'))
    #
    #     flash("Incorrect Login/password", "error")
    #
    # return render_template('login.html', title="authorization")


@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s', (username,))
        users = cursor.fetchone()
        if users:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO users VALUES (NULL, % s, % s, % s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg, title='Register')
    # if current_user.is_authenticated:
    #     return redirect(url_for('profile'))
    #
    # if request.method == "POST":
    #     if len(request.form['name']) > 4 and len(request.form['email']) > 4 \
    #             and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
    #         hash = generate_password_hash(request.form['psw'])
    #         res = dbase.addUser(request.form['name'], request.form['email'], hash)
    #         if res:
    #             flash("You have successfully register", "success")
    #             return redirect(url_for('login'))
    #         else:
    #             flash("Can't register'", "error")
    #     else:
    #         flash("Fields filled out incorrectly", "error")
    #
    # return render_template("register.html", title="register")


@app.route("/logout")
# @login_required # доступ только авторизованным
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # logout_user()
    # flash("You have been logged out!", "success")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
