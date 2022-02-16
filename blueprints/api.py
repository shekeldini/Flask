from flask import Blueprint
from blueprints.select.select import select
from blueprints.vpr_analysis.vpr_analysis import blueprint_vpr_analysis
from blueprints.task_description.task_description import blueprint_task_description
from blueprints.school_in_risk.school_in_risk import blueprint_school_in_risk
from blueprints.export.export import blueprint_export

blueprint_api = Blueprint(
    'api',
    __name__
)

blueprint_api.register_blueprint(select, url_prefix="/select")
blueprint_api.register_blueprint(blueprint_vpr_analysis, url_prefix="/vpr_analysis")
blueprint_api.register_blueprint(blueprint_task_description, url_prefix="/task_description")
blueprint_api.register_blueprint(blueprint_school_in_risk, url_prefix="/school_in_risk")
blueprint_api.register_blueprint(blueprint_export, url_prefix="/export")