# /////////////////////////////////////////////////////////////////////////////
#  NOvA TIMING SYSTEM PLOTTER -- SPILL PLOTS
#  \brief   Spill-related plots
#  \author  Justin Vasel <jvasel@indiana.edu>
#  \date    February 2018
# /////////////////////////////////////////////////////////////////////////////

# Python modules
from ROOT import TH1F, gStyle, gSystem, TDatime, TCanvas, kBlack, gROOT

# App-specific modules
import Database as db
import Config as config

gStyle.SetOptStat(10)
gROOT.SetBatch(True)

nBins = 144

def SpillCounts():
    PLOT_TITLE = 'SpillCounts'
    types = [x for x in db.session.query(db.SpillType).all()]
    nBins = len(types)
    hSpillCounts = TH1F(PLOT_TITLE, 'Spill Counts (past N minutes)', nBins, -0.5, nBins - 0.5)
    
    # Loop over spill types
    for typeIdx in range(0, nBins):
        print('Spill type {} is {}'.format(typeIdx, types[typeIdx].name))
        hSpillCounts.GetXaxis().SetBinLabel(typeIdx + 1, types[typeIdx].name)
        
        spills = db.session.query(db.Spill).filter(db.Spill.spill_type_id == types[typeIdx].id).all()
        for spill in spills:
            hSpillCounts.Fill(typeIdx)
    
    hSpillCounts.GetYaxis().SetTitle('Spills')
    hSpillCounts.SetLineColor(kBlack)
    hSpillCounts.SetLineWidth(2)
    
    cSpillCounts = TCanvas(PLOT_TITLE, PLOT_TITLE, 1200, 800)
    cSpillCounts.SetLogy()
    hSpillCounts.Draw()
    cSpillCounts.Print('{}/{}.png'.format(config.PLOT_OUT_DIR, PLOT_TITLE))
