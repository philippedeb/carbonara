import csv
import os
import time
from typing import Callable, List, Tuple
import src.package as Package
 
class Experiment:
    def __init__(self, name: str):
        self.name = name
        self._sub_experiments: List[Tuple[Package.Package, Callable[..., None]]] = []
    
    def add_sub_experiment(self, package: Package.Package, function: Callable[..., None]) -> None:
        """
        Adds a sub experiment for a certain Package to the experiment.

        Args:
            package (Package.Package): package used by function
            function (Callable[..., None]): experiment function
        """
        self._sub_experiments.append((package, function))
