import psycopg2
import os
from flask import Flask, render_template, url_for, request, flash, redirect, abort, g, make_response, jsonify, \
    send_from_directory
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from classReportController import ReportController
from classUserLogin import UserLogin
from forms import LoginForm
from data_base.postgresql import Postgresql
from configurations.development import Config
from blueprints.api import blueprint_api

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(blueprint_api, url_prefix="/api")

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизируйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "invalid"

db_connection = None


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, Postgresql(db_connection))


def connect_db():
    conn = psycopg2.connect(dbname=app.config["DB_NAME"],
                            user=app.config["USER"],
                            password=app.config["PASSWORD"],
                            host=app.config["HOST"],
                            port=app.config["PORT"])
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    """Соединение с БД, если оно еще не установленно"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global db_connection
    db_connection = get_db()


@app.teardown_appcontext
def close_db(error):
    """Закрытие соединения с БД"""
    if hasattr(g, "link_db"):
        g.link_db.close()


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
@login_required
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, path=filename)


@app.route("/task_description", methods=["POST", "GET"])
@login_required
def task_description():
    if request.method == "POST":
        report = ReportController(request=request.get_json(), connection=db_connection, user=current_user)
        return jsonify(report.get_report())
    return render_template('task_description.html', title="Описание заданий")


@app.route("/school_in_risk", methods=["POST", "GET"])
@login_required
def school_in_risk():
    if not current_user.school_in_risk_access():
        return abort(403)
    if request.method == "POST":
        report = ReportController(request=request.get_json(), connection=db_connection, user=current_user)
        return jsonify(report.get_report())
    return render_template('school_in_risk.html', title="Школы в зоне риска")


@app.route("/vpr_analysis", methods=["POST", "GET"])
@login_required
def vpr_analysis():
    if request.method == "POST":
        report = ReportController(request=request.get_json(), connection=db_connection, user=current_user)
        return jsonify(report.get_report())

    return render_template('vpr_analysis.html', title="Аналитика ВПР")


@app.route("/")
def index():
    dbase = Postgresql(db_connection)

    return render_template('index.html',
                           count_of_students=dbase.get_count_students(2021),
                           count_of_oo=dbase.get_count_oo(2021),
                           title="Главная страница")


@app.route("/test", methods=["POST", "GET"])
@login_required
def test():
    if not current_user.is_admin():
        abort(404)
    if request.method == "POST":
        report = ReportController(request=request.get_json(), connection=db_connection, user=current_user)
        return jsonify(report.get_report())

    return render_template('test.html', title="test")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page404.html", title="Страница не найдена"), 404


@app.errorhandler(403)
def page_not_allowed(error):
    return "Недостаточно прав", 403


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        dbase = Postgresql(db_connection)
        user = dbase.get_user_by_login(form.login.data)
        if user:
            user_password = user[5]
            if user and check_password_hash(user_password, form.password.data):
                userLogin = UserLogin().create(user)
                login_user(userLogin, remember=True, duration=app.config["DURATION"])
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
        dbase = Postgresql(db_connection)
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
    app.run(debug=True, host="0.0.0.0")
