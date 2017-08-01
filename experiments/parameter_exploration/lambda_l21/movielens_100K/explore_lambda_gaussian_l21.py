'''
Run cross-validation for the Gaussian+L21 model with different lambda values, 
on the MovieLens data.
'''

project_location = "/Users/thomasbrouwer/Documents/Projects/libraries/"
import sys
sys.path.append(project_location)

from BMF_Priors.code.models.bmf_gaussian_l21 import BMF_Gaussian_L21
from BMF_Priors.data.movielens.load_data import load_processed_movielens_100K
from BMF_Priors.experiments.parameter_exploration.lambda_l21.drug_sensitivity_gdsc.explore_lambda_gaussian_l21 import explore_lambda

import itertools
import matplotlib.pyplot as plt


''' Run the experiment for the Gaussian + L21 model. '''
R, M = load_processed_movielens_100K()
model_class = BMF_Gaussian_L21
n_folds = 5
values_lambda = [10**-30, 10**-20, 10**-10, 10**0, 10**10] 
values_K = [2, 5]
values_lambda_K = list(itertools.product(values_lambda, values_K))
settings = {
    'R': R, 
    'M': M, 
    'hyperparameters': { 'alpha':1., 'beta':1., 'lamb':0.1 }, 
    'init': 'random', 
    'iterations': 250,
    'burn_in': 200,
    'thinning': 1,
}
fout = './performances_gaussian_l21.txt'
average_performances = explore_lambda(
    n_folds=n_folds, values_lambda_K=values_lambda_K, model_class=model_class, settings=settings, fout=fout)


''' Plot the performances. '''
plt.figure()
plt.ylim(0,2)
plt.title("lambda exploration performances")
for K in values_K:
    performances = [perf for perf,(lamb,Kp) in zip(average_performances['MSE'],values_lambda_K) if Kp == K]
    plt.semilogx(values_lambda, performances, label=K)
    plt.legend(loc=2)
    plt.savefig('gaussian_l21.png')