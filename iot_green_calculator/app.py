import logging.config

import os
from flask import Flask, Blueprint
from flask_cors import CORS
from iot_green_calculator import settings
from iot_green_calculator.api.endpoints.solar_panel import ns as solar_panel_namespace
from iot_green_calculator.api.endpoints.battery import ns as battery
from iot_green_calculator.api.endpoints.element import ns as element
from iot_green_calculator.api.endpoints.board import ns as board
from iot_green_calculator.api.endpoints.device import ns as device
from iot_green_calculator.api.endpoints.maintenance import ns as maintenance
from iot_green_calculator.api.restplus import api

app = Flask(__name__)
cors = CORS(app)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(solar_panel_namespace)
    api.add_namespace(battery)
    api.add_namespace(element)
    api.add_namespace(board)
    api.add_namespace(device)
    api.add_namespace(maintenance)
    flask_app.register_blueprint(blueprint)


def main():
    initialize_app(app)
    log.info('Dev server at http://{}/api/'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
