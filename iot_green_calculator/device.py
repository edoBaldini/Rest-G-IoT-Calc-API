class Device:

    default_data = {
        'boards': [],
        'sensors': [],
        'processor': None,
        'radio': None, 
        'active_mode': None,
        'sleep_mode': None,
        'duty_cycle': 0,
        'voltage': 0,
        'daily_e_required': None,
        'e_manufacturing': None,
        'disposal': None, 
        'output_regulator': 0
    }

    def __init__(self, data=default_data):
        self.duty_cycle = data.get('duty_cycle')
        self.voltage = data.get('voltage')
        self.output_regulator = data.get('output_regulator')
        self.active_mode = 0
        self.sleep_mode = 0
        self.device_validation()

        ''' these fields do not need a validation because the validation
            is done in the in the element and board constructor '''
        try:
            self.add_multiple_boards(data.get('boards'))
        except (BoardError, ElementError) as e:
            raise DeviceError('error in the provided boards')
        try:
            self.add_multiple_sensors(data.get('sensors'))
        except (BoardError, ElementError) as e:
            raise DeviceError('error in the provided sensors')
        try:
            self.processor = Element(data.get('processor'))
        except (BoardError, ElementError) as e:
            raise DeviceError('error in the processor')
        try:
            self.radio = Element(data.get('radio'))
        except (BoardError, ElementError) as e:
            raise DeviceError('error in the provided radio')
        
        self.compute_e_manufacturing(self.sensors, self.processor, self.radio)
        self.compute_disposal(self.boards)
        self.compute_active_sleep()
        self.compute_e_required(self.duty_cycle, self.active_mode, self.sleep_mode, self.voltage)


    def device_validation(self):
        validation_satus = {}
        validation_satus['duty_cycle'] = self.duty_cycle > 0.0 and self.duty_cycle < 100
        validation_satus['voltage'] = self.voltage > 0.0
        validation_satus['output_regulator'] = self.output_regulator > 0.0 and self.output_regulator < 100.0

        if all(value for value in validation_satus.values()):
            return True
        else:
            raise DeviceError(validation_satus)

    def add_multiple_boards(self, boards):
        self.boards = []
        for b in boards:
            new_board = Board(b)
            self.boards.append(new_board)
    
    def add_multiple_sensors(self, sensors):
        self.sensors = []
        for s in sensors:
            new_sensor = Element(s)
            self.sensors.append(new_sensor)

    def compute_e_manufacturing(self, sensors, processor, radio):
        self.e_manufacturing = 0
        for s in sensors:
            self.e_manufacturing += s.e_manufacturing
        self.e_manufacturing += processor.e_manufacturing
        self.e_manufacturing += radio.e_manufacturing

    def compute_disposal(self, boards):
        self.disposal = 0
        for b in boards:
            self.disposal += b.disposal
    
    def compute_active_sleep(self):
        for sensor in self.sensors:
            self.active_mode += sensor.active_mode
            self.sleep_mode += sensor.sleep_mode
        self.active_mode += self.processor.active_mode
        self.active_mode += self.radio.active_mode

        for board in self.boards:
            self.active_mode += board.active_mode
            self.sleep_mode += board.sleep_mode
        self.sleep_mode += self.processor.sleep_mode
        self.sleep_mode += self.radio.sleep_mode    
        
# Energy required daily in Mj
    def compute_e_required(self, duty_cycle, active_mode, sleep_mode, voltage):
        dc = duty_cycle / 100
        self.daily_e_required = ((dc * active_mode) + ((1 - dc) * sleep_mode)) * 3600 * 24 *\
            voltage * 10 ** (-9)

class DeviceError(Exception):
    def __init__(self, message):
        self.message = message


class Board():

    DISPOSAL_KG = 0.38

    default_data = {
        'weight': 0,
        'active_mode': 0,
        'sleep_mode': 0,
        'disposal': None,
    }

    def __init__(self, data=default_data):
       self.weight = data.get('weight')
       self.active_mode = data.get('active_mode')
       self.sleep_mode = data.get('sleep_mode')
       
       self.board_validation()

       self.compute_disposal()
    

    def board_validation(self):
        validation_status = {}
        validation_status['weight'] = self.weight > 0
        validation_status['active_mode'] = self.active_mode >= 0
        validation_status['sleep_mode'] = self.sleep_mode >= 0
        if all(value for value in validation_status.values()):
            return True
        else:
            raise BoardError(validation_status)

    def compute_disposal(self):
        self.DISPOSAL_KG
        self.disposal = self.weight * self.DISPOSAL_KG

class BoardError(Exception):
    def __init__(self, message):
        self.message = message



class Element():

    MANUFACTURING_ENERGY = 5.544

    default_data = {
        'lifetime': 0,
        'area': 0,
        'active_mode': 0,
        'sleep_mode': 0,
        'e_manufacturing': None
    }

    def __init__(self, data=default_data):
       self.area = data.get('area')
       self.lifetime = data.get('lifetime')
       self.active_mode = data.get('active_mode')
       self.sleep_mode = data.get('sleep_mode')
       self.element_validation()

       self.compute_e_manufacturing()

    def element_validation(self):
        validation_status = {}
        validation_status['area'] = self.area > 0
        validation_status['lifetime'] = self.lifetime > 0
        validation_status['active_mode'] = self.active_mode > 0
        validation_status['sleep_mode'] = self.sleep_mode >= 0
        if all(value for value in validation_status.values()):
            return True
        else:
            raise ElementError(validation_status)

    def compute_e_manufacturing(self):
        self.MANUFACTURING_ENERGY  # needed to put this data in __dict__
        self.e_manufacturing = self.area * self.MANUFACTURING_ENERGY

class ElementError(Exception):
    def __init__(self, message):
        self.message = message