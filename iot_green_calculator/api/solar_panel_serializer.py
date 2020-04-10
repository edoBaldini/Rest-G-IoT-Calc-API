from flask_restplus import fields
from iot_green_calculator.api.restplus import api

solar_panel_input_fields = api.model('Solar Panel input fields', {
    'technology': fields.String(required=True, description='The solar panel\
                                    technology can be mono/polycrystalline'),
    'surface': fields.Float(required=True, description='Solar panel surface\
                                    in m2'),
    'irradiance': fields.Float(required=True, description='Daily irradiance\
                                    level of the deployment place in kWh'),
    's_hours': fields.Float(required=True, description='Daily hours of light', ),
    'lifetime': fields.Float(description='Lifetime of the solar\
                                    panel'),
    'efficiency': fields.Float(description='Efficiency of the\
                                    solar panel'),
    'kwp': fields.Float(description='Solar panel production in\
                                    ideal condition in kWp'),
    'efficiency_w': fields.Float(description='Efficiency due to\
                                    the wear out'),
    'weight': fields.Float(required=True, description='Weight of the solar\
                                    panel'),
})

solar_panel = api.inherit('Solar Panel', solar_panel_input_fields, {
    'e_manufacturing': fields.Float(description='Energy spent\
                                for the production of the solar panel in Mj'),
    'disposal': fields.Float(description='Kg of waste produced\
                                by the solar panel disposal'),
    'e_produced': fields.Float(description='Daily energy\
                                produced by the solar panel in Mj'),
})

solar_panel_not_valid_fields = api.model('Solar panel fields not valid', {
    'technology': fields.Boolean(description='The solar panel\
                                    technology can be mono/polycrystalline'),
    'surface': fields.Boolean(description='Solar panel surface\
                                    in m2'),
    'irradiance': fields.Boolean(description='Daily irradiance\
                                    level of the deployment place in kWh'),
    's_hours': fields.Boolean(description='Daily hours of light'),
    'lifetime': fields.Boolean(description='Lifetime of the solar\
                                    panel'),
    'efficiency': fields.Boolean(description='Efficiency of the\
                                    solar panel'),
    'kwp': fields.Boolean(description='Solar panel production in\
                                    ideal condition in kWp'),
    'efficiency_w': fields.Boolean(description='Efficiency due to\
                                    the wear out'),
    'weight': fields.Boolean(description='Weight of the solar\
                                    panel'),
})