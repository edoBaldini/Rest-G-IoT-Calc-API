from iot_green_calculator.solar_panel import Solar_Panel
from iot_green_calculator.battery import Battery
from iot_green_calculator.maintenance import Maintenance

def greenComputation(maintenance):
    device = maintenance.device
    solar_panel = Solar_Panel(maintenance.solar_panel).__dict__
    battery = Battery(maintenance.battery).__dict__
    green_solar_panel = compute_g_sp(device, solar_panel, battery)
    print('\n\n\n\n', green_solar_panel, '\n\n\n\n')
    green_battery = compute_g_b(device, solar_panel, battery)
    green_maintenance = compute_g_m(maintenance, green_solar_panel, green_battery)
    return (green_solar_panel, green_battery, green_maintenance)


def compute_g_sp(device, solar_panel, battery):
    battery_eff = battery['efficiency'] / 100
    solar_panel_eff = solar_panel['efficiency'] / 100
    solar_panel_eff_w = solar_panel['efficiency_w'] / 100
    output_regulator = device['output_regulator'] / 100
    # energy in kWh
    daily_e_required = convert_Mj_kWh(device['daily_e_required'])
    g_surface = daily_e_required / (solar_panel_eff *
                                    battery_eff *
                                    solar_panel_eff_w *
                                    output_regulator *
                                    solar_panel['irradiance'])
    solar_panel['surface'] = g_surface
    solar_panel['weight'] = 0
    return Solar_Panel(solar_panel)

def compute_g_b(device, solar_panel, battery):
    battery_eff = battery['efficiency'] / 100
    battery_dens = battery['density']
    output_regulator = device['output_regulator'] / 100
    device_daily_e_mWh = convert_Mj_kWh(device['daily_e_required']) * (10 ** 6)
    
    g_capacity = (device_daily_e_mWh / (battery_eff * output_regulator))\
        * (1 - (solar_panel['s_hours'] / 24))

    g_weight = (1 / battery_dens) * g_capacity * (10 ** (-3))

    battery['capacity'] = g_capacity
    battery['weight'] = g_weight

    return Battery(battery)

def compute_g_m(maintenance, g_solar_panel, g_battery):
    maintenance.solar_panel = g_solar_panel.__dict__
    maintenance.battery = g_battery.__dict__
    return Maintenance(maintenance.__dict__)


def convert_Mj_kWh(value_Mj):
    return (value_Mj * (10 ** 3) / 3600)