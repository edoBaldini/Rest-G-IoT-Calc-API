import logging
import json
import gurobipy as gp

from gurobipy import GRB, quicksum
from flask import request
from flask_restplus import Resource
from iot_green_calculator.api.maintenance_serializer import maintenance_input_fields, maintenance, tot_results
from iot_green_calculator.api.restplus import api
from iot_green_calculator.maintenance import Maintenance, MaintenanceError
from iot_green_calculator.green_proposal import greenComputation
log = logging.getLogger(__name__)

ns = api.namespace('maintenance', description='Maintenance operations')


def default_data():
    return {'avg_distance': 3.505, 'avg_fuel_cons': 6.0, 'conv_factor': 8.9, 'n_devices': 10.0, 'lifetime': 30.0, 'e_intervention': 6.738012,
 'battery': {'technology': 'Li-Ion', 'lifetime': 9.0, 'efficiency': 90.0, 'density': 140.516129, 'capacity': 6600.0, 'weight': 0.155, 'e_manufacturing': 25.544, 'disposal': 0.08556000000000001},
 'solar_panel': {'technology': 'mono-Si', 'surface': 0.03744, 'irradiance': 1.127419355, 's_hours': 9.0, 'lifetime': 20.0, 'efficiency': 17.0, 'kwp': 0, 'efficiency_w': 80.0, 'weight': 0.54, 'e_manufacturing': 205.02518400000002, 'disposal': 0.08650800000000002, 'e_produced': 0.025832875358534402},
 'device': {'duty_cycle': 5, 'voltage': 3.3, 'output_regulator': 90, 'active_mode': 84.189030303, 'sleep_mode': 0.062,
 'boards': [{'weight': 0.02, 'active_mode': 0.0, 'sleep_mode': 0.0, 'disposal': 0.0076},
 {'weight': 0.02, 'active_mode': 0.0, 'sleep_mode': 0.0, 'disposal': 0.0076}],
 'sensors': [{'area': 13.8, 'lifetime': 1000000.0, 'active_mode': 11.0, 'sleep_mode': 0.0, 'e_manufacturing': 76.5072},
 {'area': 0.278, 'lifetime': 1000000.0, 'active_mode': 0.006, 'sleep_mode': 0.0, 'e_manufacturing': 1.541232},
 {'area': 0.283, 'lifetime': 1000000.0, 'active_mode': 0.5, 'sleep_mode': 0.0, 'e_manufacturing': 1.5689519999999997},
 {'area': 0.976, 'lifetime': 1000000.0, 'active_mode': 0.38, 'sleep_mode': 0.0, 'e_manufacturing': 5.410944},
 {'area': 0.665, 'lifetime': 10.0, 'active_mode': 3.0, 'sleep_mode': 0.0, 'e_manufacturing': 3.68676},
 {'area': 0.636, 'lifetime': 10.0, 'active_mode': 6.0, 'sleep_mode': 0.0, 'e_manufacturing': 3.525984},
 {'area': 0.636, 'lifetime': 10.0, 'active_mode': 34.0, 'sleep_mode': 0.0, 'e_manufacturing': 3.525984}],
 'processor': {'area': 2.641, 'lifetime': 1000000.0, 'active_mode': 9.0, 'sleep_mode': 0.062, 'e_manufacturing': 14.641703999999999},
 'radio': {'area': 6.731, 'lifetime': 1000000.0, 'active_mode': 0.303030303, 'sleep_mode': 0.0, 'e_manufacturing': 37.316663999999996},
 'e_manufacturing': 144.14399999999998, 'disposal': 3.42, 'daily_e_required': 0.031477248}, 
 'sensors': {}, 'tot_e_intervention': 0, 'n_interventions': 0, 'tot_main_energy': 0, 'tot_main_disposal': 0} 


