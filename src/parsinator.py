import csv
import datetime
import os
import numpy as np

class Parsinator():
    def __init__(self, experiment_log_path: str, powerlogz_log_path: str) -> None:
        current_path = os.path.abspath(__file__)
        src_path = os.path.dirname(current_path)
        repository_path = os.path.dirname(src_path)
        output_path = os.path.join(repository_path, 'output')
        powerlogz_path = os.path.join(repository_path, 'powerlogz')
        result_path = os.path.join(repository_path, 'results')

        self.experiment_log_path = os.path.join(output_path, experiment_log_path)
        self.powerlogz_log_path = os.path.join(powerlogz_path, powerlogz_log_path)

        now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
        self.writer_path = os.path.join(result_path, 'results-' + now + '.csv')
        
        self.experiment_list = []
        self.powerlogz_list = []
    
    def loadinator(self):
        with open(self.experiment_log_path, 'r') as file:
            experiment_reader = csv.DictReader(file)
            self.experiment_list = list(experiment_reader)
        
        with open(self.powerlogz_log_path, 'r') as file:
            powerlogz_reader = csv.DictReader(file)
            self.powerlogz_list = list(powerlogz_reader)     
    
    def parsinator(self):
        energies = []
        results = {}

        print('\n>>> Parsed data:')
        
        # Check if results folder exists, create it if not
        if not os.path.exists(os.path.dirname(self.writer_path)):
            os.makedirs(os.path.dirname(self.writer_path))
        
        with open(self.writer_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['experiment', 'package', 'energy'])

        for i in range(0, len(self.experiment_list), 2):
            start = self.experiment_list[i]
            stop = self.experiment_list[i+1]

            energy_consumption_list = []
            for powerlogz in self.powerlogz_list:
                if powerlogz['System Time'] >= start['time'] and powerlogz['System Time'] <= stop['time']:
                    energy_consumption_list.append((float(powerlogz['Processor Power_0(Watt)'].strip()), float(powerlogz['Elapsed Time (sec)'].strip())))
                if powerlogz['System Time'] > stop['time']:
                    break
            
            if len(energy_consumption_list) == 0:
                print('No energy consumption data for experiment:', start['experiment'], 'with package:', start['package'])
                continue
            
            power_data, timestamps = zip(*energy_consumption_list)
            energy = np.trapz(power_data, timestamps)
            
            # time,experiment,package,event
            energies.append(energy)

            print('Energy consumption:', str(energy) + 'J', 'for experiment:', start['experiment'], 'with package:', start['package'])

            with open(self.writer_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([start['experiment'], start['package'], energy])

        print('Total energy:', sum(energies))
    
    def run(self):
        self.loadinator()
        self.parsinator()
