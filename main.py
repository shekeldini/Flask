import psycopg2
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g, make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from classUserLogin import UserLogin
from forms import LoginForm, RegisterForm, VPRAnalysisForm
from admin.admin import admin
from postgresql import Postgresql
from config import *

DEBUG = True
SECRET_KEY = "0ef60679aaacc60167c89fe654cc11c74920113a"
MAX_CONTENT_LENGTH = 1024 * 1024

app = Flask(__name__)
app.config.from_object(__name__)
app.register_blueprint(admin, url_prefix='/admin')

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизируйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"
dbase: Postgresql


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = psycopg2.connect(user=USER,
                            password=PASSWORD,
                            host=HOST,
                            port=PORT)
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = Postgresql(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()


@app.route("/vpr_analysis", methods=["POST", "GET"])
@login_required
def vpr_analysis():
    form = VPRAnalysisForm()
    form.name_of_the_settlement.choices = [(district[0], district[1].replace("_"," ")) for
                                           district in dbase.get_districts()]
    return render_template('vpr_analysis.html', menu=dbase.get_logged_menu(), form=form, title="Аналитика ВПР")


@app.route('/oo/<id_district>')
@login_required
def oo_by_name_of_the_settlement(id_district):
    oo = dbase.get_oo_from_district(id_district)
    ooArray = []
    for list in oo:
        for school in list:
            ooObj = {}
            ooObj['id'] = school[0]
            ooObj['name'] = school[1]
            ooArray.append(ooObj)
    return jsonify({'oo': ooArray})


@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template('index.html', menu=dbase.get_logged_menu(), title="Главная страница")
    return render_template('index.html', menu=dbase.get_guest_menu(), title="Главная страница")


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hash = generate_password_hash(form.psw.data)
        res = dbase.add_user(form.name.data, form.email.data, hash)
        if res:
            flash("Вы успешно зарегистрированы", "success")
            return redirect(url_for("login"))
        else:
            flash("Ошибка при добавлении в БД", "error")

    return render_template('register.html', title="Регистрация", menu=dbase.get_guest_menu(), form=form)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template("page404.html", title="Страница не найдена", menu=dbase.get_guest_menu()), 404


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.get_user_by_email(form.email.data)
        if user:
            user_psw = user[3]
            if user and check_password_hash(user_psw, form.psw.data):
                userLogin = UserLogin().create(user)
                rm = form.remember.data
                login_user(userLogin, remember=rm)
                return redirect(request.args.get("next") or url_for("profile"))

        flash("Неверный логин или пароль", "error")
    return render_template("login.html", title="Авторизация", menu=dbase.get_guest_menu(), form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышл из аккаунта", "success")
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", title="Профиль", menu=dbase.get_logged_menu())


@app.route('/userava')
@login_required
def userava():
    img = current_user.getAvatar(app)
    if not img:
        return ''
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    if request.method == "POST":
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = dbase.update_user_avatar(img, current_user.get_id())
                if not res:
                    flash("Ошибка обновления аватара", "success")
                    return redirect(url_for('profile'))
                flash("Аватар обновлен", "success")
            except FileNotFoundError as e:
                flash("Ошибка чтения файла", "error")
        else:
            flash("Ошибка обновления аватара", "success")
    return redirect(url_for('profile'))


if __name__ == "__main__":
    app.run(debug=DEBUG)