@ns.route('/')
class CategoryCollection(Resource):
    @api.marshal_with(maintenance)
    def get(self):
        return {}

    @api.expect(maintenance_input_fields)
    def post(self):
        data = request.json
        try:
            maintenance = Maintenance(data) # inside the maintenance constructor there is an additional validator
            maintenance_aux = Maintenance(data)
            lifetime_units, e_manuf, disposal = prepare_maintenance(maintenance.__dict__)   # default_data())
            results = maintenance_sched(lifetime_units, e_manuf, disposal, maintenance.__dict__)
            # results = maintenance_sched(lifetime_units, e_manuf, disposal, default_data())
        except MaintenanceError as e:
            print(e.message)
            return e.message, 400

            
        green_solar_panel, green_battery, green_maintenance = greenComputation(maintenance_aux) 
        lifetime_units, e_manuf, disposal = prepare_maintenance(green_maintenance.__dict__)
        green_results = maintenance_sched(lifetime_units, e_manuf, disposal, green_maintenance.__dict__)
        r = prepare_result(maintenance)
        g = prepare_result(green_maintenance)
        for i, v in r.items():
            print('real ', i, '-', v, ' green ', g[i])
        return {'maintenance': maintenance.__dict__, 'real': prepare_result(maintenance), 'green': prepare_result(green_maintenance)}

def prepare_result(maintenance):
    solar_panel = {'energy': maintenance.solar_panel['e_manufacturing'], 'disposal': maintenance.solar_panel['disposal']}
    battery = {'energy': maintenance.battery['e_manufacturing'], 'disposal': maintenance.battery['disposal']}
    device = {'energy': maintenance.device['e_manufacturing'], 'disposal': maintenance.device['disposal']}
    maintenance = {'energy': maintenance.tot_main_energy, 'disposal': maintenance.tot_main_disposal}

    tot = {'tot_energy': (solar_panel['energy'] + battery['energy'] + device['energy'] + maintenance['energy']),
            'tot_disposal': (solar_panel['disposal'] + battery['disposal'] + device['disposal'] + maintenance['disposal'])}
   
    result = {'solar_panel': solar_panel, 
                'battery': battery,
                'device': device,
                'maintenance':maintenance,
                'tot': tot
            }

    return result

''' Update the Device removing those sensors that have lifetime smaller than
    application.
    Returns data_for_maint()'''

def prepare_maintenance(dataset):
    maintenance = dataset
    sensors = maintenance['device']['sensors']
    spec_sensors = {}
    index = 0
    for value in sensors:
        if value['lifetime'] < maintenance['lifetime']:
            spec_sensors[index] = value
        index += 1
    return data_for_maint(spec_sensors, dataset)


''' Takes as input a dictionary of sensors and returns a triple with:
    -   a list of the components lifetime
    -   a list of the components energy_manufacturing
    -   a list of the components disposal
    components are sensors, battery, solar_panel and device'''


def data_for_maint(spec_sensors, dataset):
    disposal = {}
    lifetime = {}
    e_manuf = {}
    sens_e_manuf = 0
    for key, item in spec_sensors.items():
        lifetime[len(lifetime)] = item['lifetime']
        e_manuf[len(lifetime)] = item['e_manufacturing']
        sens_e_manuf += item['e_manufacturing']
    for key, value in dataset.items():
        if key == 'battery' or key == 'solar_panel':
            lifetime[key] = value['lifetime']
            e_manuf[key] = value['e_manufacturing']
            disposal[key] = value['disposal']
        if key == 'device':
            e_manuf[key] = (value['e_manufacturing'] - sens_e_manuf)
            disposal[key] = value['disposal']
            lifetime_dev = 0
            for code, item in dataset['device'].items():
                try:
                    lifetime_dev = min(lifetime_dev, item['lifetime'])
                except (TypeError, KeyError):
                    lifetime_dev = 10000
            lifetime[key] = lifetime_dev
    return (lifetime, e_manuf, disposal)

def update_maintenance(n_maintenance, e_manuf, disposal):
    key_maintenance = {'n_maintenance': n_maintenance,
                       'e_maintenance': n_maintenance * e_manuf,
                       'd_maintenance': n_maintenance * disposal}
    return key_maintenance

