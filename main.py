import psycopg2
import os
from io import BytesIO
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g, make_response, jsonify, \
    send_from_directory, Response
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from classUserLogin import UserLogin
from forms import LoginForm
from postgresql import Postgresql
from classReportController import ReportController
from config import *

DEBUG = True
SECRET_KEY = "0ef60679aaacc60167c89fe654cc11c74920113a"
MAX_CONTENT_LENGTH = 1024 * 1024

app = Flask(__name__)
app.config.from_object(__name__)
app.config["UPLOAD_FOLDER"] = "download"

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


@app.route("/api/export/")
@login_required
def export():
    export_data = {"report": {"id": request.args.get("filter_report_id"),
                              "name": request.args.get("filter_report_name")},

                   "year": {"id": request.args.get("filter_year_id"),
                            "name": request.args.get("filter_year_name")},

                   "district": {"id": request.args.get("filter_district_id"),
                                "name": request.args.get("filter_district_name")},

                   "oo": {"id": request.args.get("filter_oo_id"),
                          "name": request.args.get("filter_oo_name")},

                   "parallel": {"id": request.args.get("filter_parallel_id"),
                                "name": request.args.get("filter_parallel_name")},

                   "subject": {"id": request.args.get("filter_subject_id"),
                               "name": request.args.get("filter_subject_name")},

                   "task": {"id": request.args.get("filter_task_id"),
                            "name": request.args.get("filter_task_name")},
                   "table_type": request.args.get("filter_table_type")
                   }
    report = ReportController(request=export_data, dbase=dbase, user=current_user)
    wb, name = report.export_report()
    if not wb or not name:
        return "something wrong"
    virtual_workbook = BytesIO()
    wb.save(virtual_workbook)
    wb.close()
    return Response(
        virtual_workbook.getvalue(),
        headers={
            'Content-Disposition': f'attachment; filename={name}',
            'Content-type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
    )


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
@login_required
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, path=filename)


@app.route("/task_description", methods=["POST", "GET"])
@login_required
def task_description():
    if request.method == "POST":
        report = ReportController(request=request.get_json(), dbase=dbase, user=current_user)
        return jsonify(report.get_report())
    return render_template('task_description.html', title="Описание заданий")


@app.route("/api/task_description/get_task_numbers/<year>/<id_oo>/<int:parallel>/<int:id_subject>",
           methods=["POST", "GET"])
@login_required
def api_task_description_get_task_numbers(year, id_oo, parallel, id_subject):
    task_numbers_array = [{'id': "all", 'name': "Все задания"}]

    if id_oo != "all":
        task_numbers = dbase.get_task_number_from_kim_by_id_oo_parallels_subjects(id_subject)
    else:
        task_numbers = dbase.get_task_number_from_kim(id_subjects=id_subject,
                                                      parallel=parallel,
                                                      year=year)

    for key, value in task_numbers:
        task_numbers_array.append({'id': key, 'name': value})
    return jsonify({'task_numbers': task_numbers_array})


@app.route("/api/task_description/get_reports/<task_number>", methods=["POST", "GET"])
@login_required
def api_task_description_get_reports(task_number):
    if task_number == "all":
        return jsonify({'reports': [{'id': 4, 'name': "Описание работы"}]})
    else:
        return jsonify({'reports': [{'id': 5, 'name': "Распределение задания по позициям кодификаторов"}]})


@app.route("/school_in_risk", methods=["POST", "GET"])
@login_required
def school_in_risk():
    if current_user.get_id_role() not in (1, 2, 3):
        return abort(403)
    if request.method == "POST":
        report = ReportController(request=request.get_json(), dbase=dbase, user=current_user)
        return jsonify(report.get_report())
    return render_template('school_in_risk.html', title="Школы в зоне риска")


@app.route("/api/school_in_risk/get_districts/<year>")
@login_required
def api_districts_for_school_in_risk(year):
    districts = dbase.get_districts_for_schools_in_risk(id_user=current_user.get_id(),
                                                        year=year)
    district_array = []
    if current_user.get_id_role() in {1, 2}:
        district_array.append({'id': "all", 'name': "Все муниципалитеты"})

    for id_district, district in districts:
        district_obj = {'id': id_district, 'name': district.replace("_", " ")}
        district_array.append(district_obj)
    return jsonify({'districts': district_array})


@app.route('/api/school_in_risk/get_oo/<year>/<id_district>')
@login_required
def api_get_oo_for_schools_in_risk(year, id_district):
    oo_array = []
    if id_district == "all":
        oo_array.append({'id': "all", 'name': "Все ОО"})
        return jsonify({'oo': oo_array})
    oo = dbase.get_oo_by_district_for_schools_in_risk(id_district=id_district,
                                                      id_user=current_user.get_id(),
                                                      year=year)
    if current_user.get_id_role() in {1, 2, 3} and len(oo) > 1:
        oo_array.append({'id': "all", 'name': "Все ОО"})

    for id_school, school in oo:
        oo_obj = {'id': id_school, 'name': school}
        oo_array.append(oo_obj)
    return jsonify({'oo': oo_array})


