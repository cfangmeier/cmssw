import FWCore.ParameterSet.Config as cms

def _label(tag):
    if hasattr(tag, "getModuleLabel"):
        t = tag
    else:
        t = cms.InputTag(tag)
    return t.getModuleLabel()+t.getProductInstanceLabel()

def customiseTrackingNtuple(process):
    process.load("Validation.RecoTrack.trackingNtuple_cff")
    process.TFileService = cms.Service("TFileService",
        fileName = cms.string('trackingNtuple.root')
    )

    if process.trackingNtuple.includeSeeds.value():
        if not hasattr(process, "reconstruction_step"):
            raise Exception("TrackingNtuple includeSeeds=True needs reconstruction which is missing")

        # enable seed stopping reason in track candidate producer
        for trkCand in process.trackingNtuple.trackCandidates.value():
            producer = getattr(process, cms.InputTag(trkCand).getModuleLabel())
            producer.produceSeedStopReasons = True

    # Replace validation_step with ntuplePath
    if not hasattr(process, "validation_step"):
        raise Exception("TrackingNtuple customise assumes process.validation_step exists")


    # Should replay mixing for pileup simhits?
    usePileupSimHits = hasattr(process, "mix") and hasattr(process.mix, "input") and len(process.mix.input.fileNames) > 0

    ntuplePath = cms.EndPath(process.trackingNtupleSequence)
    if process.trackingNtuple.includeAllHits and usePileupSimHits:
        ntuplePath.insert(0, cms.SequencePlaceholder("mix"))

        process.load("Validation.RecoTrack.crossingFramePSimHitToPSimHits_cfi")
        instanceLabels = [_label(tag) for tag in process.simHitTPAssocProducer.simHitSrc]
        process.crossingFramePSimHitToPSimHits.src = ["mix:"+l for l in instanceLabels]
        process.simHitTPAssocProducer.simHitSrc = ["crossingFramePSimHitToPSimHits:"+l for l in instanceLabels]
        process.trackingNtupleSequence.insert(0, process.crossingFramePSimHitToPSimHits)

    # Bit of a hack but works
    modifier = cms.Modifier()
    modifier._setChosen()
    modifier.toReplaceWith(process.validation_step, ntuplePath)

    process.electronNHitSeedProducer = cms.EDProducer("ElectronNHitSeedProducer",
        beamSpot = cms.InputTag("offlineBeamSpot"),
        initialSeeds = cms.VInputTag(
            cms.InputTag("newCombinedSeeds"),
        ),
        matcherConfig = cms.PSet(
            detLayerGeom = cms.string('GlobalDetLayerGeometry'),
            matchingCuts = cms.VPSet(
                cms.PSet(
                    dPhiMaxHighEt = cms.vdouble(0.05),
                    dPhiMaxHighEtThres = cms.vdouble(20.0),
                    dPhiMaxLowEtGrad = cms.vdouble(-0.002),
                    dRZMaxHighEt = cms.vdouble(9999.0),
                    dRZMaxHighEtThres = cms.vdouble(0.0),
                    dRZMaxLowEtGrad = cms.vdouble(0.0),
                    version = cms.int32(2)
                ),
                cms.PSet(
                    dPhiMaxHighEt = cms.vdouble(0.003),
                    dPhiMaxHighEtThres = cms.vdouble(0.0),
                    dPhiMaxLowEtGrad = cms.vdouble(0.0),
                    dRZMaxHighEt = cms.vdouble(0.05),
                    dRZMaxHighEtThres = cms.vdouble(30.0),
                    dRZMaxLowEtGrad = cms.vdouble(-0.002),
                    etaBins = cms.vdouble(),
                    version = cms.int32(2)
                ), 
                cms.PSet(
                    dPhiMaxHighEt = cms.vdouble(0.003),
                    dPhiMaxHighEtThres = cms.vdouble(0.0),
                    dPhiMaxLowEtGrad = cms.vdouble(0.0),
                    dRZMaxHighEt = cms.vdouble(0.05),
                    dRZMaxHighEtThres = cms.vdouble(30.0),
                    dRZMaxLowEtGrad = cms.vdouble(-0.002),
                    etaBins = cms.vdouble(),
                    version = cms.int32(2)
                )),
            minNrHits = cms.vuint32(2, 3),
            minNrHitsValidLayerBins = cms.vint32(4),
            navSchool = cms.string('SimpleNavigationSchool'),
            useRecoVertex = cms.bool(False)
        ),
        measTkEvt = cms.InputTag("MeasurementTrackerEvent"),
        superClusters = cms.VInputTag(
            cms.InputTag("particleFlowSuperClusterECAL","particleFlowSuperClusterECALBarrel"),
            cms.InputTag("particleFlowSuperClusterECAL","particleFlowSuperClusterECALEndcapWithPreshower"),
            ),
        vertices = cms.InputTag("")
    )

    from RecoParticleFlow.PFTracking.mergedElectronSeeds_cfi import electronMergedSeeds
    electronMergedSeeds.EcalBasedSeeds = cms.InputTag("electronNHitSeedProducer")

    # from RecoEgamma.EgammaElectronProducers.gedGsfElectrons_cfi import gedGsfElectronsTmp
    # gedGsfElectronsTmp.seedsTag = cms.InputTag("electronNHitSeedProducer")

    process.reconstruction.replace(process.ecalDrivenElectronSeeds , process.electronNHitSeedProducer)

    if hasattr(process, "prevalidation_step"):
        modifier.toReplaceWith(process.prevalidation_step, cms.Path())

    # remove the validation_stepN and prevalidatin_stepN of phase2 validation...    
    for p in [process.paths_(), process.endpaths_()]:    
        for pathName, path in p.iteritems():    
            if "prevalidation_step" in pathName:    
                if len(pathName.replace("prevalidation_step", "")) > 0:    
                    modifier.toReplaceWith(path, cms.Path())    
            elif "validation_step" in pathName:    
                if len(pathName.replace("validation_step", "")) > 0:    
                    modifier.toReplaceWith(path, cms.EndPath())

    # Remove all output modules
    for outputModule in process.outputModules_().itervalues():
        for path in process.paths_().itervalues():
            path.remove(outputModule)
        for path in process.endpaths_().itervalues():
            path.remove(outputModule)
        

    return process
