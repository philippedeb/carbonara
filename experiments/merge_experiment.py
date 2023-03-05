# This is an example file

import os
import time
import vaex
import pandas as pd
import dask.dataframe as dd
import polars as pl

from src.experiment import Experiment
from src.package import Package

current_path = os.path.abspath(__file__)
repository_path = os.path.dirname(os.path.dirname(current_path))
data_path = os.path.join(repository_path, 'data')

def _merge_pandas_function() -> None:
    print("Reading")
    data = pd.read_csv(os.path.join(data_path, "movie_data.csv"))
    df1 = data[['tconst', 'titleType', 'primaryTitle', 'originalTitle']]
    df2 = data[['tconst', 'startYear' , 'endYear', 'runtimeMinutes', 'genres']]
    for i in range(5):
        print("Shuffle")
        df1.sample(frac=1)
        print("Merging")
        res_data = pd.merge(df1, df2, on='tconst')

def _merge_dask_function() -> None:
    print("Reading")
    data = dd.read_csv(os.path.join(data_path, "movie_data.csv"))
    df1 = data[['tconst', 'titleType', 'primaryTitle', 'originalTitle']]
    df2 = data[['tconst', 'startYear' , 'endYear', 'runtimeMinutes', 'genres']]
    for i in range(5):
        print("Shuffle")
        df1.sample(frac=1)
        print("Merging")
        res_data = dd.merge(df1, df2, on='tconst')

def _merge_polars_function() -> None:
    print("Reading")
    data = pl.read_csv(os.path.join(data_path, "movie_data.csv"))
    df1 = data[['tconst', 'titleType', 'primaryTitle', 'originalTitle']]
    df2 = data[['tconst', 'startYear' , 'endYear', 'runtimeMinutes', 'genres']]
    for i in range(5):
        print("Shuffle")
        df1.sample(frac=1)
        print("Merging")
        res_data = df1.join(df2, on='tconst', how='inner')

def _merge_vaex_function() -> None:
    print("Reading")
    data = vaex.read_csv(os.path.join(data_path, "movie_data.csv"))
    df1 = data[['tconst', 'titleType', 'primaryTitle', 'originalTitle']]
    df2 = data[['tconst', 'startYear' , 'endYear', 'runtimeMinutes', 'genres']]
    for i in range(5):
        print("Shuffle")
        df1.sample(frac=1)
        print("Merging")
        res_data = df1.join(df2, on='tconst', how='inner')

def get_experiment() -> Experiment:
    experiment = Experiment('merge')
    
    if not os.path.exists(os.path.join(data_path, "movie_data.csv")):
        raise Exception("Data available on request by Carbonara or available online (omit reason: including large data files would possibly cost redundant energy when downloading this repository).")
    
    # Add sub experiments
    experiment.add_sub_experiment(Package.PANDAS, _merge_pandas_function)
    experiment.add_sub_experiment(Package.DASK, _merge_dask_function)
    experiment.add_sub_experiment(Package.POLARS, _merge_polars_function)
    experiment.add_sub_experiment(Package.VAEX, _merge_vaex_function)
    
    return experiment
