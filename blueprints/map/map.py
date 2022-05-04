from flask import Blueprint, g, jsonify, request
from flask_login import login_required, current_user

from data_base.map import Map


dbase: Map

blueprint_map = Blueprint(
    'map',
    __name__
)


@blueprint_map.before_request
def before_request():
    """Установление соединения с БД перед выполением запроса"""
    global dbase
    db_connection = g.get('link_db')
    dbase = Map(db_connection)


@blueprint_map.teardown_request
def teardown_request(request):
    global dbase
    dbase = None
    return request


@blueprint_map.route("/get_year/")
@login_required
def api_get_year():
    years = dbase.get_years(id_user=current_user.get_id())
    years_array = []
    if years:
        for year in sorted(years, key=lambda x: int(x[0])):
            year_obj = {'id': year, 'name': year}
            years_array.append(year_obj)
    return jsonify({'year': years_array})


@blueprint_map.route("/get_parallels/")
@login_required
def api_get_parallels():
    years = request.args.get("filter_year_id").split(",")

    parallels = dbase.get_parallels_by_year(id_user=current_user.get_id(),
                                            years=years)
    parallels_array = []
    for parallel in sorted(parallels,key=lambda x: int(x[0])):
        parallels_array.append({'id': parallel, 'name': parallel})
    return jsonify({'parallels': parallels_array})


@blueprint_map.route('/get_subjects/')
@login_required
def api_get_subjects():
    years = request.args.get("filter_year_id").split(",")
    parallel = request.args.get("filter_parallel_id")
    subjects_array = []
    subjects = dbase.get_subjects(parallel=parallel,
                                  id_user=current_user.get_id(),
                                  id_district="all",
                                  years=years)
    for id_subject, subject_name in sorted(subjects, key=lambda x: x[1]):
        subjects_obj = {'id': id_subject, 'name': subject_name}
        subjects_array.append(subjects_obj)

    return jsonify({'subjects': subjects_array})


@blueprint_map.route("/get_reports")
@login_required
def api_get_reports():
    reports = ["Средняя отметка"]
    reports_array = []
    for report_id, report in enumerate(reports, start=6):
        reports_obj = {'id': report_id, 'name': report}
        reports_array.append(reports_obj)
    return jsonify({'reports': reports_array})


@blueprint_map.route("/get_schools_coordinates/")
@login_required
def api_get_schools_coordinates():
    id_year = request.args.get("id_year")
    district_name = request.args.get("district_name")
    id_subjects = int(request.args.get("id_subjects"))
    id_parallels = int(request.args.get("id_parallels"))
    schools = []
    if id_year and district_name and id_subjects and id_parallels:
        oo_logins_list = dbase.get_oo(
            id_district=dbase.get_id_district_by_name(district_name),
            id_subjects=id_subjects,
            parallel=id_parallels,
            years=[id_year]
        )
        for oo_login in oo_logins_list:
            oo_value = dbase.get_mean_mark_for_oo(
                oo_login=oo_login,
                id_subjects=id_subjects,
                parallel=id_parallels,
                year=id_year
            )
            oo_name = dbase.get_oo_name_by_oo_login(
                oo_login=oo_login,
                year=id_year
            )
            coordinates = dbase.get_coordinates_for_oo(
                year=id_year,
                oo_login=oo_login
            )
            if coordinates:
                schools.append(
                    {
                        "name": oo_name,
                        "coordinates": coordinates,
                        "oo_login": oo_login,
                        "value": oo_value,
                        "text": "Средняя по ВПР: ",
                        "district": district_name
                    }
                )

    return jsonify({'schools': schools})
