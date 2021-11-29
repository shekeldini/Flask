import psycopg2
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g, make_response, jsonify
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from classUserLogin import UserLogin
from forms import LoginForm
from admin.admin import admin
from postgresql import Postgresql
from classReport import Report
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
login_manager.login_message_category = "invalid"
dbase: Postgresql


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = psycopg2.connect(dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
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

        report = Report(request=request.get_json(), dbase=dbase, user=current_user)
        return jsonify(report.get_report())

    return render_template('vpr_analysis.html', title="Аналитика ВПР")

@app.route("/get_reports")
@login_required
def get_reports():
    reports = ["Статистика по отметкам", "Сравнение отметок с отметками по журналу"]
    reports_array = []
    for report_id, report in enumerate(reports):
        reports_obj = {'id': report_id, 'name': report}
        reports_array.append(reports_obj)
    return jsonify({'reports': reports_array})


@app.route("/get_districts")
@login_required
def get_districts():
    districts = dbase.get_districts(current_user.get_id())
    district_array = []
    if current_user.get_id_role() in {1, 2}:
        district_array.append({'id': "all", 'name': "Вся выборка"})

    for district in districts:
        district_obj = {'id': district[0], 'name': district[1].replace("_", " ")}
        district_array.append(district_obj)
    return jsonify({'districts': district_array})

@app.route('/oo/<id_district>')
@login_required
def oo_by_name_of_the_settlement(id_district):
    oo_array = []
    if id_district == "all":
        oo_array.append({'id': "all", 'name': "Вся выборка"})
        return jsonify({'oo': oo_array})
    oo = dbase.get_oo_from_district(id_district, current_user.get_id())
    if current_user.get_id_role() in {1, 2, 3}:
        oo_array.append({'id': "all", 'name': "Вся выборка"})

    for school in oo:
        oo_obj = {'id': school[0], 'name': school[1]}
        oo_array.append(oo_obj)
    return jsonify({'oo': oo_array})

@app.route('/parallels/<id_oo>')
@login_required
def parallels_for_oo(id_oo):
    if id_oo == "all":
        parallels = dbase.get_parallels()
        parallels_array = []
        for parallel in sorted(parallels, key=lambda x: x[0]):
            parallels_obj = {'id': parallel, 'name': parallel}
            parallels_array.append(parallels_obj)
    else:
        parallels = dbase.get_parallels_for_oo(id_oo)
        parallels_array = []
        for parallel in sorted(parallels, key=lambda x: x[1]):
            parallels_obj = {'id': parallel[0], 'name': parallel[1]}
            parallels_array.append(parallels_obj)

    return jsonify({'parallels': parallels_array})

@app.route('/all_subjects/<parallel>')
@login_required
def all_subjects(parallel):
    subjects = dbase.get_subjects(parallel, current_user.get_id())
    subjects_array = []
    for subject in sorted(subjects, key=lambda x: x[1]):
        subjects_obj = {'id': subject[0], 'name': subject[1]}
        subjects_array.append(subjects_obj)

    return jsonify({'subjects': subjects_array})

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
        return render_template('index.html',
                               count_of_students=dbase.get_count_students(),
                               count_of_oo=dbase.get_count_oo(),
                               count_of_subject=dbase.get_count_of_subject(),
                               count_of_parallels=dbase.get_count_of_parallels(),
                               title="Главная страница")

    return render_template('index.html',
                           count_of_students=dbase.get_count_students(),
                           count_of_oo=dbase.get_count_oo(),
                           count_of_subject=dbase.get_count_of_subject(),
                           count_of_parallels=dbase.get_count_of_parallels(),
                           title="Главная страница")


@app.errorhandler(404)
def pageNotFound(error):
    return render_template("page404.html", title="Страница не найдена"), 404


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.get_user_by_login(form.login.data)
        if user:
            user_password = user[5]
            if user and check_password_hash(user_password, form.password.data):
                userLogin = UserLogin().create(user)
                login_user(userLogin, remember=True)
                return redirect(request.args.get("next") or url_for("index"))

        flash("Неверный логин или пароль", "invalid")
        return redirect(url_for('login'))
    return render_template("login.html", title="Авторизация", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


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
    app.run(debug=DEBUG, host="0.0.0.0")
