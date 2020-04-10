from flask_restplus import fields
from iot_green_calculator.api.restplus import api

battery_input_fields = api.model('Battery input fields', {
    'technology': fields.String(required=True, description='Battery technology can be\
                                                            lithium, pba, NiMh'),
    'lifetime': fields.Float(description='Lifetime of the battery'),
    'efficiency': fields.Float(description='Efficiency of the battery'),
    'density': fields.Float(description='Density of the battery'),
    'capacity': fields.Float(required=True, description='Capacity of the battery'),
    'weight': fields.Float(required=True, description='Weight of the battert'),
})

battery = api.inherit('Battery', battery_input_fields, {
    'e_manufacturing': fields.Float(description='Energy spent\
                                for the production of the battery in Mj'),
    'disposal': fields.Float(description='Kg of waste produced\
                                by the battery disposal'),
})

battery_not_valid_fields = api.model('Battery fields not valid', {
    'technology': fields.Boolean(description='The solar panel\
                                    technology can be mono/polycrystalline'),
    'lifetime': fields.Boolean(description='Lifetime of the battery'),
    'efficiency': fields.Boolean(description='Efficiency of the battery'),
    'density': fields.Boolean(description='Density of the battery'),
    'capacity': fields.Boolean(description='Capacity of the battery'),
    'weight': fields.Boolean(description='Weight of the battert')
})