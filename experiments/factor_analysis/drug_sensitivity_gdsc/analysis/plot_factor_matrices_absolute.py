"""
Plot the factor analysis outcomes:
- Use only the first repeat's factor matrices U, V.
- Plot these factor matrices. Take the absolute of all values, and divide each 
  row by the row's max value.
"""

import sys, os
project_location = os.path.dirname(__file__)+"/../../../../../"
sys.path.append(project_location)

from BMF_Priors.data.drug_sensitivity.load_data import load_gdsc_ic50

import matplotlib.pyplot as plt
import numpy
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram


''' Plot settings. '''
figsize_U = (1,30)
figsize_V = (1,4)
left, right, bottom, top = 0.01, 0.99, 0.01, 0.99
fontsize = 14


''' Load in the factor matrices. '''
folder_results = "./../results/"
names_filenames = [
    ('NMF-NP', 'baseline_mf_nonprobabilistic_abs'),
    ('GGG',    'gaussian_gaussian_abs'),
    ('GGGU',   'gaussian_gaussian_univariate_abs'),
    ('GGGW',   'gaussian_gaussian_wishart_abs'),
    ('GGGA',   'gaussian_gaussian_ard_abs'),
    ('GLL',    'gaussian_laplace_abs'),
    ('GLLI',   'gaussian_laplace_ig_abs'),
    ('GEG',    'gaussian_gaussian_exponential_abs'),
    ('GEE',    'gaussian_exponential_abs'),
    ('GEEA',   'gaussian_exponential_ard_abs'),
    ('GTT',    'gaussian_truncatednormal_abs'),
    ('GTTN',   'gaussian_truncatednormal_hierarchical_abs'),
    ('GL21',   'gaussian_l21_abs'),
    ('GVG',    'gaussian_gaussian_volumeprior_abs'),
    ('GVnG',   'gaussian_gaussian_volumeprior_nonnegative_abs'),
    ('PGG',    'poisson_gamma_abs'),
    ('PGGG',   'poisson_gamma_gamma_abs'),   
]
name_plotname_U_V = [
    (name, filename, eval(open(folder_results+'%s_U.txt' % (filename),'r').read())[0], 
                     eval(open(folder_results+'%s_V.txt' % (filename),'r').read())[0])
    for name, filename in names_filenames
]


''' Method for computing dendrogram. Return order of indices. '''
def compute_dendrogram(R):
    #plt.figure()
    # Hierarchical clustering methods: 
    # single (Nearest Point), complete (Von Hees), average (UPGMA), weighted (WPGMA), centroid (UPGMC), median (WPGMC), ward (incremental)
    Y = linkage(y=R, method='centroid', metric='euclidean') 
    Z = dendrogram(Z=Y, orientation='top', no_plot=True)#False)
    reordered_indices = Z['leaves']
    return reordered_indices
        

''' Plot the performances. '''
folder_plots_factor_matrices = './plots_factor_matrices_absolute/'
plot = True
# If True, run hierarchical clustering on R and reorder rows of kernelU, kernelV based on that
reorder_rows_columns = True 
if reorder_rows_columns:
    R, M = load_gdsc_ic50()
    indices_rows = compute_dendrogram(R)
    indices_columns = compute_dendrogram(R.T)

if plot:
    for name, plotname, U, V in name_plotname_U_V:
        U, V = numpy.array(U), numpy.array(V)
        U, V = numpy.abs(U), numpy.abs(V)
        
        # Renormalise each factor matrix row to have a maximum absolute value of 1
        row_max_U, row_max_V = numpy.abs(U).max(axis=1), numpy.abs(V).max(axis=1)
        U = numpy.array([U[i] / row_max_U[i] for i in range(U.shape[0])])
        V = numpy.array([V[i] / row_max_V[i] for i in range(V.shape[0])])
        
        # Reorder rows and columns using hierarchical clustering of R
        if reorder_rows_columns:
            U = U[indices_rows,:]
            V = V[indices_columns,:]
        
        ''' Plot U. '''
        fig, ax = plt.subplots(figsize=figsize_U)
        ax.imshow(U, cmap=plt.cm.bwr, interpolation='nearest', vmin=-1, vmax=1)
        
        # Turn off all the ticks
        ax = plt.gca()
        for t in ax.xaxis.get_major_ticks():
            t.tick1On = False
            t.tick2On = False
        for t in ax.yaxis.get_major_ticks():
            t.tick1On = False
            t.tick2On = False
        
        # Get rid of row and column labels
        ax.set_xticklabels([]), ax.set_yticklabels([])
        
        # Turn off the frame
        #ax.set_frame_on(False)
        
        # Store the plot
        plot_file = folder_plots_factor_matrices+'%s_U' % (plotname)
        plt.savefig(plot_file, dpi=600, bbox_inches='tight')
        plt.close()
        
        ''' Plot V. '''
        fig, ax = plt.subplots(figsize=figsize_V)
        ax.imshow(V, cmap=plt.cm.bwr, interpolation='nearest', vmin=-1, vmax=1)
        
        # Turn off all the ticks
        ax = plt.gca()
        for t in ax.xaxis.get_major_ticks():
            t.tick1On = False
            t.tick2On = False
        for t in ax.yaxis.get_major_ticks():
            t.tick1On = False
            t.tick2On = False
        
        # Get rid of row and column labels
        ax.set_xticklabels([]), ax.set_yticklabels([])
        
        # Turn off the frame
        #ax.set_frame_on(False)
        
        # Store the plot
        plot_file = folder_plots_factor_matrices+'%s_V' % (plotname)
        plt.savefig(plot_file, dpi=600, bbox_inches='tight')
        plt.close()