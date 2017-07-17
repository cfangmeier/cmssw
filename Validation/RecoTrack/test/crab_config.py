# from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'EGamma_17-07-10_TestSubmission'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'trackingNtupleExample_DIGI_L1_DIGI2RAW.py'

config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/PhaseIFall16DR-FlatPU28to62HcalNZSRAW_81X_upgrade2017_realistic_v26-v1/GEN-SIM-RAW'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 3
config.Data.totalUnits = config.Data.unitsPerJob*100
config.Data.outLFNDirBase = '/store/user/cfangmei'
config.Data.publication = True
config.Data.outputDatasetTag = 'EGamma_17-07-10_TestSubmission'

config.Site.storageSite = "T2_US_Nebraska"
