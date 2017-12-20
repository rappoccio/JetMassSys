import FWCore.ParameterSet.Config as cms

process = cms.Process('NoSplit')

process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring([
'/store/mc/RunIIFall17DRStdmix/QCD_Pt-15to7000_TuneCP5_Flat2017_13TeV_pythia8/AODSIM/NoPU_94X_mc2017_realistic_v10-v2/40000/000A2345-58D8-E711-95B6-0CC47A4D7690.root'
    ]))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
