# /////////////////////////////////////////////////////////////////////////////
#  NOvA TIMING SYSTEM PLOTTER -- SPILL PLOTS
#  \brief   Spill-related plots
#  \author  Justin Vasel <jvasel@indiana.edu>
#  \date    February 2018
# /////////////////////////////////////////////////////////////////////////////

# Python modules
from ROOT import TH1F, gStyle, gSystem, TDatime, TCanvas, gROOT, TLegend
from ROOT import kBlack, kAzure, kMagenta, kYellow, kOrange, kPink, kGreen
from ROOT import kTRUE, kFALSE
from sqlalchemy import and_

# App-specific modules
import Database as db
import Config as config
import Plots.Utilities as util

gStyle.SetOptStat(10)
gROOT.SetBatch(True)

time1 = TDatime()
time2 = TDatime()
tzoffset = time1.Convert(kTRUE) - time2.Convert(kFALSE)
gStyle.SetTimeOffset(tzoffset)

nBins = 144

# .............................................................................
def SpillCounts(startTime, endTime):
    PLOT_TITLE = 'SpillCounts'
    types = [x for x in db.session.query(db.SpillType).all()]
    nBins = len(types)
    timeRange = endTime - startTime
    hSpillCounts = TH1F(PLOT_TITLE, 'Spill Counts (past {})'.format(util.TimeScaleTitle(timeRange)), nBins, 0, nBins)
    
    # Loop over spill types
    for typeIdx in range(0, nBins):
        hSpillCounts.GetXaxis().SetBinLabel(typeIdx + 1, types[typeIdx].name)
        
        spills = db.session.query(db.Spill).filter(and_(db.Spill.spill_type_id == types[typeIdx].id, db.Spill.time > startTime, db.Spill.time < endTime)).all()
        for spill in spills:
            hSpillCounts.Fill(typeIdx)
    
    hSpillCounts.GetYaxis().SetTitle('Spills')
    hSpillCounts.SetLineColor(kBlack)
    hSpillCounts.SetLineWidth(2)
    
    cSpillCounts = TCanvas(PLOT_TITLE, PLOT_TITLE, 1200, 800)
    cSpillCounts.SetLogy()
    hSpillCounts.Draw()
    cSpillCounts.Print('{}/{}.png'.format(config.PLOT_OUT_DIR, PLOT_TITLE))


# .............................................................................
def SpillCountsVsTime(startTime, endTime):
    gStyle.SetOptStat(0)
    PLOT_TITLE = 'SpillCountsVsTime'
    
    timeRange = endTime - startTime
    minutesPerBin = int((timeRange / nBins) / 60)
    
    hSpillCountsVsTimeNuMI = TH1F(PLOT_TITLE, 'Spill Counts vs time (past {})'.format(util.TimeScaleTitle(timeRange)), nBins, startTime, endTime)
    
    hSpillCountsVsTimeNuMI.GetYaxis().SetTitle('Spills / {} minutes'.format(minutesPerBin))
    hSpillCountsVsTimeNuMI.SetMarkerColor(kPink)
    hSpillCountsVsTimeNuMI.SetLineWidth(2)
    hSpillCountsVsTimeNuMI.SetMarkerStyle(34)
    hSpillCountsVsTimeNuMI.GetYaxis().SetRangeUser(0, 4e3)
    hSpillCountsVsTimeNuMI.GetXaxis().SetTimeDisplay(1)
    hSpillCountsVsTimeNuMI.GetXaxis().SetTimeFormat("%H:%M")
    hSpillCountsVsTimeNuMI.GetXaxis().SetTitle("(central time)")
    
    hSpillCountsVsTimeBNB = hSpillCountsVsTimeNuMI.Clone("BNB")
    hSpillCountsVsTimeBNB.SetMarkerColor(kMagenta + 2)
    hSpillCountsVsTimeBNBtclk = hSpillCountsVsTimeNuMI.Clone("BNBtclk")
    hSpillCountsVsTimeBNBtclk.SetMarkerColor(kAzure)
    hSpillCountsVsTimeOneHtz = hSpillCountsVsTimeNuMI.Clone("1Hz")
    hSpillCountsVsTimeOneHtz.SetMarkerColor(kOrange)
    
    for spill in db.session.query(db.Spill).filter(and_(db.Spill.time > startTime, db.Spill.time < endTime)):
        if spill.spill_type_id == 0:
            hSpillCountsVsTimeNuMI.Fill(spill.time)
        if spill.spill_type_id == 1:
            hSpillCountsVsTimeBNB.Fill(spill.time)
        if spill.spill_type_id == 3:
            hSpillCountsVsTimeBNBtclk.Fill(spill.time)
        if spill.spill_type_id == 4:
            hSpillCountsVsTimeOneHtz.Fill(spill.time)
    
    cSpillCountsVsTime = TCanvas(PLOT_TITLE, PLOT_TITLE, 1200, 800)
    hSpillCountsVsTimeNuMI.Draw("P")
    hSpillCountsVsTimeBNB.Draw("Psame")
    hSpillCountsVsTimeBNBtclk.Draw("Psame")
    hSpillCountsVsTimeOneHtz.Draw("Psame")
    
    legend = TLegend(0.7, 0.7, 0.85, 0.85)
    legend.AddEntry(hSpillCountsVsTimeBNBtclk, 'BNBtclk', 'p')
    legend.AddEntry(hSpillCountsVsTimeOneHtz, '1Hz', 'p')
    legend.AddEntry(hSpillCountsVsTimeBNB, 'BNB', 'p')
    legend.AddEntry(hSpillCountsVsTimeNuMI, 'NuMI', 'p')
    legend.SetBorderSize(0)
    legend.Draw()
    
    cSpillCountsVsTime.Print('{}/{}.png'.format(config.PLOT_OUT_DIR, PLOT_TITLE))
