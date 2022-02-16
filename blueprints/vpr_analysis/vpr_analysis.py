from flask import Blueprint, g, jsonify
from flask_login import login_required
from postgresql import Postgresql

dbase: Postgresql

blueprint_vpr_analysis = Blueprint(
    'vpr_analysis',
    __name__
)


@blueprint_vpr_analysis.before_request
def before_request():
    """Установление соединения с БД перед выполением запроса"""
    global dbase
    db_connect = g.get('link_db')
    dbase = Postgresql(db_connect)


@blueprint_vpr_analysis.teardown_request
def teardown_request(request):
    global dbase
    dbase = None
    return request


@blueprint_vpr_analysis.route("/get_reports")
@login_required
def api_get_reports():
    reports = ["Статистика по отметкам", "Сравнение отметок с отметками по журналу", "Результаты ВПР"]
    reports_array = []
    for report_id, report in enumerate(reports):
        reports_obj = {'id': report_id, 'name': report}
        reports_array.append(reports_obj)
    return jsonify({'reports': reports_array})
