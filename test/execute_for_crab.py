import sys
import PSet
files = []
outfile = file( 'filesToProcess.txt', 'w')
for ifile in PSet.process.source.fileNames :    
    outfile.write( ifile + '\n' )


outfile.close()

sys.argv.append('--files')
sys.argv.append('filesToProcess.txt')

print sys.argv

from jetmass_sys import *

jetmass_sys(sys.argv)

