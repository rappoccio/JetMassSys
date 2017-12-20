# import ROOT in batch mode
import sys
import ROOT
# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()


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
    fatjets, fatjetLabel = Handle("std::vector<pat::Jet>"), "slimmedJetsAK8"

            
    # loop over files
    for ifile in files : #{ Loop over root files
        events = Events(ifile)
        for iev,event in enumerate(events):
            event.getByLabel(fatjetLabel, fatjets)
            # Fat AK8 Jets
            for i,j in enumerate(fatjets.product()):
                print "jetAK8 %3d: pt %5.1f (raw pt %5.1f), eta %+4.2f, mass %5.1f ungroomed, %5.1f softdrop " % (
                    i, j.pt(), j.pt()*j.jecFactor('Uncorrected'), j.eta(), j.mass(), j.userFloat('ak8PFJetsPuppiSoftDropMass'))
                # To get the constituents of the AK8 jets, you have to loop over all of the
                # daughters recursively. To save space, the first two constituents are actually
                # the Soft Drop SUBJETS, which will then point to their daughters.
                # The remaining constituents are those constituents removed by soft drop but
                # still in the AK8 jet.
                #if 'jetAk8' not in seenIt:
                constituents = []
                for ida in xrange( j.numberOfDaughters() ) :
                    cand = j.daughter(ida)
                    if cand.numberOfDaughters() == 0 :
                        constituents.append( [cand, 'cand'] )
                    else :
                        for jda in xrange( cand.numberOfDaughters() ) :
                            cand2 = cand.daughter(jda)
                            constituents.append( [cand2, 'subjet'] )
                constituents.sort(key = lambda c:c[0].pt(), reverse=True)

                wSubjets = j.subjets('SoftDropPuppi')
                for iw,wsub in enumerate( wSubjets ) :
                    print "   w subjet %3d: pt %5.1f (raw pt %5.1f), eta %+4.2f, mass %5.1f " % (
                        iw, wsub.pt(), wsub.pt()*wsub.jecFactor('Uncorrected'), wsub.eta(), wsub.mass()
                        )
                    print "   \tbtag discriminators:"
                    for btag in wsub.getPairDiscri():
                        print  "\t\t%s %s" % (btag.first, btag.second)
                    print "   \tuserFloats:"
                    for ufl in wsub.userFloatNames():
                        print  "\t\t%s %s" % (ufl, wsub.userFloat(ufl))
                    seenIt['jetAk8SD'] = True




if __name__ == "__main__" :
    jetmass_sys(sys.argv)
