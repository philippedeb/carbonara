import experiments.groupby_experiment as experiment_1
import experiments.read_write_experiment as experiment_2
import experiments.merge_experiment as experiment_3
from src.runner import Runner

r = Runner()

r.add_experiment(experiment_1.get_experiment())
r.add_experiment(experiment_2.get_experiment())
r.add_experiment(experiment_3.get_experiment())

# For valid results, run the experiment for at least 30 times (n=30), to get a proper sample set, and check for a normal distribution.
r.run(n=5, warm_up_time=5*60, tail_energy_time=30)
