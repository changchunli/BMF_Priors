'''
Measure sparsity experiment on the MovieLens 100K dataset, with 
the Gaussian + Gaussian + Volume Prior (nonnegative) model.
'''

import sys, os
project_location = os.path.dirname(__file__)+"/../../../../"
sys.path.append(project_location)

from BMF_Priors.code.models.bmf_gaussian_gaussian_volumeprior_nonnegative import BMF_Gaussian_Gaussian_VolumePrior_nonnegative
from BMF_Priors.data.movielens.load_data import load_movielens_100K
from BMF_Priors.experiments.sparsity.sparsity_experiment import sparsity_experiment

import matplotlib.pyplot as plt


''' Run the experiment. '''
R, M = load_movielens_100K()
model_class = BMF_Gaussian_Gaussian_VolumePrior_nonnegative
n_repeats = 20
stratify_rows = False
fractions_known = [0.07, 0.06, 0.05, 0.04, 0.03, 0.02]
fractions_unknown = [1. - v for v in fractions_known]
settings = {
    'R': R, 
    'M': M, 
    'K': 5,
    'hyperparameters': { 'alpha':1., 'beta':1., 'lamb':0.1, 'gamma':10**0 }, 
    'init': 'random', 
    'iterations': 150,
    'burn_in': 100,
    'thinning': 1,
}
fout = './results/performances_gaussian_gaussian_volumeprior_nonnegative.txt'
average_performances, all_performances = sparsity_experiment(
    n_repeats=n_repeats, fractions_unknown=fractions_unknown, stratify_rows=stratify_rows,
    model_class=model_class, settings=settings, fout=fout)


''' Plot the performance. '''
plt.figure()
plt.title("Sparsity performances")
plt.plot(fractions_unknown, average_performances['MSE'])
plt.ylim(0,4)