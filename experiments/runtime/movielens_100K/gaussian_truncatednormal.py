'''
Measure runtime on the MovieLens 100K dataset, with the Gaussian +
Truncated Normal model.
'''

import sys, os
project_location = os.path.dirname(__file__)+"/../../../../"
sys.path.append(project_location)

from BMF_Priors.code.models.bmf_gaussian_truncatednormal import BMF_Gaussian_TruncatedNormal
from BMF_Priors.data.movielens.load_data import load_movielens_100K
from BMF_Priors.experiments.runtime.runtime_experiment import measure_runtime


''' Run the experiment. '''
R, M = load_movielens_100K()
model_class = BMF_Gaussian_TruncatedNormal
values_K = [5, 10, 20, 50]
settings = {
    'R': R, 
    'M': M, 
    'hyperparameters': { 'alpha':1., 'beta':1., 'muUV':0., 'tauUV':0.1 }, 
    'init': 'random', 
    'iterations': 10,
}
fout = './results/times_gaussian_truncatednormal.txt'

times_per_iteration = measure_runtime(values_K, model_class, settings, fout)
print zip(values_K, times_per_iteration)