@app.route('/api/school_in_risk/get_parallels/<year>/<id_district>/<id_oo>')
@login_required
def api_get_parallels_for_schools_in_risk(year, id_district, id_oo):
    parallels_array = []
    for parallel in dbase.get_parallels_for_schools_in_risk(year=year,
                                                            id_district=id_district,
                                                            id_oo=id_oo):
        parallels_array.append({'id': parallel, 'name': parallel})
    return jsonify({'parallels': parallels_array})


@app.route('/api/school_in_risk/get_subject/<year>/<id_district>/<id_oo>/<parallel>')
@login_required
def api_get_subject_for_schools_in_risk(year, id_district, id_oo, parallel):
    subject_array = []
    for id_subject, subject in dbase.get_subject_for_school_in_risk(year=year,
                                                                    id_district=id_district,
                                                                    id_oo=id_oo,
                                                                    parallel=parallel):
        subject_array.append({'id': id_subject, 'name': subject})
    return jsonify({'subjects': subject_array})


@app.route("/vpr_analysis", methods=["POST", "GET"])
@login_required
def vpr_analysis():
    if request.method == "POST":
        report = ReportController(request=request.get_json(), dbase=dbase, user=current_user)
        return jsonify(report.get_report())

    return render_template('vpr_analysis.html', title="Аналитика ВПР")


@app.route("/api/vpr_analysis/get_reports")
@login_required
def api_get_reports():
    reports = ["Статистика по отметкам", "Сравнение отметок с отметками по журналу", "Результаты ВПР"]
    reports_array = []
    for report_id, report in enumerate(reports):
        reports_obj = {'id': report_id, 'name': report}
        reports_array.append(reports_obj)
    return jsonify({'reports': reports_array})


@app.route("/api/select/get_year")
@login_required
def api_get_year():
    available_years = [2021]
    years_array = []
    for year in available_years:
        year_obj = {'id': year, 'name': year}
        years_array.append(year_obj)
    return jsonify({'year': years_array})


@app.route("/api/select/get_districts/<int:year>")
@login_required
def api_get_districts(year):
    districts = dbase.get_districts(id_user=current_user.get_id(),
                                    year=year)
    district_array = []
    if current_user.get_id_role() in {1, 2}:
        district_array.append({'id': "all", 'name': "Все муниципалитеты"})

    for district in districts:
        district_obj = {'id': district[0], 'name': district[1].replace("_", " ")}
        district_array.append(district_obj)
    return jsonify({'districts': district_array})


@app.route('/api/select/get_oo/<int:year>/<id_district>')
@login_required
def api_oo_by_name_of_the_settlement(year, id_district):
    oo_array = []
    if id_district == "all":
        oo_array.append({'id': "all", 'name': "Все ОО"})
        return jsonify({'oo': oo_array})
    oo = dbase.get_oo_from_district(id_district=id_district,
                                    id_user=current_user.get_id(),
                                    year=year)
    if current_user.get_id_role() in {1, 2, 3} and len(oo) > 1:
        oo_array.append({'id': "all", 'name': "Все ОО"})

    for school in oo:
        oo_obj = {'id': school[0], 'name': school[1]}
        oo_array.append(oo_obj)
    return jsonify({'oo': oo_array})


@app.route('/api/select/get_parallels/<int:year>/<id_district>/<id_oo>')
@login_required
def api_get_parallels(year, id_district, id_oo):
    if id_oo == "all" and id_district != "all":
        parallels = dbase.get_parallels(id_user=current_user.get_id(),
                                        id_district=id_district,
                                        year=year)
        parallels_array = []
        for parallel in sorted(parallels, key=lambda x: x[0]):
            parallels_obj = {'id': parallel, 'name': parallel}
            parallels_array.append(parallels_obj)
        return jsonify({'parallels': parallels_array})
    else:
        if id_oo == "all":
            parallels = dbase.get_all_parallels(year=year)
            parallels_array = []
            for parallel in sorted(parallels, key=lambda x: x[0]):
                parallels_obj = {'id': parallel, 'name': parallel}
                parallels_array.append(parallels_obj)
            return jsonify({'parallels': parallels_array})
        else:
            parallels = dbase.get_parallels_for_oo(id_oo)
            parallels_array = []
            for parallel in sorted(parallels, key=lambda x: x[1]):
                parallels_obj = {'id': parallel[0], 'name': parallel[1]}
                parallels_array.append(parallels_obj)

            return jsonify({'parallels': parallels_array})


@app.route('/api/select/get_subjects/<year>/<id_district>/<id_oo>/<parallel>')
@login_required
def api_get_subjects(year, id_district, id_oo, parallel):
    if id_district == "all" or id_oo == "all":
        subjects = dbase.get_subjects(parallel=parallel,
                                      id_user=current_user.get_id(),
                                      id_district=id_district,
                                      year=year)
        subjects_array = []
        for subject in sorted(subjects, key=lambda x: x[1]):
            subjects_obj = {'id': subject[0], 'name': subject[1]}
            subjects_array.append(subjects_obj)

        return jsonify({'subjects': subjects_array})
    else:
        subjects = dbase.get_subjects_for_oo_parallels(id_oo_parallels=parallel)
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


@app.errorhandler(403)
def page_not_allowed(error):
    return "Недостаточно прав", 403


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
