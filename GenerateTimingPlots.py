# /////////////////////////////////////////////////////////////////////////////
#  NOvA TIMING SYSTEM PLOTTER
#  \brief   A script to produce timing system plots
#  \author  Justin Vasel <jvasel@indiana.edu>
#  \date    February 2018
# /////////////////////////////////////////////////////////////////////////////

import code

import Config as config
from Plots import SpillPlots
from Plots import TCRPlots
from Plots import SystemsPlots

timeBegin = 1518908400
timeEnd = 1518994800

# SPILL PLOTS
SpillPlots.SpillCounts(timeBegin, timeEnd)
SpillPlots.SpillCountsVsTime(timeBegin, timeEnd)

# TCR PLOTS
TCRPlots.TCRDeltas(timeBegin, timeEnd, 'tdu-near-master-ppc-01')
TCRPlots.TCRDeltasVsTime(timeBegin, timeEnd, 'tdu-near-master-ppc-01')

# SYSTEM PLOTS
SystemsPlots.NssHeartbeats(timeBegin, timeEnd)
