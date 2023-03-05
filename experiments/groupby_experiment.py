import os
import vaex
import pandas as pd
import dask.dataframe as dd
import polars as pl

from src.experiment import Experiment
from src.package import Package

ITERATIONS = 1

current_path = os.path.abspath(__file__)
repository_path = os.path.dirname(os.path.dirname(current_path))
data_path = os.path.join(repository_path, 'data')

def _groupby_pandas_function() -> None:
    print("Reading")
    data = pd.read_csv(os.path.join(data_path, "movie_data.csv"))
    for i in range(ITERATIONS):
        data_grouped = data.groupby(by=['genres']).agg({'primaryTitle': 'count'})
        data.sample(frac=1)

def _groupby_dask_function() -> None:
    print("Reading")
    data = dd.read_csv(os.path.join(data_path, "movie_data.csv"))
    for i in range(ITERATIONS):
        data_grouped = data.groupby(by=['genres']).agg({'primaryTitle': 'count'})
        data_grouped.compute()
        data.sample(frac=1)

def _groupby_polars_function() -> None:
    print("Reading")
    data = pl.read_csv(os.path.join(data_path, "movie_data.csv"))
    for i in range(ITERATIONS):
        data_grouped = data.groupby(by=['genres']).agg({'primaryTitle': 'count'})
        data.sample(frac=1)

def _groupby_vaex_function() -> None:
    print("Reading")
    data = vaex.read_csv(os.path.join(data_path, "movie_data.csv"))
    for i in range(ITERATIONS):
        data_grouped = data.groupby(by=['genres']).agg({'primaryTitle': 'count'})
        data.sample(frac=1)
    
def get_experiment() -> Experiment:
    experiment = Experiment('groupby')
    
    if not os.path.exists(os.path.join(data_path, "movie_data.csv")):
        raise Exception("Data available on request by Carbonara or available online (omit reason: including large data files would possibly cost redundant energy when downloading this repository).")
    
    # Add sub experiments
    experiment.add_sub_experiment(Package.PANDAS, _groupby_pandas_function)
    experiment.add_sub_experiment(Package.DASK, _groupby_dask_function)
    experiment.add_sub_experiment(Package.POLARS, _groupby_polars_function)
    experiment.add_sub_experiment(Package.VAEX, _groupby_vaex_function)
    
    return experiment
