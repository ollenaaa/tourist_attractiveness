import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

class Attractiveness:
    def __init__(self) -> None:
        self.attrectiveness = ctrl.Consequent(np.arange(0, 11, 1), 'attrectiveness')

        self.transport_infr = ctrl.Antecedent(np.arange(0, 18, 1), 'transport')
        self.tourism_infr = ctrl.Antecedent(np.arange(0, 18, 1), 'tourism')
        self.entertainment_infr = ctrl.Antecedent(np.arange(0, 18, 1), 'entertainment')

        self.attrectiveness['low'] = fuzz.trapmf(self.attrectiveness.universe, [0, 0, 2, 4])
        self.attrectiveness['medium'] = fuzz.trapmf(self.attrectiveness.universe, [2, 4, 6, 8])
        self.attrectiveness['high'] = fuzz.trapmf(self.attrectiveness.universe, [6, 8, 10, 10])

        self.transport_infr['low'] = fuzz.trapmf(self.transport_infr.universe, [0, 0, 4, 8])
        self.transport_infr['medium'] = fuzz.trapmf(self.transport_infr.universe, [4, 8, 10, 14])
        self.transport_infr['high'] = fuzz.trapmf(self.transport_infr.universe, [10, 14, 17, 17])

        self.tourism_infr['low'] = fuzz.trapmf(self.tourism_infr.universe, [0, 0, 4, 8])
        self.tourism_infr['medium'] = fuzz.trapmf(self.tourism_infr.universe, [4, 8, 10, 14])
        self.tourism_infr['high'] = fuzz.trapmf(self.tourism_infr.universe, [10, 14, 17, 17])

        self.entertainment_infr['low'] = fuzz.trapmf(self.entertainment_infr.universe, [0, 0, 4, 8])
        self.entertainment_infr['medium'] = fuzz.trapmf(self.entertainment_infr.universe, [4, 8, 10, 14])
        self.entertainment_infr['high'] = fuzz.trapmf(self.entertainment_infr.universe, [10, 14, 17, 17])

        self.Base_Rules = [
            ctrl.Rule(self.transport_infr['low'] & self.tourism_infr['low'] & self.entertainment_infr['low'], self.attrectiveness['low']),
            ctrl.Rule(self.transport_infr['low'] & self.tourism_infr['low'] & self.entertainment_infr['medium'], self.attrectiveness['low']),
            ctrl.Rule(self.transport_infr['low'] & self.tourism_infr['low'] & self.entertainment_infr['high'], self.attrectiveness['medium']),
            ctrl.Rule(self.transport_infr['low'] & self.tourism_infr['medium'] & self.entertainment_infr['low'], self.attrectiveness['low']),
            ctrl.Rule(self.transport_infr['low'] & self.tourism_infr['medium'] & self.entertainment_infr['medium'], self.attrectiveness['medium']),
            ctrl.Rule(self.transport_infr['low'] & self.tourism_infr['medium'] & self.entertainment_infr['high'], self.attrectiveness['medium']),
            ctrl.Rule(self.transport_infr['low'] & self.tourism_infr['high'] & self.entertainment_infr['low'], self.attrectiveness['low']),
            ctrl.Rule(self.transport_infr['low'] & self.tourism_infr['high'] & self.entertainment_infr['medium'], self.attrectiveness['medium']),
            ctrl.Rule(self.transport_infr['low'] & self.tourism_infr['high'] & self.entertainment_infr['high'], self.attrectiveness['medium']),

            ctrl.Rule(self.transport_infr['medium'] & self.tourism_infr['low'] & self.entertainment_infr['low'], self.attrectiveness['low']),
            ctrl.Rule(self.transport_infr['medium'] & self.tourism_infr['low'] & self.entertainment_infr['medium'], self.attrectiveness['medium']),
            ctrl.Rule(self.transport_infr['medium'] & self.tourism_infr['low'] & self.entertainment_infr['high'], self.attrectiveness['medium']),
            ctrl.Rule(self.transport_infr['medium'] & self.tourism_infr['medium'] & self.entertainment_infr['low'], self.attrectiveness['medium']),
            ctrl.Rule(self.transport_infr['medium'] & self.tourism_infr['medium'] & self.entertainment_infr['medium'], self.attrectiveness['medium']),
            ctrl.Rule(self.transport_infr['medium'] & self.tourism_infr['medium'] & self.entertainment_infr['high'], self.attrectiveness['medium']),
            ctrl.Rule(self.transport_infr['medium'] & self.tourism_infr['high'] & self.entertainment_infr['low'], self.attrectiveness['medium']),
            ctrl.Rule(self.transport_infr['medium'] & self.tourism_infr['high'] & self.entertainment_infr['medium'], self.attrectiveness['high']),
            ctrl.Rule(self.transport_infr['medium'] & self.tourism_infr['high'] & self.entertainment_infr['high'], self.attrectiveness['high']),

            ctrl.Rule(self.transport_infr['high'] & self.tourism_infr['low'] & self.entertainment_infr['low'], self.attrectiveness['medium']),
            ctrl.Rule(self.transport_infr['high'] & self.tourism_infr['low'] & self.entertainment_infr['medium'], self.attrectiveness['medium']),
            ctrl.Rule(self.transport_infr['high'] & self.tourism_infr['low'] & self.entertainment_infr['high'], self.attrectiveness['medium']),
            ctrl.Rule(self.transport_infr['high'] & self.tourism_infr['medium'] & self.entertainment_infr['low'], self.attrectiveness['medium']),
            ctrl.Rule(self.transport_infr['high'] & self.tourism_infr['medium'] & self.entertainment_infr['medium'], self.attrectiveness['high']),
            ctrl.Rule(self.transport_infr['high'] & self.tourism_infr['medium'] & self.entertainment_infr['high'], self.attrectiveness['high']),
            ctrl.Rule(self.transport_infr['high'] & self.tourism_infr['high'] & self.entertainment_infr['low'], self.attrectiveness['high']),
            ctrl.Rule(self.transport_infr['high'] & self.tourism_infr['high'] & self.entertainment_infr['medium'], self.attrectiveness['high']),
            ctrl.Rule(self.transport_infr['high'] & self.tourism_infr['high'] & self.entertainment_infr['high'], self.attrectiveness['high'])
        ]

    def defuzzifier(self, num_transport, num_tourism, num_entertainment):
        ctrl_system = ctrl.ControlSystem(self.Base_Rules)
        simulation = ctrl.ControlSystemSimulation(ctrl_system)

        simulation.input['tourism'] = num_tourism[1]
        simulation.input['transport'] = num_transport[1]
        simulation.input['entertainment'] = num_entertainment[1]

        simulation.compute()

        output = simulation.output['attrectiveness']
        # print(f"Output = {output}")

        self.attrectiveness.view(sim=simulation)
        plt.show()
