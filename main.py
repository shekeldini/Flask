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
    if request.method == "POST":
        result = request.get_json()
        id_name_of_the_settlement = result["name_of_the_settlement"]
        id_oo = result["oo"]
        id_oo_parallels = result["parallel"]
        id_oo_parallels_subjects = result["subject"]
        res = dbase.get_count_students_mark(id_oo_parallels_subjects, id_oo_parallels)
        count_of_mark = sum(res.values())

        return jsonify({"percents": {2: round((res[2] / count_of_mark) * 100, 2),
                                     3: round((res[3] / count_of_mark) * 100, 2),
                                     4: round((res[4] / count_of_mark) * 100, 2),
                                     5: round((res[5] / count_of_mark) * 100, 2)}})
    return render_template('vpr_analysis.html', menu=dbase.get_logged_menu(), title="Аналитика ВПР")


@app.route("/get_districts")
@login_required
def get_districts():
    districts = dbase.get_districts()
    district_array = []
    for district in districts:
        district_obj = {'id': district[0], 'name': district[1].replace("_", " ")}
        district_array.append(district_obj)
    return jsonify({'districts': district_array})


@app.route('/oo/<id_district>')
@login_required
def oo_by_name_of_the_settlement(id_district):
    oo = dbase.get_oo_from_district(id_district)
    oo_array = []
    for list_ in oo:
        for school in list_:
            oo_obj = {'id': school[0], 'name': school[1]}
            oo_array.append(oo_obj)
    return jsonify({'oo': oo_array})


@app.route('/parallels/<id_oo>')
@login_required
def parallels_for_oo(id_oo):
    parallels = dbase.get_parallels_for_oo(id_oo)
    parallels_array = []
    for parallel in sorted(parallels, key=lambda x: x[1]):
        parallels_obj = {'id': parallel[0], 'name': parallel[1]}
        parallels_array.append(parallels_obj)

    return jsonify({'parallels': parallels_array})


@app.route('/subjects/<id_oo_parallels>')
@login_required
def subjects_for_oo_parallels(id_oo_parallels):
    subjects = dbase.get_subjects_for_oo_parallels(id_oo_parallels)
    subjects_array = []
    for subject in sorted(subjects, key=lambda x: x[1]):
        subjects_obj = {'id': subject[0], 'name': subject[1]}
        subjects_array.append(subjects_obj)

    return jsonify({'subjects': subjects_array})


@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template('index.html', menu=dbase.get_logged_menu(), title="Главная страница")
    return render_template('index.html', menu=dbase.get_guest_menu(), title="Главная страница")


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hash_psw = generate_password_hash(form.psw.data)
        res = dbase.add_user(form.name.data, form.email.data, hash_psw)
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
