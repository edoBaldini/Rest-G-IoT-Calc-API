class Solar_Panel:

    TECHNOLOGY = ["mono-Si", "multi-Si"]  # "CdTe"]

    MANUFACTURING_ENERGY = {"mono-Si": 5476.100,  # IN MEGAJOULES [MJ]
                            "multi-Si": 4676.100}
                           # "CdTe": 3749.16}

    DISPOSAL_KG = {"Si": 0.1602}                 # IN KILOGRAMS [Kg]
                   # "CdTe": 0.0487}

    DENSITY_KG_WP = {"Si": 0.102}
                     # "CdTe": 0.202}

    EFFICIENCY = {"mono-Si": 17,               # DEFINED AS [Kwp / m2]
                  "multi-Si": 12.30}
                  
                  # "CdTe": 10.90}
    EFFICIENCY_W = {"mono-Si": 80,
                    "multi-Si": 80}

    WH2MJ = 3600 * 10 ** (- 6)                   # CONVERSION FROM WH TO MJ
    LIFETIME = 43.73

    default_data = {
        'technology': None,
        'surface': 0,                           # squared meters
        'irradiance': 0,                        # daily irradiance in Mj
        's_hours': 0,
        'lifetime': 0,                          # years
        'efficiency': 0,
        'kwp': 0,
        'efficiency_w': 0,                      # wear-out efficiency
        'weight': 0,                            # kg
        'e_manufacturing': None,
        'disposal': None,
        'e_produced': None,
    }

    def __init__(self, data=default_data):
        self.technology = data.get('technology')
        self.surface = data.get('surface')
        self.irradiance = data.get('irradiance')
        self.s_hours = data.get('s_hours')
        self.lifetime = data.get('lifetime')
        self.efficiency = data.get('efficiency')
        self.kwp = data.get('kwp')
        self.efficiency_w = data.get('efficiency_w')
        self.weight = data.get('weight')
        
        self.solar_panel_validation()

#   Lifetime, Efficiency and Efficiency_w if equal to 0 will be replaced with common parameters
        self.complete_fields()
        self.compute_e_manufacturing()
        self.compute_disposal()
        self.daily_energy_produced()

    def solar_panel_validation(self):
        validation_status = {}
        validation_status['technology'] = self.technology in self.TECHNOLOGY
        validation_status['surface'] = self.surface > 0.0
        validation_status['irradiance'] = self.irradiance > 0.0
        validation_status['s_hours'] = (self.s_hours > 0.0 and self.s_hours < 24)
        validation_status['lifetime'] = self.lifetime >= 0.0
        validation_status['efficiency'] = (self.efficiency >= 0.0 and self.efficiency <= 100.0)
        validation_status['kwp'] = self.kwp >= 0
        validation_status['efficiency_w'] = (self.efficiency_w >= 0.0 and self.efficiency_w <= 100.0)
        validation_status['weight'] = self.weight >= 0
        if all(value for value in validation_status.values()):
            return True
        else:
            raise SolarPanelError(validation_status)

    def compute_e_manufacturing(self):
        self.e_manufacturing = self.surface *\
            self.MANUFACTURING_ENERGY[self.technology]

    def compute_disposal(self):
        t = 'Si'
        eff = self.efficiency / 100
        if self.weight == 0:
            self.disposal = eff * self.surface * (10**3) *\
            self.DENSITY_KG_WP[t] * self.DISPOSAL_KG[t]
        else:
            self.disposal = self.weight * self.DISPOSAL_KG[t]

    def daily_energy_produced(self):
        eff = self.efficiency / 100
        self.e_produced = self.surface * self.irradiance * eff *\
            (10**3) * self.WH2MJ

    def complete_fields(self):
        self.auto_set_eff() if self.efficiency is 0 else self.efficiency
        self.auto_set_lifetime() if self.lifetime is 0 else self.lifetime
        self.auto_set_eff_w() if self.efficiency_w is 0 else self.efficiency_w

    def auto_set_eff(self):
        self.efficiency = self.EFFICIENCY[self.technology]
        self.kwp = self.efficiency * self.surface

    def auto_set_lifetime(self):
        self.lifetime = self.LIFETIME

    def auto_set_eff_w(self):
        self.efficiency_w = self.EFFICIENCY[self.technology]


class SolarPanelError(Exception):
    def __init__(self, message):
        self.message = message