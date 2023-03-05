import csv
import os
import pprint

class Readinator():
    def __init__(self, data_path: str) -> None:
        current_path = os.path.abspath(__file__)
        src_path = os.path.dirname(current_path)
        repository_path = os.path.dirname(src_path)
        result_path = os.path.join(repository_path, 'results')
        self.data_path = os.path.join(result_path, data_path)

        self.data_dict = {}

    def reader(self) -> None:
        with open(self.data_path) as f:
            data = list(csv.DictReader(f))

        for item in data:
            if item['experiment'] not in self.data_dict:
                self.data_dict[item['experiment']] = {}
            
            experiment_dict = self.data_dict[item['experiment']]
            if item['package'] not in experiment_dict:
                experiment_dict[item['package']] = []
            experiment_dict[item['package']].append(item['energy'])

    def display_data(self) -> None:
        pprint.pprint(self.data_dict)
