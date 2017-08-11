"""
Plot the convergence of the many different BMF algorithms on the GDSC data.
"""

import matplotlib.pyplot as plt


''' Plot settings. '''
MSE_min, MSE_max = 425, 750
it_min, it_max = 0, 200
iterations = range(1,200+1)

folder_plots = "./"
folder_results = "./../results/"
plot_file = folder_plots+"convergences_gdsc_numbered.png"


''' Load in the performances. '''
ggg = eval(open(folder_results+'performances_gaussian_gaussian.txt','r').read())
gggu = eval(open(folder_results+'performances_gaussian_gaussian_univariate.txt','r').read())
gggw = eval(open(folder_results+'performances_gaussian_gaussian_wishart.txt','r').read())
ggga = eval(open(folder_results+'performances_gaussian_gaussian_ard.txt','r').read())
gll = eval(open(folder_results+'performances_gaussian_laplace.txt','r').read())
glli = eval(open(folder_results+'performances_gaussian_laplace_ig.txt','r').read())
gvg = eval(open(folder_results+'performances_gaussian_gaussian_volumeprior.txt','r').read())
gvng = eval(open(folder_results+'performances_gaussian_gaussian_volumeprior_nonnegative.txt','r').read())
geg = eval(open(folder_results+'performances_gaussian_gaussian_exponential.txt','r').read())
gee = eval(open(folder_results+'performances_gaussian_exponential.txt','r').read())
geea = eval(open(folder_results+'performances_gaussian_exponential_ard.txt','r').read())
gtt = eval(open(folder_results+'performances_gaussian_truncatednormal.txt','r').read())
gttn = eval(open(folder_results+'performances_gaussian_truncatednormal_hierarchical.txt','r').read())
gl21 = eval(open(folder_results+'performances_gaussian_l21.txt','r').read())
pgg = eval(open(folder_results+'performances_poisson_gamma.txt','r').read())
pggg = eval(open(folder_results+'performances_poisson_gamma_gamma.txt','r').read())

nmf_np = eval(open(folder_results+'performances_baseline_mf_nonprobabilistic.txt').read())
row = eval(open(folder_results+'performances_baseline_average_row.txt','r').read())
column = eval(open(folder_results+'performances_baseline_average_column.txt','r').read())


''' Assemble the average performances and method names. '''
performances_names_colours_linestyles_markers = [
    (ggg,  'GGG',  'r', '-', '1'),
    (gggu, 'GGGU', 'r', '-', '2'),
    (ggga, 'GGGA', 'r', '-', '3'),
    (gggw, 'GGGW', 'r', '-', '4'),
    (gll,  'GLL',  'r', '-', '5'),
    (glli, 'GLLI', 'r', '-', '6'),
    (gvg,  'GVG',  'r', '-', '7'),
    (gee,  'GEE',  'b', '-', '1'),
    (geea, 'GEEA', 'b', '-', '2'),
    (gtt,  'GTT',  'b', '-', '3'),
    (gttn, 'GTTN', 'b', '-', '4'),
    (gl21, 'GL21', 'b', '-', '5'),
    (geg,  'GEG',  'g', '-', '1'),
    (gvng, 'GVnG', 'g', '-', '2'),
    (pgg,  'PGG',  'y', '-', '1'),
    (pggg, 'PGGG', 'y', '-', '2'),
    (nmf_np, 'Row',    'grey', '-', '1'),
    (column, 'NMF-NP', 'grey', '-', '2'),
    (row,    'Col',    'grey', '-', '3'),
]


''' Plot the performances. '''
fig = plt.figure(figsize=(3,2.25))
fig.subplots_adjust(left=0.135, right=0.97, bottom=0.135, top=0.97)
plt.xlabel("Iterations", fontsize=9, labelpad=0)
plt.ylabel("MSE", fontsize=9, labelpad=2)
plt.xticks(fontsize=6)

x = iterations
for performances, name, colour, linestyle, marker in performances_names_colours_linestyles_markers:
    y = performances
    print name, performances[-1]
    plt.plot(x, y, label=name, linestyle=linestyle, c=colour, marker=('$%s$' % marker), 
             markevery=10, markersize=3, linewidth=0.5)
 
plt.yticks(range(0,MSE_max+1,50),fontsize=6)
plt.ylim(MSE_min,MSE_max)
plt.xlim(it_min, it_max)
    
plt.savefig(plot_file, dpi=600)
    