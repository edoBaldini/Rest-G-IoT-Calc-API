import logging

from flask import request
from flask_restplus import Resource
from iot_green_calculator.api.device_serializer import board_input_fields, board
from iot_green_calculator.api.restplus import api
from iot_green_calculator.device import Board, BoardError

log = logging.getLogger(__name__)

ns = api.namespace('board', description='Board operations')


@ns.route('/')
class CategoryCollection(Resource):
    @api.marshal_with(board)
    def get(self):
        return {}

    @api.expect(board_input_fields)
    @api.response(200, 'board analyzed', board)
    def post(self):
        data = request.json
        try:
            board = Board(data)
        except BoardError as e:
            print(e.message)
            return e.message, 400
        
        return board.__dict__


