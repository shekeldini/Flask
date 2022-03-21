from flask import Blueprint, request, g, jsonify
from flask_login import login_required, current_user
from data_base.postgresql import Postgresql
from blueprints.task_description.task_description import blueprint_task_description
from blueprints.vpr_analysis.vpr_analysis import blueprint_vpr_analysis
from blueprints.school_in_risk.school_in_risk import blueprint_school_in_risk

dbase: Postgresql

blueprint_select = Blueprint(
    'select',
    __name__
)
blueprint_select.register_blueprint(blueprint_task_description, url_prefix="/task_description")
blueprint_select.register_blueprint(blueprint_vpr_analysis, url_prefix="/vpr_analysis")
blueprint_select.register_blueprint(blueprint_school_in_risk, url_prefix="/school_in_risk")



@blueprint_select.before_request
def before_request():
    """Установление соединения с БД перед выполением запроса"""
    global dbase
    db_connect = g.get('link_db')
    dbase = Postgresql(db_connect)


@blueprint_select.teardown_request
def teardown_request(request):
    global dbase
    dbase = None
    return request


@blueprint_select.route("/get_year/")
@login_required
def api_get_year():
    years = dbase.get_years(id_user=current_user.get_id())
    years_array = []
    if years:
        for year in years:
            if int(year) != 2022:
                year_obj = {'id': year, 'name': year}
                years_array.append(year_obj)
    return jsonify({'year': years_array})


@blueprint_select.route("/get_districts/")
@login_required
def api_get_districts():
    years = request.args.get("filter_year_id").split(",")
    district_array = []
    districts = dbase.get_districts(id_user=current_user.get_id(),
                                    years=years)
    for district in districts:
        district_obj = {'id': district[0], 'name': district[1].replace("_", " ")}
        district_array.append(district_obj)

    if current_user.get_id_role() in {1, 2} and len(district_array) > 1:
        district_array.insert(0, {'id': "all", 'name': "Все муниципалитеты"})
    return jsonify({'districts': district_array})


@blueprint_select.route('/get_oo/')
@login_required
def get_oo():
    years = request.args.get("filter_year_id").split(",")
    id_district = request.args.get("filter_district_id")
    oo_array = []

    if id_district == "all":
        oo_array.append({'id': "all", 'name': "Все ОО"})
        return jsonify({'oo': oo_array})

    oo_list = dbase.get_oo_from_district(id_district=id_district,
                                         id_user=current_user.get_id(),
                                         years=years)
    for id_oo, name in oo_list:
        oo_obj = {'id': dbase.get_school_login(id_oo=id_oo), 'name': name}
        oo_array.append(oo_obj)

    if current_user.get_id_role() in {1, 2, 3} and len(oo_array) > 1:
        oo_array.insert(0, {'id': "all", 'name': "Все ОО"})
    return jsonify({'oo': oo_array})


@blueprint_select.route('/get_parallels/')
@login_required
def api_get_parallels():
    years = request.args.get("filter_year_id").split(",")
    id_district = request.args.get("filter_district_id")
    id_oo = request.args.get("filter_oo_id")
    parallels_array = []
    if id_oo == "all" and id_district != "all":
        parallels = dbase.get_parallels(id_user=current_user.get_id(),
                                        id_district=id_district,
                                        years=years)

        for parallel in sorted(parallels):
            parallels_obj = {'id': parallel, 'name': parallel}
            parallels_array.append(parallels_obj)

        return jsonify({'parallels': parallels_array})
    else:
        if id_district == "all":
            parallels = dbase.get_all_parallels(years=years)
            for parallel in sorted(parallels):
                parallels_obj = {'id': parallel, 'name': parallel}
                parallels_array.append(parallels_obj)
            return jsonify({'parallels': parallels_array})
        else:
            parallels = dbase.get_parallels_for_oo(oo_login=id_oo,
                                                   years=years)
            for parallel in sorted(parallels):
                parallels_obj = {'id': parallel, 'name': parallel}
                parallels_array.append(parallels_obj)

            return jsonify({'parallels': parallels_array})


@blueprint_select.route('/get_subjects/')
@login_required
def api_get_subjects():
    years = request.args.get("filter_year_id").split(",")
    id_district = request.args.get("filter_district_id")
    oo_login = request.args.get("filter_oo_id")
    parallel = request.args.get("filter_parallel_id")
    subjects_array = []
    if id_district == "all" or oo_login == "all":
        subjects = dbase.get_subjects(parallel=parallel,
                                      id_user=current_user.get_id(),
                                      id_district=id_district,
                                      years=years)

        for id_subject, subject_name in sorted(subjects, key=lambda x: x[1]):
            subjects_obj = {'id': id_subject, 'name': subject_name}
            subjects_array.append(subjects_obj)

        return jsonify({'subjects': subjects_array})
    else:
        subjects = dbase.get_subjects_for_oo(oo_login=oo_login,
                                             parallel=parallel,
                                             id_user=current_user.get_id(),
                                             years=years)
        for id_subject, subject_name in sorted(subjects, key=lambda x: x[1]):
            subjects_obj = {'id': id_subject, 'name': subject_name}
            subjects_array.append(subjects_obj)

        return jsonify({'subjects': subjects_array})

