from flask_restplus import fields
from iot_green_calculator.api.restplus import api

element_input_fields = api.model('Element input fields', {
    'area': fields.Float(required=True, description="area in cm2"),
    'lifetime': fields.Float(required=True, description="expected lifetime"),
    'active_mode': fields.Float(required=True, description="mA spent in active mode"),
    'sleep_mode': fields.Float(required=True, description="mA spent in sleepmode"),

})


element = api.inherit('Element', element_input_fields, {
    'e_manufacturing': fields.Float(description='Energy spent\
                                for the production of an element in Mj'),

})

board_input_fields = api.model('Board input fields', {
    'weight': fields.Float(required=True, description="weight in kg"),
    'active_mode': fields.Float(required=True, description="mA spent in active mode"),
    'sleep_mode': fields.Float(required=True, description="mA spent in sleepmode"),
})

board = api.inherit('Board', board_input_fields, {
    'disposal': fields.Float(required=True, description="Kg of waste produced\
                                by the board disposal")
})

device_input_fields = api.model('Device input fields', {
    'duty_cycle': fields.Float(required=True, description='duty cycle'),
    'voltage': fields.Float(required=True, description='operation voltage'),
    'output_regulator': fields.Float(required=True, description='efficiency of the\
                                    output regulator'),
    'boards': fields.List(fields.Nested(board_input_fields)),
    'sensors': fields.List(fields.Nested(element)),
    'processor': fields.Nested(element),
    'radio': fields.Nested(element),
})

device = api.inherit('Device', device_input_fields, {
    'e_manufacturing': fields.Float(description='Energy spent\
                                for the production of the entire device in Mj'),
    'disposal': fields.Float(required=True, description="Kg of waste produced\
                                by the entire device disposal"),
    'daily_e_required': fields.Float(description='Daily energy spent\
                                to run the device in Mj'),
})