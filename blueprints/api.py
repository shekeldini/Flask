from flask import Blueprint
from blueprints.select.select import blueprint_select
from blueprints.export.export import blueprint_export

blueprint_api = Blueprint(
    'api',
    __name__
)

blueprint_api.register_blueprint(blueprint_select, url_prefix="/select")
blueprint_api.register_blueprint(blueprint_export, url_prefix="/export")