def maintenance_sched(life_units, e_manuf, disposal, maintenance_session):

    life = int(maintenance_session['lifetime'])
    n_devices = maintenance_session['n_devices']
    e_int = maintenance_session['e_intervention']
    print("lifeunits, ", life_units)
    life_units = [int(item) for key, item in life_units.items()]  # list
    up_disposal = {}
    maintenance_session['sensors'] = {}
    maintenance_results = {}
    maintenance_results['sensors'] = {}
    # The algorithm needs to have equal length for e_manuf and disposal so, it adds as many 0(s) to disposal as the length difference
    if len(disposal) < (len(e_manuf) - len(up_disposal)):
        for key, value in e_manuf.items():
            if key not in disposal:
                up_disposal[key] = 0
    for key in disposal:
        up_disposal[key] = disposal[key]

    print('life units: ', life_units)
    print('e manu: ', e_manuf)
    print('e_int: ', e_int)
    print('n devices: ', n_devices)
    print('life: ', life)
    print('disposal: ', up_disposal)

    try:
        m = gp.Model()
        m.ModelSense = GRB.MINIMIZE
        n_unit = len(life_units)

        # Add variables
        x = [[m.addVar(vtype=GRB.BINARY, name="x[%s, %s]" % (i, j))
             for i in range(n_unit)] for j in range(life)]

        e_manuf_t = [[elem for key, elem in e_manuf.items()]
                     for i in range(life)]

        disposal_t = [[elem for key, elem in up_disposal.items()]
                      for i in range(life)]

        w = [m.addVar(vtype=GRB.BINARY, name="w[%s]" % i) for i in range(life)]

        e_int_t = [e_int for i in range(life)]

        # Objective function
        energy_objective = quicksum(quicksum(n_devices * (e_manuf_t[i][j] *
                                             x[i][j]) for j in range(n_unit)) +
                                    (e_int_t[i] * w[i]) for i in range(life))
        disposal_objective = quicksum(quicksum(n_devices * (disposal_t[i][j] *
                                               x[i][j]) for j in range(n_unit))
                                      for i in range(life))

        m.setObjectiveN(energy_objective, 0)
        m.setObjectiveN(disposal_objective, 1)

        # Constraints
        for i in range(n_unit):
            for k in range(life - life_units[i]):
                m.addConstr(quicksum(x[j][i] for j in range(k, k +
                            life_units[i])) >= 1, 'c0')

            for j in range(life):
                m.addConstr(x[j][i] <= w[j], 'c1')

        m.optimize()

        for i in range(n_unit):
            r_times = [j for j in range(life) if x[j][i].x >= 0.99]
            key = list(e_manuf.keys())[i]
            if key == 'battery' or key == 'solar_panel' or key == 'device':
                maintenance_results[key] = update_maintenance(len(r_times),
                                                              e_manuf[key],
                                                              up_disposal[key])
            else:
                maintenance_results['sensors'][key] =\
                    update_maintenance(len(r_times), e_manuf[key],
                                       up_disposal[key])

        maintenance_list = [j + 1 for j in range(life) if w[j].x >= 0.99]
        maintenance_session['n_interventions'] = len(maintenance_list)
        maintenance_session['tot_e_intervention'] = len(maintenance_list) *\
            e_int
        maintenance_results['n_interventions'] = len(maintenance_list)
        maintenance_results['tot_e_intervention'] = len(maintenance_list) *\
            e_int

        m.setParam(GRB.Param.ObjNumber, 0)
        m.setParam(GRB.Param.SolutionNumber, 0)
        maintenance_session['tot_main_energy'] = (m.ObjNVal / n_devices)
        maintenance_results['tot_main_energy'] = (m.ObjNVal / n_devices)

        m.setParam(GRB.Param.ObjNumber, 1)
        m.setParam(GRB.Param.SolutionNumber, 0)
        maintenance_session['tot_main_disposal'] = (m.ObjNVal / n_devices)
        maintenance_results['tot_main_disposal'] = (m.ObjNVal / n_devices)

        return maintenance_results
    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))

    except AttributeError:
        print('Encountered an attribute error')


