import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

class TourismInfrastructure:
    def __init__(self) -> None:
        self.tourism_infastructure = ctrl.Consequent(np.arange(0, 18, 1), 'Tourism infastructure')

        self.hotels = ctrl.Antecedent(np.arange(0, 300001, 1), 'hotels')
        self.hotels_links = ctrl.Antecedent(np.arange(0, 3501, 1), "hotels links")

        self.hotels['low'] = fuzz.trapmf(self.hotels.universe, [0, 0, 9500, 15000])
        self.hotels['medium'] = fuzz.trapmf(self.hotels.universe, [5000, 15000, 20000, 30000])
        self.hotels['high'] = fuzz.trapmf(self.hotels.universe, [20000, 30000, 300000, 300000])

        self.hotels_links['low'] = fuzz.trapmf(self.hotels_links.universe, [0, 0, 600, 900])
        self.hotels_links['medium'] = fuzz.trapmf(self.hotels_links.universe, [550, 1000, 1800, 2250])
        self.hotels_links['high'] = fuzz.trapmf(self.hotels_links.universe, [1800, 2250, 3500, 3500])

        self.tourism_infastructure['low'] = fuzz.trapmf(self.tourism_infastructure.universe, [0, 0, 4, 8])
        self.tourism_infastructure['medium'] = fuzz.trapmf(self.tourism_infastructure.universe, [4, 8, 10, 14])
        self.tourism_infastructure['high'] = fuzz.trapmf(self.tourism_infastructure.universe, [10, 14, 17, 17])

        self.Base_Rules = [
            ctrl.Rule(self.hotels['low'] | self.hotels_links['low'], self.tourism_infastructure['low']),
            ctrl.Rule(self.hotels['low'] & self.hotels_links['medium'], self.tourism_infastructure['medium']),
            ctrl.Rule(self.hotels['low'] & self.hotels_links['high'], self.tourism_infastructure['medium']),

            ctrl.Rule(self.hotels['medium'] & self.hotels_links['low'], self.tourism_infastructure['medium']),
            ctrl.Rule(self.hotels['medium'] | self.hotels_links['medium'], self.tourism_infastructure['medium']),
            ctrl.Rule(self.hotels['medium'] & self.hotels_links['high'], self.tourism_infastructure['medium']),

            ctrl.Rule(self.hotels['high'] & self.hotels_links['low'], self.tourism_infastructure['medium']),
            ctrl.Rule(self.hotels['high'] & self.hotels_links['medium'], self.tourism_infastructure['medium']),
            ctrl.Rule(self.hotels['high'] | self.hotels_links['high'], self.tourism_infastructure['high'])
        ]

    def fuzzy_inference(self, country : str, num_hotels : int, num_hotels_links : float):
        ctrl_system = ctrl.ControlSystem(self.Base_Rules)
        simulation = ctrl.ControlSystemSimulation(ctrl_system)

        simulation.input['hotels'] = num_hotels
        simulation.input['hotels links'] = num_hotels_links

        simulation.compute()

        output = simulation.output['Tourism infastructure']
        print(f"Assessment of tourism infrastructure for {country} = {simulation.output['Tourism infastructure']}")
        self.tourism_infastructure.view(sim=simulation)
        plt.show()
        return self.tourism_infastructure, output