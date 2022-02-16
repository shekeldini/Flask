from flask import Blueprint, g, jsonify
from flask_login import login_required
from postgresql import Postgresql

dbase: Postgresql

blueprint_task_description = Blueprint(
    'task_description',
    __name__
)


@blueprint_task_description.before_request
def before_request():
    """Установление соединения с БД перед выполением запроса"""
    global dbase
    db_connect = g.get('link_db')
    dbase = Postgresql(db_connect)


@blueprint_task_description.teardown_request
def teardown_request(request):
    global dbase
    dbase = None
    return request


@blueprint_task_description.route("/get_task_numbers/<year>/<id_oo>/<int:parallel>/<int:id_subject>",
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


@blueprint_task_description.route("/get_reports/<task_number>", methods=["POST", "GET"])
@login_required
def api_task_description_get_reports(task_number):
    if task_number == "all":
        return jsonify({'reports': [{'id': 4, 'name': "Описание работы"}]})
    else:
        return jsonify({'reports': [{'id': 5, 'name': "Распределение задания по позициям кодификаторов"}]})
