import os
import vaex
import pandas as pd
import dask.dataframe as dd
import polars as pl

from src.experiment import Experiment
from src.package import Package

current_path = os.path.abspath(__file__)
repository_path = os.path.dirname(os.path.dirname(current_path))
temp_path = os.path.join(repository_path, 'temp')
data_path = os.path.join(repository_path, 'data')

# Check if temp folder exists, create it if not
if not os.path.exists(temp_path):
    os.makedirs(temp_path)

def _read_write_pandas_function() -> None:
    print("Reading")
    data = pd.read_csv(os.path.join(data_path, "movie_data.csv"))
    print("Writing")
    data.to_csv(os.path.join(temp_path, "pandas_read_write_experiment.csv"))

def _read_write_dask_function() -> None:
    print("Reading")
    data = dd.read_csv(os.path.join(data_path, "movie_data.csv"), dtype={'runtimeMinutes': 'object'})
    print("Writing")
    data.to_csv(os.path.join(temp_path, "dask_read_write_experiment.csv"))

def _read_write_polars_function() -> None:
    print("Reading")
    data = pl.read_csv("data/movie_data.csv")
    print("Writing")
    data.write_csv(os.path.join(temp_path, "polars_read_write_experiment.csv"))

def _read_write_vaex_function() -> None:
    print("Reading")
    data = vaex.read_csv(os.path.join(data_path, "movie_data.csv"))
    print("Writing")
    data.export_csv(os.path.join(temp_path, "vaex_read_write_experiment.csv"))
    
def get_experiment() -> Experiment:
    experiment = Experiment('read_write')
    
    if not os.path.exists(os.path.join(data_path, "movie_data.csv")):
        raise Exception("Data available on request by Carbonara or available online (omit reason: including large data files would possibly cost redundant energy when downloading this repository).")
    
    # Add sub experiments
    experiment.add_sub_experiment(Package.PANDAS, _read_write_pandas_function)
    experiment.add_sub_experiment(Package.DASK, _read_write_dask_function)
    experiment.add_sub_experiment(Package.POLARS, _read_write_polars_function)
    experiment.add_sub_experiment(Package.VAEX, _read_write_vaex_function)
    
    return experiment
