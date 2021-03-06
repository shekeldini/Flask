from flask import Blueprint, g, jsonify
from flask_login import login_required, current_user
from data_base.classDataBaseSchoolsInRisk import DataBaseSchoolsInRisk

db_connection = None
dbase: DataBaseSchoolsInRisk

blueprint_school_in_risk = Blueprint(
    'school_in_risk',
    __name__
)


@blueprint_school_in_risk.before_request
def before_request():
    """Установление соединения с БД перед выполением запроса"""
    global db_connection, dbase
    db_connection = g.get('link_db')
    dbase = DataBaseSchoolsInRisk(db_connection)


@blueprint_school_in_risk.teardown_request
def teardown_request(request):
    global db_connection, dbase
    db_connection = None
    dbase = None
    return request

@blueprint_school_in_risk.route("/get_year/")
@login_required
def api_get_year():
    years = dbase.get_years(id_user=current_user.get_id())
    years_array = []
    for year in years:
        year_obj = {'id': year, 'name': year}
        years_array.append(year_obj)
    return jsonify({'year': years_array})


@blueprint_school_in_risk.route("/get_districts/<year>")
@login_required
def api_districts_for_school_in_risk(year):
    districts = dbase.get_districts(id_user=current_user.get_id(),
                                    year=year)
    district_array = []
    if districts:
        if current_user.get_id_role() in {1, 2}:
            district_array.append({'id': "all", 'name': "Все муниципалитеты"})

        for id_district, district in districts:
            district_obj = {'id': id_district, 'name': district.replace("_", " ")}
            district_array.append(district_obj)
    return jsonify({'districts': district_array})

@blueprint_school_in_risk.route('/get_oo/<year>/<id_district>')
@login_required
def api_get_oo_for_schools_in_risk(year, id_district):
    oo_array = []
    if id_district == "all":
        oo_array.append({'id': "all", 'name': "Все ОО"})
        return jsonify({'oo': oo_array})
    oo = dbase.get_oo_by_district(id_district=id_district,
                                  id_user=current_user.get_id(),
                                  year=year)
    if current_user.get_id_role() in {1, 2, 3} and len(oo) > 1:
        oo_array.append({'id': "all", 'name': "Все ОО"})

    for id_school, school in oo:
        oo_obj = {'id': id_school, 'name': school}
        oo_array.append(oo_obj)
    return jsonify({'oo': oo_array})


@blueprint_school_in_risk.route('/get_parallels/<year>/<id_district>/<id_oo>')
@login_required
def api_get_parallels_for_schools_in_risk(year, id_district, id_oo):
    parallels_array = []
    for parallel in dbase.get_parallels(year=year,
                                        id_district=id_district,
                                        id_oo=id_oo):
        parallels_array.append({'id': parallel, 'name': parallel})
    return jsonify({'parallels': parallels_array})


@blueprint_school_in_risk.route('/get_subject/<year>/<id_district>/<id_oo>/<parallel>')
@login_required
def api_get_subject_for_schools_in_risk(year, id_district, id_oo, parallel):
    subject_array = []
    for id_subject, subject in dbase.get_subjects(year=year,
                                                  id_district=id_district,
                                                  id_oo=id_oo,
                                                  parallel=parallel):
        subject_array.append({'id': id_subject, 'name': subject})
    return jsonify({'subjects': subject_array})
