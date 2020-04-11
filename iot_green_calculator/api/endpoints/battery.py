import logging

from flask import request
from flask_restplus import Resource
from iot_green_calculator.api.battery_serializer import battery_input_fields, battery, battery_not_valid_fields
from iot_green_calculator.api.restplus import api
from iot_green_calculator.battery import Battery, BatteryError

log = logging.getLogger(__name__)

ns = api.namespace('battery', description='Battery operations')


@ns.route('/')
class CategoryCollection(Resource):
    @api.marshal_with(battery)
    def get(self):
        return {}

    @api.expect(battery_input_fields)
    @api.response(200, 'battery analyzed', battery)
    @api.response(400, 'input not valid', battery_not_valid_fields)
    def post(self):
        data = request.json
        try:
            battery = Battery(data) # inside the battery constructor there is an additional validator
        except BatteryError as e:
            print(e.message)
            return e.message, 400
        
        return battery.__dict__


