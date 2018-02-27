'''
Measure convergence on the MovieLens 100K dataset, with the Gaussian + 
Gaussian + Volume Prior model.
'''

import sys, os
project_location = os.path.dirname(__file__)+"/../../../../"
sys.path.append(project_location)

from BMF_Priors.code.models.bmf_gaussian_gaussian_volumeprior import BMF_Gaussian_Gaussian_VolumePrior
from BMF_Priors.data.movielens.load_data import load_movielens_100K
from BMF_Priors.experiments.convergence.convergence_experiment import measure_convergence_time

import matplotlib.pyplot as plt


''' Run the experiment. '''
R, M = load_movielens_100K()
model_class = BMF_Gaussian_Gaussian_VolumePrior
settings = {
    'R': R, 
    'M': M, 
    'K': 20, 
    'hyperparameters': { 'alpha':1., 'beta':1., 'lamb':0.1, 'gamma':10**-50 }, 
    'init': 'random', 
    'iterations': 200,
}
fout_performances = './results/performances_gaussian_gaussian_volumeprior.txt'
fout_times = './results/times_gaussian_gaussian_volumeprior.txt'
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
