# /////////////////////////////////////////////////////////////////////////////
#  NOvA TIMING SYSTEM PLOTTER -- Systems PLOTS
#  \brief   Systems-related plots
#  \author  Justin Vasel <jvasel@indiana.edu>
#  \date    February 2018
# /////////////////////////////////////////////////////////////////////////////
import math

# Python modules
from ROOT import TH1F, TH2F, gStyle, gSystem, TDatime, TCanvas, gROOT, TLegend
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
def NssHeartbeats(startTime, endTime):
    PLOT_TITLE = 'NssHeartbeats'
    timeRange = endTime - startTime
    
    minutesPerBin = int((timeRange / nBins) / 60)
    
    heartbeats = db.session.query(db.Heartbeat).filter(and_(db.Heartbeat.time > startTime, db.Heartbeat.time < endTime)).all()
    
    hNssHeartbeats = TH1F(PLOT_TITLE, 'Spill Server Heartbeats vs time (past {})'.format(util.TimeScaleTitle(timeRange)), nBins, startTime, endTime)
    hNssHeartbeats.SetLineWidth(2)
    hNssHeartbeats.SetMarkerStyle(7)
    hNssHeartbeats.SetLineColor(kBlack)
    hNssHeartbeats.GetXaxis().SetTimeDisplay(1)
    hNssHeartbeats.GetXaxis().SetTimeFormat("%H:%M")
    hNssHeartbeats.GetXaxis().SetTitle("(central time)")
        
    for heartbeat in heartbeats:
        hNssHeartbeats.Fill(heartbeat.time)
    
    hNssHeartbeats.GetYaxis().SetTitle('Heartbeats / {} minutes'.format(minutesPerBin))
    
    cNssHeartbeats = TCanvas(PLOT_TITLE, PLOT_TITLE, 1200, 800)
    hNssHeartbeats.SetMinimum(0)
    hNssHeartbeats.Draw()
    cNssHeartbeats.Print('{}/{}.png'.format(config.PLOT_OUT_DIR, PLOT_TITLE))
