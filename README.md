# JetMassSys

Package to make some quick plots (over RECO/AOD files) to investigate the effect of tracking
inefficiency systematic uncertainties on the jet mass. The main FWLite script is `plot_jmrs_trkeff.py`.
This investigates ungroomed AK8 jets in RECO/AOD, and loops through the PF candidate list. We randomly remove
charged PF candidates with some fixed (configurable) probability (the scale factor -- SF), and recompute the mass. This is
compared to the generator level in a 3-d histogram (pt,mass,mreco/mgen and then pt,mass,ptreco/ptgen).
Another script (`plot_scales_3d.py`) fits the slices of the 3-d histogram in pt and mass, and fits the xreco/xgen distributions.
The means are the JMS, the widths are the JMR, and they are written to a ROOT file. There is then a third script (`plot_jmrs_trkeff.py`) to compute
the relative ratio to the case where the tracking inefficiency is the same in data and MC (SF=1.0). 


## Instructions for running with CRAB

```
./execute_for_crab.sh
python crab_submit.py -f datasets.txt
hadd QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8.root crab_jetmass_sys/results/*.root
``` 


## Instructions to make fits

```
python plot_scales_3d.py --infile QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8.root --hist h3_mreco_mgen_100 --postfix _ungroomed_trkeff100
python plot_scales_3d.py --infile QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8.root --hist h3_mreco_mgen_099 --postfix _ungroomed_trkeff099
python plot_scales_3d.py --infile QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8.root --hist h3_mreco_mgen_100 --postfix _ungroomed_trkeff100
python plot_scales_3d.py --infile QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8.root --hist h3_mreco_mgen_099 --postfix _ungroomed_trkeff099
python plot_scales_3d.py --infile QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8.root --hist h3_mreco_mgen_098 --postfix _ungroomed_trkeff098
python plot_scales_3d.py --infile QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8.root --hist h3_mreco_mgen_097 --postfix _ungroomed_trkeff097
python plot_scales_3d.py --infile QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8.root --hist h3_mreco_mgen_096 --postfix _ungroomed_trkeff096
python plot_scales_3d.py --infile QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8.root --hist h3_mreco_mgen_095 --postfix _ungroomed_trkeff095
```

## Instructions to make uncertainty plots
```
python plot_jmrs_trkeff.py
```
