cmsDriver.py generate_step2 \
  --conditions 92X_upgrade2017_realistic_v10 \
  -n 10 \
  --era Run2_2017 \
  --eventcontent FEVTDEBUG \
  -s DIGI:pdigi_valid,L1,DIGI2RAW \
  --datatier GEN-SIM-DIGI-RAW \
  --filein /store/mc/RunIISummer17DRStdmix/ZToEE_NNPDF30_13TeV-powheg_M_120_200/GEN-SIM-RAW/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v1/150000/04B374C3-40AA-E711-84BF-0CC47A78A360.root \
  --fileout file:step2.root \
  --no_exec
