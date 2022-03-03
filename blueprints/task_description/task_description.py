from flask import Blueprint, g, jsonify, request
from flask_login import login_required
from data_base.postgresql import Postgresql

dbase: Postgresql

blueprint_task_description = Blueprint(
    'task_description',
    __name__
)


@blueprint_task_description.before_request
def before_request():
    """Установление соединения с БД перед выполением запроса"""
    global dbase
    db_connection = g.get('link_db')
    dbase = Postgresql(db_connection)


@blueprint_task_description.teardown_request
def teardown_request(request):
    global dbase
    dbase = None
    return request


@blueprint_task_description.route("/get_task_numbers/")
@login_required
def api_task_description_get_task_numbers():
    years = request.args.get("filter_year_id").split(",")
    oo_login = request.args.get("filter_oo_id")
    parallel = request.args.get("filter_parallel_id")
    id_subjects = request.args.get("filter_subject_id")

    task_numbers_array = [{'id': "all", 'name': "Все задания"}]

    task_numbers = dbase.get_task_number_from_kim_by_id_oo_parallels_subjects(year=years[0],
                                                                              oo_login=oo_login,
                                                                              parallel=parallel,
                                                                              id_subjects=id_subjects)

    for key, value in task_numbers:
        task_numbers_array.append({'id': key, 'name': value})
    return jsonify({'task_numbers': task_numbers_array})


@blueprint_task_description.route("/get_reports/")
@login_required
def api_task_description_get_reports():
    task_number = request.args.get("filter_task_number")
    if task_number == "all":
        return jsonify({'reports': [{'id': 4, 'name': "Описание работы"}]})
    else:
        return jsonify({'reports': [{'id': 5, 'name': "Распределение заданий по позициям кодификаторов"}]})
