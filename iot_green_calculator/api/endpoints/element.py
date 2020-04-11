import logging

from flask import request
from flask_restplus import Resource
from iot_green_calculator.api.device_serializer import element_input_fields, element
from iot_green_calculator.api.restplus import api
from iot_green_calculator.device import Element, ElementError

log = logging.getLogger(__name__)

ns = api.namespace('element', description='Element operations')


@ns.route('/')
class CategoryCollection(Resource):
    @api.marshal_with(element)
    def get(self):
        return {}

    @api.expect(element_input_fields)
    @api.response(200, 'element analyzed', element)
    def post(self):
        data = request.json
        try:
            element = Element(data)
        except ElementError as e:
            print(e.message)
            return e.message, 400
        
        return element.__dict__


