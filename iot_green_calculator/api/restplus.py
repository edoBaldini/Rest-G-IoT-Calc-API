import logging
import traceback

from flask_restplus import Api
from iot_green_calculator import settings

log = logging.getLogger(__name__)

api = Api(version='1.0', title='G-IoT calculator API',
          description='Green IoT calculator API')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500