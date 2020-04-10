class Battery:

    TECHNOLOGY = ["Li-Ion", "PbA", "NiMh"]

    MANUFACTURING_ENERGY = {"Li-Ion": 164.8,    # IN MEGAJOULES [MJ]
                            "PbA": 29.175,
                            "NiMh": 204.143}

    DISPOSAL_KG = {"Li-Ion": 0.552,              # IN [KG]
                   "PbA": 0.388,
                   "NiMh": 0.670}

    DENSITY_WH_KG = {"Li-Ion": 140,
                     "PbA": 27,
                     "NiMh": 73}

    EFFICIENCY = {"Li-Ion": 90,
                  "PbA": 80,
                  "NiMh": 66}

    LIFETIME = {"Li-Ion": 15,
                "PbA": 3.85,
                "NiMh": 7.95}

    default_data = {
        'technology': None,
        'lifetime': 0,
        'efficiency': 0,
        'density': 0,
        'capacity': 0,
        'weight': 0,
        'e_manufacturing': None,
        'disposal': None
    }

    def __init__(self, data=default_data):
        self.technology = data.get('technology')
        self.lifetime = data.get('lifetime')
        self.efficiency = data.get('efficiency')
        self.density = data.get('density')
        self.capacity = data.get('capacity')
        self.weight = data.get('weight')
        
        self.battery_validation()

        self.complete_fields()
        self.compute_e_manufacturing()
        self.compute_disposal()
    
    def battery_validation(self):
        validation_satus = {}
        validation_satus['technology'] = self.technology in self.TECHNOLOGY
        validation_satus['lifetime'] = self.lifetime >= 0.0
        validation_satus['efficiency'] = self.efficiency >= 0.0 and self.efficiency < 100
        validation_satus['density'] = self.density >= 0.0
        validation_satus['capacity'] = self.capacity > 0.0
        validation_satus['weight'] = self.weight > 0.0
        if all(value for value in validation_satus.values()):
            return True
        else:
            raise BatteryError(validation_satus)

    def compute_e_manufacturing(self):
        self.e_manufacturing = self.weight *\
            self.MANUFACTURING_ENERGY[self.technology]

    def compute_disposal(self):
        self.disposal = self.weight * self.DISPOSAL_KG[self.technology]

    def complete_fields(self):
        self.auto_set_eff() if self.efficiency is 0 else self.efficiency
        self.auto_set_lifetime() if self.lifetime is 0 else self.lifetime
        self.auto_set_density() if self.density == 0 else self.density

    def auto_set_eff(self):
        self.efficiency = self.EFFICIENCY[self.technology]

    def auto_set_lifetime(self):
        self.lifetime = self.LIFETIME[self.technology]

    def auto_set_density(self):
        self.density = self.DENSITY_WH_KG[self.technology]

class BatteryError(Exception):
    def __init__(self, message):
        self.message = message