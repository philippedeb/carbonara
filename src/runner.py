from ast import List
from concurrent.futures import ProcessPoolExecutor
import csv
import datetime
import math
import os
import random
import time
from typing import Callable, List, Optional, Tuple

from src.experiment import Experiment
from src.package import Package
from src.system_info import print_system_details

WARM_UP_TIME_MINUTES = 5
TAIL_ENERGY_TIME_MINUTES = 1

class Runner:
    """
    Can be used to run experiments using a systematic approach for measuring energy consumption.
    Required: Intel Power Gadget 3.6
    """

    def __init__(self, experiments = []):
        self.experiments = experiments
        self.writer_name = "placeholder.csv"


    def add_experiment(self, experiment: Experiment) -> None:
        """
        Adds an experiment to the runner.

        Args:
            experiment (Experiment): The experiment to add.
        """
        self.experiments.append(experiment)


    def run(self, n: int = 1, warm_up_time: Optional[int] = None, tail_energy_time: Optional[int] = None) -> None:
        """
        Runs all experiments n times and writes the results to a CSV file in /output.

        Args:
            n (int, optional): Number of repeats. Defaults to 1.
            warm_up_time (int, optional): Time for machine to warmup (in seconds). Defaults to WARM_UP_TIME_MINUTES (* 60).
            warm_up_time (int, optional): Time for machine to wait for tail energy (in seconds). Defaults to TAIL_ENERGY_TIME_MINUTES (* 60).
        """
        assert len(self.experiments) > 0, 'No experiments added to runner!'
        
        print_system_details()
        
        print("""
              
             _____            _                                 
            /  __ \          | |                                
            | /  \/ __ _ _ __| |__   ___  _ __   __ _ _ __ __ _ 
            | |    / _` | '__| '_ \ / _ \| '_ \ / _` | '__/ _` |
            | \__/\ (_| | |  | |_) | (_) | | | | (_| | | | (_| |
             \____/\__,_|_|  |_.__/ \___/|_| |_|\__,_|_|  \__,_|
                                                                
            Version 🍝: 1.0.0                                                    

            """)
        
        # Request manual action from user
        self.__wait_for_user_input('\n>>> Make sure to START logging now (using Intel Power Gadget 3.6)')
        
        # Warm up machine
        self.__warm_up_machine(WARM_UP_TIME_MINUTES * 60 if warm_up_time is None else warm_up_time)
        
        # Setup environment for CSV writer
        self.__setup_csv_writer()
        
        # Create a batch of experiments to run
        sub_experiments = self.__repeat_and_shuffle_experiments(n)
        
        # Run the batch of experiments
        for sub_experiment in sub_experiments:
            experiment_name, package, function = sub_experiment
            
            # Wait for tail energy from previous tasks
            self.__reduce_tail_energy(TAIL_ENERGY_TIME_MINUTES * 60 if tail_energy_time is None else tail_energy_time)
            
            # Run experiment
            print('\nStarted running experiment \'%s\' with package \'%s\'' % (experiment_name, package.value))
            self.__start(experiment_name, package.value)
            function()
            self.__stop(experiment_name, package.value)
            print('Finished running experiment \'%s\' with package \'%s\'' % (experiment_name, package.value))
        
        # Let the user know that the experiments finished running and manual action is required
        self.__wait_for_user_input('The experiments finished running! Please STOP logging to save the results.')


    def __setup_csv_writer(self) -> None:
        """
        Sets up the environment for a CSV writer for the experiments.
        """
        
        # Get the path to the output folder to write the CSV file to
        current_path = os.path.abspath(__file__)
        src_path = os.path.dirname(current_path)
        repository_path = os.path.dirname(src_path)
        output_path = os.path.join(repository_path, 'output')
        
        # Check if output folder exists, create it if not
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # Create a file name based on time such that it is unique
        now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
        self.writer_name = os.path.join(output_path, 'run-' + now + '.csv')
        
        # Set headers
        with open(self.writer_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['time', 'experiment', 'package', 'event'])


    def __repeat_and_shuffle_experiments(self, n: int) -> List[Tuple[Package, Callable[..., None]]]:
        sub_experiments = []
        
        # Add sub experiments n times
        for experiment in self.experiments:
            for subexperiment in experiment._sub_experiments:
                for _ in range(n):
                    package, function = subexperiment
                    sub_experiments.append((experiment.name, package, function))
        
        # Shuffle experiments
        random.shuffle(sub_experiments)
        
        return sub_experiments


    def __start(self, experiment_name: str, package: Package) -> None:
        """
        Starts the experiment and writes metadata to CSV.

        Args:
            experiment_name (str): name of the experiment.
            package (Package): package used for the experiment.
        """
        t = datetime.datetime.now().strftime("%H:%M:%S.%f")
        print("Start: ", t)
        print("---------------------------------")
        with open(self.writer_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([t, experiment_name, package, 'START'])


    def __stop(self, experiment_name: str, package: Package) -> None:
        """
        Stops the experiment and writes metadata to CSV.

        Args:
            experiment_name (str): name of the experiment.
            package (Package): package used for the experiment.
        """
        t = datetime.datetime.now().strftime("%H:%M:%S.%f")
        print("---------------------------------")
        print("Stop: ", t)
        with open(self.writer_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([t, experiment_name, package, 'END'])


    def __warm_up_machine(self, seconds: int) -> None:
        """
        Warms up the machine by running a CPU intensive task for a given amount of seconds.

        Args:
            seconds (int): The amount of seconds to run the task for.
        """
        print("\nWarming up machine for %d seconds..." % seconds)
        start = time.time()
        
        while True:
            # Perform some CPU intensive operation
            math.factorial(100000)
            if time.time() - start >= seconds:
                break
        
        print("Warming up machine finished.")


    def __wait_for_user_input(self, message: str) -> None:
        """
        Waits for user input.

        Args:
            message (str): The message to display to the user.
        """
        input(message + '\nPress enter to continue...')


    def __reduce_tail_energy(self, seconds: int = 60, minutes: int = 0) -> None:
        """
        Waits for tail energy consumption of the machine to be reduced by waiting for a given amount of seconds.

        Args:
            seconds (int): The amount of seconds to wait for. Defaults to 0.
            minutes (int): The amount of minutes to wait for. Defaults to 0.
        """
        while (seconds >= 60):
            minutes += 1
            seconds -= 60
        print("\nWaiting for tail energy consumption to be reduced by %d minutes and %d seconds..." % (minutes, seconds))
        time.sleep(minutes * 60 + seconds)
        print("Tail energy consumption reduced.")
