import logging

from flask import request
from flask_restplus import Resource
from iot_green_calculator.api.solar_panel_serializer import solar_panel_input_fields, solar_panel, solar_panel_not_valid_fields
from iot_green_calculator.api.restplus import api
from iot_green_calculator.solar_panel import Solar_Panel, SolarPanelError

log = logging.getLogger(__name__)

ns = api.namespace('solar_panel', description='Solar panel operations')


@ns.route('/')
class CategoryCollection(Resource):
    @api.marshal_with(solar_panel)
    def get(self):
        return {}

    @api.expect(solar_panel_input_fields)
    @api.response(200, 'solar panel analyzed', solar_panel)
    @api.response(400, 'input not valid', solar_panel_not_valid_fields)
    def post(self):
        data = request.json
        try:
            solar_panel = Solar_Panel(data) # inside the solar panel constructor there is an additional validator
        except SolarPanelError as e:
            print(e.message)
            return e.message, 400
        
        return solar_panel.__dict__


