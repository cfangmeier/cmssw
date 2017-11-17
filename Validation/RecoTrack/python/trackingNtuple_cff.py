from __future__ import print_function
import FWCore.ParameterSet.Config as cms

from RecoLocalTracker.Configuration.RecoLocalTracker_cff import *
from SimGeneral.TrackingAnalysis.simHitTPAssociation_cfi import *
from SimTracker.TrackerHitAssociation.tpClusterProducer_cfi import *
from SimTracker.TrackAssociatorProducers.quickTrackAssociatorByHits_cfi import *
from RecoTracker.TransientTrackingRecHit.TTRHBuilders_cff import *
from RecoLocalTracker.SiPixelRecHits.PixelCPEGeneric_cfi import *
from Geometry.TrackerNumberingBuilder.trackerTopology_cfi import *

from Validation.RecoTrack.trackingNtuple_cfi import *
from Validation.RecoTrack.TrackValidation_cff import *
from SimGeneral.TrackingAnalysis.trackingParticleNumberOfLayersProducer_cff import *
import Validation.RecoTrack.TrackValidation_cff as _TrackValidation_cff
import RecoTracker.IterativeTracking.ElectronSeeds_cff as _electron_cff

_includeHits = True
#_includeHits = False

_includeSeeds = True
#_includeSeeds = False

from CommonTools.RecoAlgos.trackingParticleRefSelector_cfi import trackingParticleRefSelector as _trackingParticleRefSelector
trackingParticlesIntime = _trackingParticleRefSelector.clone(
    signalOnly = False,
    intimeOnly = True,
    chargedOnly = False,
    tip = 1e5,
    lip = 1e5,
    minRapidity = -10,
    maxRapidity = 10,
    ptMin = 0,
)
trackingNtuple.trackingParticles = "trackingParticlesIntime"
trackingNtuple.trackingParticlesRef = True
trackingNtuple.includeAllHits = _includeHits
trackingNtuple.includeSeeds = _includeSeeds

def _filterForNtuple(lst):
    ret = []
    for item in lst:
        if "PreSplitting" in item:
            continue
        if "SeedsA" in item and item.replace("SeedsA", "SeedsB") in lst:
            ret.append(item.replace("SeedsA", "Seeds"))
            continue
        if "SeedsB" in item:
            continue
        if "SeedsPair" in item and item.replace("SeedsPair", "SeedsTripl") in lst:
            ret.append(item.replace("SeedsPair", "Seeds"))
            continue
        if "SeedsTripl" in item:
            continue
        ret.append(item)
    return ret

# Build seed tracks from the GSF tracks seeds
_seedProducers = ['electronMergedSeeds']
# _seedProducers = _filterForNtuple(_TrackValidation_cff._seedProducers)
(_seedSelectors, trackingNtupleSeedSelectors) = _TrackValidation_cff._addSeedToTrackProducers(_seedProducers, globals())

trackingNtuple.seedTracks = _seedSelectors
# def _seedProdToTrackCands(name):
#         return name.replace("seedTracks", "").replace("Seeds", "TrackCandidates")
# trackingNtuple.trackCandidates = map(_seedProdToTrackCands, _seedProducers)
trackingNtuple.tracks = cms.untracked.InputTag('electronGsfTracks')

# Matches to the original seeds defined in RecoTracker.IterativeTracking.ElectronSeeds_cff
_seedProducersOriginal = ['initialStepSeeds',
                          'highPtTripletStepSeeds',
                          'mixedTripletStepSeeds',
                          'pixelLessStepSeeds',
                          'tripletElectronSeeds',
                          'pixelPairElectronSeeds',
                          'stripPairElectronSeeds']
(_seedSelectorsOriginal, trackingNtupleSeedSelectorsOriginal) = _TrackValidation_cff._addSeedToTrackProducers(_seedProducersOriginal, globals())
trackingNtuple.seedTracksOriginal = _seedSelectorsOriginal
trackingNtuple.barrelSuperClusters = cms.untracked.InputTag("particleFlowSuperClusterECAL:particleFlowSuperClusterECALBarrel")
trackingNtuple.endcapSuperClusters = cms.untracked.InputTag("particleFlowSuperClusterECAL:particleFlowSuperClusterECALEndcapWithPreshower")
trackingNtupleSequence = cms.Sequence()

# reproduce hits because they're not stored in RECO
if _includeHits:
    trackingNtupleSequence += (
        siPixelRecHits +
        siStripMatchedRecHits
    )

if _includeSeeds:
    trackingNtupleSequence += trackingNtupleSeedSelectors
    trackingNtupleSequence += trackingNtupleSeedSelectorsOriginal

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
seedProducer = cms.EDProducer( "ElectronNHitSeedProducer",
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
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

# seedProducer_step = cms.Path(seedProducer)
trackingNtuple.electronSeeds = cms.untracked.InputTag("electronNHitSeedProducer")

dump=cms.EDAnalyzer('EventContentAnalyzer')  # See: https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookWriteFrameworkModule#SeE

trackingNtupleSequence += (
    # sim information
    trackingParticlesIntime +
    simHitTPAssocProducer +
    tpClusterProducer +
    quickTrackAssociatorByHits +
    trackingParticleNumberOfLayersProducer +
    # Add Electron Seed Info
    seedProducer +
    # ntuplizer
    dump +
    trackingNtuple
)

trackingPhase2PU140.toModify(trackingNtuple, # FIXME
  pixelDigiSimLink = cms.untracked.InputTag('simSiPixelDigis', "Pixel"),
  stripDigiSimLink = cms.untracked.InputTag(''),
  phase2OTSimLink = cms.untracked.InputTag('simSiPixelDigis', "Tracker")
)
print('Configuration for Ntuple finished')
