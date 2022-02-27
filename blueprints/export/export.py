from io import BytesIO

from flask import Blueprint, request, g, Response
from flask_login import login_required, current_user
from data_base.postgresql import Postgresql
from classReportController import ReportController

db_connection = None

blueprint_export = Blueprint(
    'export',
    __name__
)


@blueprint_export.before_request
def before_request():
    """Установление соединения с БД перед выполением запроса"""
    global db_connection
    db_connection = g.get('link_db')


@blueprint_export.teardown_request
def teardown_request(request):
    global db_connection
    db_connection = None
    return request


@blueprint_export.route("/")
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
    report = ReportController(request=export_data, connection=db_connection, user=current_user)
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
