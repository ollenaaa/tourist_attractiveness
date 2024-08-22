import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

class EntertainmentInfrastructure:
    def __init__(self) -> None:
        self.entertainment_infastructure = ctrl.Consequent(np.arange(0, 18, 1), 'Entertainment infastructure')

        self.impressions = ctrl.Antecedent(np.arange(0, 1100001, 1), "impressions")
        self.attractions = ctrl.Antecedent(np.arange(0, 4001, 1), 'attractions')
        self.attractions_links = ctrl.Antecedent(np.arange(0, 951, 1), "attractions_links")

        self.entertainment_infastructure['low'] = fuzz.trapmf(self.entertainment_infastructure.universe, [0, 0, 4, 8])
        self.entertainment_infastructure['medium'] = fuzz.trapmf(self.entertainment_infastructure.universe, [4, 8, 10, 14])
        self.entertainment_infastructure['high'] = fuzz.trapmf(self.entertainment_infastructure.universe, [10, 14, 17, 17])

        self.impressions['low'] = fuzz.trimf(self.impressions.universe, [0, 0, 150])
        self.impressions['medium'] = fuzz.trapmf(self.impressions.universe, [100, 300, 400, 600])
        self.impressions['high'] = fuzz.trapmf(self.impressions.universe, [400, 600, 1100, 1100])

        self.attractions['low'] = fuzz.trimf(self.attractions.universe, [0, 0, 300])
        self.attractions['medium'] = fuzz.trapmf(self.attractions.universe, [200, 400, 600, 800])
        self.attractions['high'] = fuzz.trapmf(self.attractions.universe, [600, 800, 4000, 4000])

        self.attractions_links['low'] = fuzz.trimf(self.attractions_links.universe, [0, 0, 150])
        self.attractions_links['medium'] = fuzz.trapmf(self.attractions_links.universe, [100, 200, 300, 400])
        self.attractions_links['high'] = fuzz.trapmf(self.attractions_links.universe, [300, 400, 950, 950])

        self.Base_Rules = [
            ctrl.Rule(self.impressions['low'] | self.attractions['low'] | self.attractions_links['low'], self.entertainment_infastructure['low']),
            ctrl.Rule(self.impressions['low'] & self.attractions['low'] & self.attractions_links['medium'], self.entertainment_infastructure['low']),
            ctrl.Rule(self.impressions['low'] & self.attractions['low'] & self.attractions_links['high'], self.entertainment_infastructure['low']),
            ctrl.Rule(self.impressions['low'] & self.attractions['medium'] & self.attractions_links['low'], self.entertainment_infastructure['medium']),
            ctrl.Rule(self.impressions['low'] & self.attractions['medium'] & self.attractions_links['medium'], self.entertainment_infastructure['medium']),
            ctrl.Rule(self.impressions['low'] & self.attractions['medium'] & self.attractions_links['high'], self.entertainment_infastructure['medium']),
            ctrl.Rule(self.impressions['low'] & self.attractions['high'] & self.attractions_links['low'], self.entertainment_infastructure['high']),
            ctrl.Rule(self.impressions['low'] & self.attractions['high'] & self.attractions_links['medium'], self.entertainment_infastructure['medium']),
            ctrl.Rule(self.impressions['low'] & self.attractions['high'] & self.attractions_links['high'], self.entertainment_infastructure['high']),

            ctrl.Rule(self.impressions['medium'] & self.attractions['low'] & self.attractions_links['low'], self.entertainment_infastructure['medium']),
            ctrl.Rule(self.impressions['medium'] & self.attractions['low'] & self.attractions_links['medium'], self.entertainment_infastructure['medium']),
            ctrl.Rule(self.impressions['medium'] & self.attractions['low'] & self.attractions_links['high'], self.entertainment_infastructure['medium']),
            ctrl.Rule(self.impressions['medium'] & self.attractions['medium'] & self.attractions_links['low'], self.entertainment_infastructure['medium']),
            ctrl.Rule(self.impressions['medium'] | self.attractions['medium'] | self.attractions_links['medium'], self.entertainment_infastructure['medium']),
            ctrl.Rule(self.impressions['medium'] & self.attractions['medium'] & self.attractions_links['high'], self.entertainment_infastructure['high']),
            ctrl.Rule(self.impressions['medium'] & self.attractions['high'] & self.attractions_links['low'], self.entertainment_infastructure['medium']),
            ctrl.Rule(self.impressions['medium'] & self.attractions['high'] & self.attractions_links['medium'], self.entertainment_infastructure['medium']),
            ctrl.Rule(self.impressions['medium'] & self.attractions['high'] & self.attractions_links['high'], self.entertainment_infastructure['high']),

            ctrl.Rule(self.impressions['high'] & self.attractions['low'] & self.attractions_links['low'], self.entertainment_infastructure['medium']),
            ctrl.Rule(self.impressions['high'] & self.attractions['low'] & self.attractions_links['medium'], self.entertainment_infastructure['medium']),
            ctrl.Rule(self.impressions['high'] & self.attractions['low'] & self.attractions_links['high'], self.entertainment_infastructure['high']),
            ctrl.Rule(self.impressions['high'] & self.attractions['medium'] & self.attractions_links['low'], self.entertainment_infastructure['medium']),
            ctrl.Rule(self.impressions['high'] & self.attractions['medium'] & self.attractions_links['medium'], self.entertainment_infastructure['high']),
            ctrl.Rule(self.impressions['high'] & self.attractions['medium'] & self.attractions_links['high'], self.entertainment_infastructure['medium']),
            ctrl.Rule(self.impressions['high'] & self.attractions['high'] & self.attractions_links['low'], self.entertainment_infastructure['high']),
            ctrl.Rule(self.impressions['high'] & self.attractions['high'] & self.attractions_links['medium'], self.entertainment_infastructure['high']),
            ctrl.Rule(self.impressions['high'] | self.attractions['high'] | self.attractions_links['high'], self.entertainment_infastructure['high']),
        ]

    def fuzzy_inference(self, country : str, num_impressions : float, num_attractions : float, num_attractions_links : float):
        ctrl_system = ctrl.ControlSystem(self.Base_Rules)
        simulation = ctrl.ControlSystemSimulation(ctrl_system)

        simulation.input['impressions'] = num_impressions
        simulation.input['attractions'] = num_attractions
        simulation.input['attractions_links'] = num_attractions_links

        simulation.compute()

        output = simulation.output['Entertainment infastructure']
        print(f"Assessment of entertainment infrastructure for {country} = {simulation.output['Entertainment infastructure']}")
        self.entertainment_infastructure.view(sim=simulation)
        plt.show()

        return self.entertainment_infastructure, output