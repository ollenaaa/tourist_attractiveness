import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

class TransportInfrastructure:
    def __init__(self) -> None:
        self.transport_infrastructure = ctrl.Consequent(np.arange(0, 18, 1), 'Transport infrastructure')

        self.air_links = ctrl.Antecedent(np.arange(0, 151, 1), 'air links')
        self.airport = ctrl.Antecedent(np.arange(0, 1551, 1), 'airport')
        self.taxi = ctrl.Antecedent(np.arange(0, 501, 1), 'taxi')
        self.transport = ctrl.Antecedent(np.arange(0, 2101, 1), 'transport')

        self.transport_infrastructure['low'] = fuzz.trapmf(self.transport_infrastructure.universe, [0, 0, 4, 8])
        self.transport_infrastructure['medium'] = fuzz.trapmf(self.transport_infrastructure.universe, [4, 8, 10, 14])
        self.transport_infrastructure['high'] = fuzz.trapmf(self.transport_infrastructure.universe, [10, 14, 17, 17])

        self.air_links['low'] = fuzz.trapmf(self.air_links.universe, [0, 0, 25, 50])
        self.air_links['medium'] = fuzz.trapmf(self.air_links.universe, [25, 50, 90, 120])
        self.air_links['high'] = fuzz.trapmf(self.air_links.universe, [100, 145, 150, 150])
   
        self.airport['low'] = fuzz.trapmf(self.airport.universe, [0, 0, 250, 450])
        self.airport['medium'] = fuzz.trapmf(self.airport.universe, [250, 500, 1000, 1250])
        self.airport['high'] = fuzz.trapmf(self.airport.universe, [1000, 1250, 1550, 1550])

        self.taxi['low'] = fuzz.trapmf(self.taxi.universe, [0, 0, 80, 150])
        self.taxi['medium'] = fuzz.trapmf(self.taxi.universe, [50, 150, 210, 300])
        self.taxi['high'] = fuzz.trapmf(self.taxi.universe, [250, 300, 500, 500])

        self.transport['low'] = fuzz.trapmf(self.transport.universe, [0, 0, 100, 300])
        self.transport['medium'] = fuzz.trapmf(self.transport.universe, [100, 350, 550, 800])
        self.transport['high'] = fuzz.trapmf(self.transport.universe, [600, 800, 2100, 2100])

        self.Base_Rules = [
            ctrl.Rule(self.air_links['low'] | self.airport['low'] | self.taxi['low'] | self.transport['low'], self.transport_infrastructure['low']),
            ctrl.Rule(self.air_links['low'] & self.airport['low'] & self.taxi['low'] & self.transport['medium'], self.transport_infrastructure['low']),
            ctrl.Rule(self.air_links['low'] & self.airport['low'] & self.taxi['low'] & self.transport['high'], self.transport_infrastructure['low']),
            ctrl.Rule(self.air_links['low'] & self.airport['low'] & self.taxi['medium'] & self.transport['low'], self.transport_infrastructure['low']),
            ctrl.Rule(self.air_links['low'] & self.airport['low'] & self.taxi['medium'] & self.transport['medium'], self.transport_infrastructure['low']),
            ctrl.Rule(self.air_links['low'] & self.airport['low'] & self.taxi['medium'] & self.transport['high'], self.transport_infrastructure['low']),
            ctrl.Rule(self.air_links['low'] & self.airport['low'] & self.taxi['high'] & self.transport['low'], self.transport_infrastructure['low']),
            ctrl.Rule(self.air_links['low'] & self.airport['low'] & self.taxi['high'] & self.transport['medium'], self.transport_infrastructure['low']),
            ctrl.Rule(self.air_links['low'] & self.airport['low'] & self.taxi['high'] & self.transport['high'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['low'] & self.airport['medium'] & self.taxi['low'] & self.transport['low'], self.transport_infrastructure['low']),
            ctrl.Rule(self.air_links['low'] & self.airport['medium'] & self.taxi['low'] & self.transport['medium'], self.transport_infrastructure['low']),
            ctrl.Rule(self.air_links['low'] & self.airport['medium'] & self.taxi['low'] & self.transport['high'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['low'] & self.airport['medium'] & self.taxi['medium'] & self.transport['low'], self.transport_infrastructure['low']),
            ctrl.Rule(self.air_links['low'] & self.airport['medium'] & self.taxi['medium'] & self.transport['medium'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['low'] & self.airport['medium'] & self.taxi['medium'] & self.transport['high'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['low'] & self.airport['medium'] & self.taxi['high'] & self.transport['low'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['low'] & self.airport['medium'] & self.taxi['high'] & self.transport['medium'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['low'] & self.airport['medium'] & self.taxi['high'] & self.transport['high'], self.transport_infrastructure['high']),
            ctrl.Rule(self.air_links['low'] & self.airport['high'] & self.taxi['low'] & self.transport['low'], self.transport_infrastructure['low']),
            ctrl.Rule(self.air_links['low'] & self.airport['high'] & self.taxi['low'] & self.transport['medium'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['low'] & self.airport['high'] & self.taxi['low'] & self.transport['high'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['low'] & self.airport['high'] & self.taxi['medium'] & self.transport['low'], self.transport_infrastructure['low']),
            ctrl.Rule(self.air_links['low'] & self.airport['high'] & self.taxi['medium'] & self.transport['medium'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['low'] & self.airport['high'] & self.taxi['medium'] & self.transport['high'], self.transport_infrastructure['high']),
            ctrl.Rule(self.air_links['low'] & self.airport['high'] & self.taxi['high'] & self.transport['low'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['low'] & self.airport['high'] & self.taxi['high'] & self.transport['medium'], self.transport_infrastructure['high']),
            ctrl.Rule(self.air_links['low'] & self.airport['high'] & self.taxi['high'] & self.transport['high'], self.transport_infrastructure['high']),

            ctrl.Rule(self.air_links['medium'] & self.airport['low'] & self.taxi['low'] & self.transport['low'], self.transport_infrastructure['low']),
            ctrl.Rule(self.air_links['medium'] & self.airport['low'] & self.taxi['low'] & self.transport['medium'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['medium'] & self.airport['low'] & self.taxi['low'] & self.transport['high'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['medium'] & self.airport['low'] & self.taxi['medium'] & self.transport['low'], self.transport_infrastructure['low']),
            ctrl.Rule(self.air_links['medium'] & self.airport['low'] & self.taxi['medium'] & self.transport['medium'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['medium'] & self.airport['low'] & self.taxi['medium'] & self.transport['high'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['medium'] & self.airport['low'] & self.taxi['high'] & self.transport['low'], self.transport_infrastructure['low']),
            ctrl.Rule(self.air_links['medium'] & self.airport['low'] & self.taxi['high'] & self.transport['medium'], self.transport_infrastructure['low']),
            ctrl.Rule(self.air_links['medium'] & self.airport['low'] & self.taxi['high'] & self.transport['high'], self.transport_infrastructure['high']),
            ctrl.Rule(self.air_links['medium'] & self.airport['medium'] & self.taxi['low'] & self.transport['low'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['medium'] & self.airport['medium'] & self.taxi['low'] & self.transport['medium'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['medium'] & self.airport['medium'] & self.taxi['low'] & self.transport['high'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['medium'] & self.airport['medium'] & self.taxi['medium'] & self.transport['low'], self.transport_infrastructure['low']),
            ctrl.Rule(self.air_links['medium'] | self.airport['medium'] | self.taxi['medium'] | self.transport['medium'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['medium'] & self.airport['medium'] & self.taxi['medium'] & self.transport['high'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['medium'] & self.airport['medium'] & self.taxi['high'] & self.transport['low'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['medium'] & self.airport['medium'] & self.taxi['high'] & self.transport['medium'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['medium'] & self.airport['medium'] & self.taxi['high'] & self.transport['high'], self.transport_infrastructure['high']),
            ctrl.Rule(self.air_links['medium'] & self.airport['high'] & self.taxi['low'] & self.transport['low'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['medium'] & self.airport['high'] & self.taxi['low'] & self.transport['medium'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['medium'] & self.airport['high'] & self.taxi['low'] & self.transport['high'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['medium'] & self.airport['high'] & self.taxi['medium'] & self.transport['low'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['medium'] & self.airport['high'] & self.taxi['medium'] & self.transport['medium'], self.transport_infrastructure['high']),
            ctrl.Rule(self.air_links['medium'] & self.airport['high'] & self.taxi['medium'] & self.transport['high'], self.transport_infrastructure['high']),
            ctrl.Rule(self.air_links['medium'] & self.airport['high'] & self.taxi['high'] & self.transport['low'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['medium'] & self.airport['high'] & self.taxi['high'] & self.transport['medium'], self.transport_infrastructure['high']),
            ctrl.Rule(self.air_links['medium'] & self.airport['high'] & self.taxi['high'] & self.transport['high'], self.transport_infrastructure['medium']),

            ctrl.Rule(self.air_links['high'] & self.airport['low'] & self.taxi['low'] & self.transport['low'], self.transport_infrastructure['low']),
            ctrl.Rule(self.air_links['high'] & self.airport['low'] & self.taxi['low'] & self.transport['medium'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['high'] & self.airport['low'] & self.taxi['low'] & self.transport['high'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['high'] & self.airport['low'] & self.taxi['medium'] & self.transport['low'], self.transport_infrastructure['low']),
            ctrl.Rule(self.air_links['high'] & self.airport['low'] & self.taxi['medium'] & self.transport['medium'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['high'] & self.airport['low'] & self.taxi['medium'] & self.transport['high'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['high'] & self.airport['low'] & self.taxi['high'] & self.transport['low'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['high'] & self.airport['low'] & self.taxi['high'] & self.transport['medium'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['high'] & self.airport['low'] & self.taxi['high'] & self.transport['high'], self.transport_infrastructure['high']),
            ctrl.Rule(self.air_links['high'] & self.airport['medium'] & self.taxi['low'] & self.transport['low'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['high'] & self.airport['medium'] & self.taxi['low'] & self.transport['medium'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['high'] & self.airport['medium'] & self.taxi['low'] & self.transport['high'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['high'] & self.airport['medium'] & self.taxi['medium'] & self.transport['low'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['high'] & self.airport['medium'] & self.taxi['medium'] & self.transport['medium'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['high'] & self.airport['medium'] & self.taxi['medium'] & self.transport['high'], self.transport_infrastructure['high']),
            ctrl.Rule(self.air_links['high'] & self.airport['medium'] & self.taxi['high'] & self.transport['low'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['high'] & self.airport['medium'] & self.taxi['high'] & self.transport['medium'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['high'] & self.airport['medium'] & self.taxi['high'] & self.transport['high'], self.transport_infrastructure['high']),
            ctrl.Rule(self.air_links['high'] & self.airport['high'] & self.taxi['low'] & self.transport['low'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['high'] & self.airport['high'] & self.taxi['low'] & self.transport['medium'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['high'] & self.airport['high'] & self.taxi['low'] & self.transport['high'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['high'] & self.airport['high'] & self.taxi['medium'] & self.transport['low'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['high'] & self.airport['high'] & self.taxi['medium'] & self.transport['medium'], self.transport_infrastructure['high']),
            ctrl.Rule(self.air_links['high'] & self.airport['high'] & self.taxi['medium'] & self.transport['high'], self.transport_infrastructure['high']),
            ctrl.Rule(self.air_links['high'] & self.airport['high'] & self.taxi['high'] & self.transport['low'], self.transport_infrastructure['medium']),
            ctrl.Rule(self.air_links['high'] & self.airport['high'] & self.taxi['high'] & self.transport['medium'], self.transport_infrastructure['high']),
            ctrl.Rule(self.air_links['high'] | self.airport['high'] | self.taxi['high'] | self.transport['high'], self.transport_infrastructure['high'])
        ]

    def fuzzy_inference(self, country : str, num_air_link : int, num_airport : float, num_taxi : float, num_transport : float):
        ctrl_system = ctrl.ControlSystem(self.Base_Rules)
        simulation = ctrl.ControlSystemSimulation(ctrl_system)

        simulation.input['air links'] = num_air_link
        simulation.input['airport'] = num_airport
        simulation.input['taxi'] = num_taxi
        simulation.input['transport'] = num_transport

        simulation.compute()

        output = simulation.output['Transport infrastructure']
        print(f"Assessment of transport infrastructure for {country} = {simulation.output['Transport infrastructure']}")
        self.transport_infrastructure.view(sim=simulation)
        plt.show()

        return self.transport_infrastructure, output

