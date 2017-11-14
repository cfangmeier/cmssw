import FWCore.ParameterSet.Config as cms

import Validation.RecoTrack.TrackValidation_cff as _TrackValidation_cff

process = cms.Process("electronNHitSeedProducer")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.categories.append('ElectronNHitSeedProducer')
process.MessageLogger.cerr.INFO = cms.untracked.PSet(
    limit = cms.untracked.int32(-1)
)
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

d_path = ('/mnt/hadoop/user/uscms01/pnfs/unl.edu/data4/cms/store/user/cfangmei/'
          'ZToEE_NNPDF30_13TeV-powheg_M_120_200/EGamma_17-08-08_Step2/171103_175747/0000/')

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:'+d_path+'step2_1.root')
)

from Configuration.AlCa.GlobalTag import GlobalTag
# process.GlobalTag = GlobalTag(process.GlobalTag, '92X_upgrade2017_realistic_v10', '')
process.GlobalTag = GlobalTag(globaltag='92X_upgrade2017_realistic_v10')

process.trackerTopology = cms.ESProducer('TrackerTopologyEP')
process.VolumeBasedMagneticFieldESProduce = cms.ESProducer('VolumeBasedMagneticFieldESProducerFromDB',
    valueOverride = cms.int32(-1),
)

# process.seedProducer = cms.EDProducer('ElectronNHitSeedProducer')


# _seedProducersOriginal = ['initialStepSeeds',
#                           'highPtTripletStepSeeds',
#                           'mixedTripletStepSeeds',
#                           'pixelLessStepSeeds',
#                           'tripletElectronSeeds',
#                           'pixelPairElectronSeeds',
#                           'stripPairElectronSeeds']
# (_seedSelectorsOriginal, trackingNtupleSeedSelectorsOriginal) = _TrackValidation_cff._addSeedToTrackProducers(_seedProducersOriginal, globals())

process.navigationSchoolESProducer = cms.ESProducer( "NavigationSchoolESProducer",
  ComponentName = cms.string( "SimpleNavigationSchool" ),
  SimpleMagneticField = cms.string( "ParabolicMf" )
)

process.seedProducer = cms.EDProducer( "ElectronNHitSeedProducer",
    matcherConfig = cms.PSet(
      detLayerGeom = cms.string( "hltESPGlobalDetLayerGeometry" ),
      navSchool = cms.string( "SimpleNavigationSchool" ),
      useRecoVertex = cms.bool( False ),
      minNrHits = cms.vuint32( 2, 3 ),
      matchingCuts = cms.VPSet( 
        cms.PSet(
          dPhiMaxHighEt = cms.vdouble( 0.05 ),
          version = cms.int32( 2 ),
          dRZMaxHighEt = cms.vdouble( 9999.0 ),
          dRZMaxLowEtGrad = cms.vdouble( 0.0 ),
          dPhiMaxLowEtGrad = cms.vdouble( -0.002 ),
          dPhiMaxHighEtThres = cms.vdouble( 20.0 ),
          dRZMaxHighEtThres = cms.vdouble( 0.0 )
        ),
        cms.PSet(
          etaBins = cms.vdouble(  ),
          dPhiMaxHighEt = cms.vdouble( 0.003 ),
          version = cms.int32( 2 ),
          dRZMaxHighEt = cms.vdouble( 0.05 ),
          dRZMaxLowEtGrad = cms.vdouble( -0.002 ),
          dPhiMaxLowEtGrad = cms.vdouble( 0.0 ),
          dPhiMaxHighEtThres = cms.vdouble( 0.0 ),
          dRZMaxHighEtThres = cms.vdouble( 30.0 )
        ),
        cms.PSet(
          etaBins = cms.vdouble(  ),
          dPhiMaxHighEt = cms.vdouble( 0.003 ),
          version = cms.int32( 2 ),
          dRZMaxHighEt = cms.vdouble( 0.05 ),
          dRZMaxLowEtGrad = cms.vdouble( -0.002 ),
          dPhiMaxLowEtGrad = cms.vdouble( 0.0 ),
          dPhiMaxHighEtThres = cms.vdouble( 0.0 ),
          dRZMaxHighEtThres = cms.vdouble( 30.0 )
        )
      ),
      minNrHitsValidLayerBins = cms.vint32( 4 )
    ),
    beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
    measTkEvt = cms.InputTag( "hltSiStripClusters" ),
    vertices = cms.InputTag( "" ),
    # superClusters = cms.VInputTag( 'hltEgammaSuperClustersToPixelMatch' ),
    superClusters = cms.VInputTag(
        "particleFlowSuperClusterECAL:particleFlowSuperClusterECALBarrel",
        "particleFlowSuperClusterECAL:particleFlowSuperClusterECALEndcapWithPreshower"
    ),
    # initialSeeds = cms.InputTag( "hltElePixelSeedsCombined" )
    initialSeeds = cms.InputTag( "initialStepSeeds" )
)

process.p = cms.Path(process.seedProducer)
