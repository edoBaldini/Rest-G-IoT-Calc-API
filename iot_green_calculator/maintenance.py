from iot_green_calculator.solar_panel import Solar_Panel, SolarPanelError 
from iot_green_calculator.battery import Battery, BatteryError
from iot_green_calculator.device import Device, DeviceError

class Maintenance:

    KWH_TO_MJ = 3600 * (10 ** (-3))
    CONV_FACTOR = 9.2                   # from liter of fuel to kWh
    AVG_FUEL_CONS = 5
   
    default_data = {
        'avg_distance': 0,
        'avg_fuel_cons': 0,
        'conv_factor': 0,
        'n_devices': 0,
        'lifetime': 0,
        'e_intervention': None,
        'battery': None,
        'solar_panel': None,
        'device': None,
        'sensors': None,
        'tot_e_intervention': None,
        'n_interventions': None,
        'tot_main_energy': None,
        'tot_main_disposal': None,
    }
    
    def __init__(self, data=default_data):
        self.avg_distance = data.get('avg_distance')
        self.avg_fuel_cons = data.get('avg_fuel_cons')
        self.conv_factor = data.get('conv_factor')
        self.n_devices = data.get('n_devices')
        self.lifetime = data.get('lifetime')
        self.e_intervention = data.get('e_intervention')
        self.battery =  data.get('battery')
        self.solar_panel =  data.get('solar_panel')
        self.device =  data.get('device')
        self.sensors = data.get('sensors')
        self.tot_e_intervention = data.get('tot_e_intervention')
        self.n_interventions = data.get('n_interventions')
        self.tot_main_energy = data.get('tot_main_energy')
        self.tot_main_disposal = data.get('tot_main_disposal')

        self.maintenance_validation()

        self.complete_fields()
        self.compute_e_intervention()

    def compute_e_intervention(self):
        self.e_intervention = (self.avg_distance * self.avg_fuel_cons) / 100 *\
            self.conv_factor * self.KWH_TO_MJ

    def complete_fields(self):
        self.avg_fuel_cons = self.AVG_FUEL_CONS if self.avg_fuel_cons == 0 else self.avg_fuel_cons
        self.conv_factor = self.CONV_FACTOR if self.conv_factor == 0 else self.conv_factor
    
    def maintenance_validation(self):
        validation_satus = {}
        validation_satus['avg_distance'] = self.avg_distance > 0.0
        validation_satus['avg_fuel_cons'] = self.avg_fuel_cons >= 0.0
        validation_satus['conv_factor'] = self.conv_factor >= 0.0
        validation_satus['n_devices'] = self.n_devices > 0.0
        validation_satus['lifetime'] = self.lifetime > 0.0
        try:
            device = Device(self.device)
            validation_satus['device'] = True
        except Exception as e:
            validation_satus['device'] = False
        try:
            solar_panel = Solar_Panel(self.solar_panel)
            validation_satus['solar_panel'] = True
        except Exception as e:
            validation_satus['solar_panel'] = False
        try:
            battery = Battery(self.battery)
            validation_satus['battery'] = True
        except Exception as e:
            validation_satus['battery'] = False

        if all(value for value in validation_satus.values()):
            return True
        else:
            raise MaintenanceError(validation_satus)

class MaintenanceError(Exception):
    def __init__(self, message):
        self.message = message
