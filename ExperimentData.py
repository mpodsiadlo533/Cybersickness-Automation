'''
Plik pomocniczy do GUI
'''

import pandas as pd

class ExperimentData:
    '''
    Class which manage csv file cases
    '''

    def __init__(self, filepath):
        self.data = pd.read_csv(filepath, sep =';')
        self.current_index = 0

    def get_next_experiment(self):
        experiment = self.data.iloc[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.data)
        return experiment

    def get_previous_experiment(self):
        self.current_index = (self.current_index - 1) % len(self.data)
        return self.data.iloc[self.current_index]