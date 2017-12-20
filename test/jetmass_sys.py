# import ROOT in batch mode
import sys
import ROOT
# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()
import random
import array

def getMatched(obj,coll,dR=0.1):
    p4 = ROOT.TLorentzVector(obj.px(), obj.py(), obj.pz(), obj.energy())
    for i,c in enumerate(coll):
        cp4 = ROOT.TLorentzVector(c.px(), c.py(), c.pz(), c.energy())
        if p4.DeltaR(cp4) < dR :
            return i,c
    return -1,None
        

def jetmass_sys(argv) :
    
    from optparse import OptionParser
    parser = OptionParser()

    parser.add_option('--files', type='string', action='store',
                      dest='files',
                      help='Input files')

    parser.add_option('--xrootd', type='string', action='store',
                      default=None,
                      dest='xrootd',
                      help='xrootd redirector, try root://cmsxrootd.fnal.gov/')

    parser.add_option('--trkeff', type='float', action='store',
                      default=0.95,
                      dest='trkeff',
                      help='Track efficiency')

    parser.add_option('--verbose', action='store_true',
                      dest='verbose', default = False,
                      help='Verbose')
    
    (options, args) = parser.parse_args()
    argv = []

    
    filelist = file( options.files )
    filesraw = filelist.readlines()
    files = []
    nevents = 0
    for ifile in filesraw : #{ Loop over text file and find root files linked
        if len( ifile ) > 2 :
            if options.xrootd != None : 
                #s = 'root://cmsxrootd.fnal.gov/' + ifile.rstrip()
                s = options.xrootd + ifile.rstrip()
            else :
                s = ifile.rstrip()
            files.append( s )
            print 'Added ' + s
            #} End loop over txt file

    # load FWlite python libraries
    from DataFormats.FWLite import Handle, Events
    fatjets, fatjetLabel = Handle("std::vector<reco::PFJet>"), "ak8PFJetsCHS"
    genjets, genjetLabel = Handle("std::vector<reco::GenJet>"), "ak8GenJetsNoNu"


    fout = ROOT.TFile("outplots.root", "RECREATE")

    binszzz = array.array('d', [] )
    for ival in xrange( 80 ):
        binszzz.append( ival * 0.025 )
    ptBinA = array.array('d', [  200., 260., 350., 460., 550., 650., 760., 900, 1000, 1100, 1200, 1300, 13000.])
    nbinsPt = len(ptBinA) - 1
    mBinA = array.array('d', [0, 1, 5, 10, 20, 40, 60, 80, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000])
    nbinsm = len(mBinA) - 1
    
    h3_mreco_mgen = ROOT.TH3F("h3_mreco_mgen", "Reco Mass/Gen Mass", nbinsPt, ptBinA, nbinsm, mBinA, len(binszzz) - 1, binszzz)
    h3_ptreco_ptgen = ROOT.TH3F("h3_ptreco_ptgen", "Reco pt/Gen pt", nbinsPt, ptBinA, nbinsm, mBinA, len(binszzz) - 1, binszzz)

    # loop over files
    for ifile in files : #{ Loop over root files
        events = Events(ifile)
        print 'Processing ', ifile
        for iev,event in enumerate(events):
            if iev % 1000 == 0 :
                print 'Processing ', iev
            event.getByLabel(fatjetLabel, fatjets)
            event.getByLabel(genjetLabel, genjets)

            if len(genjets.product()) == 0 or len(fatjets.product()) == 0:
                continue
            # Fat AK8 Jets
            for i,j in enumerate(fatjets.product()):
                if j == None :
                    continue
                if j.pt() < 200. :
                    continue
                if genjets.product() == None :
                    continue
                igen,gen = getMatched( j, genjets.product() )
                if gen == None :
                    continue
                if options.verbose:
                    print "jetAK8 %3d: pt %5.1f, eta %+4.2f, mass %5.1f" % (
                        i, j.pt(), j.eta(), j.mass())
                    print "genAK8 %3d: pt %5.1f, eta %+4.2f, mass %5.1f" % (
                        igen, gen.pt(), gen.eta(), gen.mass()
                        )
                constituents = []
                constituentsP4 = []
                for ida in xrange( j.numberOfDaughters() ) :
                    constituents.append( j.daughter(ida) )
                for ic,c in enumerate(constituents):
                    #calo_e = c.ecalEnergy() + c.hcalEnergy()
                    #calo_p4 = ROOT.TLorentzVector()
                    
                    #print ' %3d : %6.2f / %6.2f = %6.3e' % ( ic, c.pt(), calo_e, calo_e / c.pt() )
                    if random.random() < options.trkeff :
                        constituentsP4.append( ROOT.TLorentzVector(c.px(), c.py(), c.pz(), c.energy()) )

                oldp4 = ROOT.TLorentzVector( j.px(), j.py(), j.pz(), j.energy () )
                newp4 = sum( constituentsP4, ROOT.TLorentzVector() )
                deltapt = oldp4.Perp() - newp4.Perp()
                deltam = oldp4.M() - newp4.M()
                h3_mreco_mgen.Fill( gen.pt(), gen.mass(), newp4.M() / gen.mass() )
                h3_ptreco_ptgen.Fill( gen.pt(), gen.mass(), newp4.Perp() / gen.pt() )
                if options.verbose:
                    print ' dpt : (%5.2f - %5.2f) / %5.2f  = %6.2e' % ( oldp4.Perp(), newp4.Perp(), gen.pt(), newp4.Perp()/gen.pt()  )
                    print ' dm  : (%5.2f - %5.2f) / %5.2f  = %6.2e' % ( oldp4.M(),    newp4.M(),    gen.mass(),  newp4.M()/gen.mass()  )

    fout.cd()
    h3_mreco_mgen.Write()
    h3_ptreco_ptgen.Write()
    fout.Close()


if __name__ == "__main__" :
    jetmass_sys(sys.argv)
