'''
Run factor analysis experiment on the GDSC drug sensitivity dataset, with 
the Gaussian + Truncated Normal + hierarchical model.
'''

import sys, os
project_location = os.path.dirname(__file__)+"/../../../../"
sys.path.append(project_location)

from BMF_Priors.code.models.bmf_gaussian_truncatednormal_hierarchical import BMF_Gaussian_TruncatedNormal_Hierarchical
from BMF_Priors.data.drug_sensitivity.load_data import load_gdsc_ic50_integer
from BMF_Priors.experiments.factor_analysis.factor_analysis import run_model_store_matrices


''' Run the experiment. '''
R, M = load_gdsc_ic50_integer()
model_class = BMF_Gaussian_TruncatedNormal_Hierarchical
n_repeats = 10
settings = {
    'R': R, 
    'M': M, 
    'K': 10,
    'hyperparameters': { 'alpha':1., 'beta':1., 'mu_mu':0., 'tau_mu':0.1, 'a':1., 'b':1. }, 
    'init': 'random', 
    'iterations': 300,
    'burn_in': 200,
    'thinning': 2,
}
fout_U = './results/gaussian_truncatednormal_hierarchical_U.txt'
fout_V = './results/gaussian_truncatednormal_hierarchical_V.txt'
all_expU, all_expV = run_model_store_matrices(
    n_repeats=n_repeats, model_class=model_class, settings=settings, fout_U=fout_U, fout_V=fout_V)
