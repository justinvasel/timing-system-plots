# /////////////////////////////////////////////////////////////////////////////
#  NOvA TIMING SYSTEM PLOTTER -- TCR PLOTS
#  \brief   TCR-related plots
#  \author  Justin Vasel <jvasel@indiana.edu>
#  \date    February 2018
# /////////////////////////////////////////////////////////////////////////////
import math

# Python modules
from ROOT import TH1F, TH2F, gStyle, gSystem, TDatime, TCanvas, gROOT, TLegend, TColor
from ROOT import kBlack, kAzure, kMagenta, kYellow, kOrange, kPink, kGreen
from ROOT import kViridis
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
def TCRDeltas(startTime, endTime, host):
    PLOT_TITLE = 'TCRDeltas_{}'.format(host)
    timeRange = endTime - startTime
    
    deltas = db.session.query(db.TCR).filter(and_(db.TCR.tdu_id == host, db.TCR.time > startTime, db.TCR.time < endTime)).all()
    max_delta = max([x.delta for x in deltas])
    
    nBins = math.ceil(max_delta) + 2
    hTCRDeltas = TH1F(PLOT_TITLE, 'TCR Deltas (past {})'.format(util.TimeScaleTitle(timeRange)), nBins, 0, nBins)
            
    for delta in deltas:
        hTCRDeltas.Fill(delta.delta)
    
    gStyle.SetOptStat(10)
    
    hTCRDeltas.GetYaxis().SetTitle('Count')
    hTCRDeltas.GetXaxis().SetTitle('TCR Delta (64 MHz clock ticks)')
    hTCRDeltas.SetLineColor(kBlack)
    hTCRDeltas.SetLineWidth(2)
    
    cTCRDeltas = TCanvas(PLOT_TITLE, PLOT_TITLE, 1200, 800)
    cTCRDeltas.SetLogy()
    hTCRDeltas.Draw()
    cTCRDeltas.Print('{}/{}.png'.format(config.PLOT_OUT_DIR, PLOT_TITLE))
    
# .............................................................................
def TCRDeltasVsTime(startTime, endTime, host):
    PLOT_TITLE = 'TCRDeltasVsTime_{}'.format(host)
    timeRange = endTime - startTime
    
    minutesPerBin = int((timeRange / nBins) / 60)
    
    deltas = db.session.query(db.TCR).filter(and_(db.TCR.tdu_id == host, db.TCR.time > startTime, db.TCR.time < endTime)).all()
    max_delta = max([x.delta for x in deltas])
    
    hTCRDeltasVsTime = TH2F(PLOT_TITLE, 'TCR Deltas (past {}) vs time'.format(util.TimeScaleTitle(timeRange)), nBins, startTime, endTime, math.ceil(max_delta) + 2, 0, math.ceil(max_delta) + 2)
    hTCRDeltasVsTime.GetXaxis().SetTimeDisplay(1)
    hTCRDeltasVsTime.GetXaxis().SetTimeFormat("%H:%M")
    hTCRDeltasVsTime.GetXaxis().SetTitle("(central time)")
            
    for delta in deltas:
        hTCRDeltasVsTime.Fill(delta.time, delta.delta)
    
    hTCRDeltasVsTime.GetXaxis().SetTitle('(central time)')
    hTCRDeltasVsTime.GetYaxis().SetTitle('TCR Delta (64 MHz clock ticks) / {} minutes'.format(minutesPerBin))
    
    cTCRDeltasVsTime = TCanvas(PLOT_TITLE, PLOT_TITLE, 1200, 800)
    gStyle.SetPalette(kViridis)
    TColor().InvertPalette()
    gStyle.SetOptStat(0)
    hTCRDeltasVsTime.Draw('colz')
    cTCRDeltasVsTime.Print('{}/{}.png'.format(config.PLOT_OUT_DIR, PLOT_TITLE))
