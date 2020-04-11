import logging

from flask import request
from flask_restplus import Resource
from iot_green_calculator.api.device_serializer import device_input_fields, device
from iot_green_calculator.api.restplus import api
from iot_green_calculator.device import Device, DeviceError

log = logging.getLogger(__name__)

ns = api.namespace('device', description='Device operations')


@ns.route('/')
class CategoryCollection(Resource):
    @api.marshal_with(device)
    def get(self):
        return {}

    @api.expect(device_input_fields)
    @api.response(200, 'device analyzed', device)
    def post(self):
        data = request.json
        try:
            device = Device(data)
        except DeviceError as e:
            print(e.message)
            return e.message, 400
        
        return self.device_jsonified(device).__dict__

    def device_jsonified(self, device):
        processor = device.processor.__dict__
        radio = device.radio.__dict__
        boards = [b.__dict__ for b in device.boards]
        sensors = [s.__dict__ for s in device.sensors]

        device_json = device

        device_json.processor = processor
        device_json.radio = radio
        device_json.sensors = sensors
        device_json.boards = boards
        return device_json