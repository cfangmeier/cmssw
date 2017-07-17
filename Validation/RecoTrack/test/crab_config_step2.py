# from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'EGamma_17-07-17_trackingNtupleProduction'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'trackingNtupleExample_electronGsfTracks81.py'


config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/cfangmei-EGamma_17-07-10_TestSubmission-fe0f0bb736606c177abe79d8a16bb1ee/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 300
config.Data.totalUnits = 100000
config.Data.outLFNDirBase = '/store/user/cfangmei'
config.Data.publication = True
config.Data.outputDatasetTag = 'EGamma_17-07-17_trackingNtupleProduction'

config.Site.storageSite = "T2_US_Nebraska"
