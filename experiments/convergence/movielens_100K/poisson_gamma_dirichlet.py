'''
Measure convergence on the MovieLens 100K dataset, with the Poisson +
Dirichlet + Gamma model.
'''

import sys, os
project_location = os.path.dirname(__file__)+"/../../../../"
sys.path.append(project_location)

from BMF_Priors.code.models.bmf_poisson_gamma_dirichlet import BMF_Poisson_Gamma_Dirichlet
from BMF_Priors.data.movielens.load_data import load_movielens_100K
from BMF_Priors.experiments.convergence.convergence_experiment import measure_convergence_time

import matplotlib.pyplot as plt


''' Run the experiment. '''
R, M = load_movielens_100K()
model_class = BMF_Poisson_Gamma_Dirichlet
settings = {
    'R': R, 
    'M': M, 
    'K': 20, 
    'hyperparameters': { 'alpha':1., 'a':1., 'b':1. }, 
    'init': 'random', 
    'iterations': 200,
}
fout_performances = './results/performances_poisson_gamma_dirichlet.txt'
fout_times = './results/times_poisson_gamma_dirichlet.txt'
repeats = 10
performances, times = measure_convergence_time(
    repeats, model_class, settings, fout_performances, fout_times)


''' Plot the times, and performance vs iterations. '''
plt.figure()
plt.title("Performance against average time")
plt.plot(times, performances)
plt.ylim(0,2000)

plt.figure()
plt.title("Performance against iteration")
plt.plot(performances)
plt.ylim(0,2000)
