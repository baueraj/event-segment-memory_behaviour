import analy_funs_es2
importlib.reload(analy_funs_es2)
from analy_funs_es2 import *

# ============================================================================================
# ============================================================================================

# http://rpy.sourceforge.net/rpy2/doc-dev/html/introduction.html

import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from init_es2 import *
from analy_funs_es2 import *

pandas2ri.activate()

robjects.r.source("/Users/bauera/Dropbox/UofT/experiments/common-R-code/moreyFuncs")

allDat = get_participant_data(aPs, cPs, dPath)

pGrp = 'aDat_byCs'
accDat = allDat[pGrp][0].iloc[:,:2]
accDat.reset_index(level=0, inplace=True)

# ============================================================================================
# ============================================================================================

robjects.r['summarySE']

# ============================================================================================
# ============================================================================================

# plot barplots (with error bars) of acc and RT separately, per cartoon
# adult data only
pGrp = 'aDat_byCs'
dat_plot = [allDat[pGrp][0].mean().values.tolist(), allDat[pGrp][1].mean().values.tolist()]

pltColors = ['b', 'r', 'b', 'r']
pltXLabels = ['wi_acc', 'ac_acc', 'wi_RT', 'ac_RT']

for i in range(len(dat_plot)):
    fig, ax = plt.subplots()
    ax2 = ax.twinx()  
    
    for j in range(len(dat_plot[i])):
        if j < 2:
            ax.bar(j/2 + 0.5, dat_plot[i][j], width = 0.4, align='center', color = pltColors[j])
            ax.errorbar(j/2 + 0.5, dat_plot[i][j], yerr = dat_SEM_plot[i][j], ecolor = 'k', elinewidth = 1.5)
        else:
            ax2.bar(j/2 + 0.5, dat_plot[i][j], width = 0.4, align='center', color = pltColors[j]) 
            ax2.errorbar(j/2 + 0.5, dat_plot[i][j], yerr = dat_SEM_plot[i][j], ecolor = 'k', elinewidth = 1.5)
    #plt.title(cartoonNames[i])

    rng = np.arange(0.5, 2.5, 0.5)
    ax.set_xticks(rng)
    ax.set_xticklabels(pltXLabels)
    
    ax.set_ylim([0.4, 1.0])
    ax2.set_ylim([900, 1800])

# ============================================================================================
# ============================================================================================

