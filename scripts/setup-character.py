# Set scene parameters to fit character
scene.setScale(1.0)
scene.setBoolAttribute('internalAudio', True)
scene.run('lighting.py')                        # Initial lighting for scene
camera = getCamera()
camera.setEye(0.03, 1.59, 1.42)
camera.setCenter(0.11, 0.88, -0.43)
camera.setUpVector(SrVec(0, 1, 0))
camera.setScale(1)
camera.setFov(1.0472)
camera.setFarPlane(100)
camera.setNearPlane(0.1)
camera.setAspectRatio(0.966897)
scene.getPawn('camera').setPosition(SrVec(0, -2, 0))

# Set joint map for character
scene.run('zebra2-map.py')
zebra2Map = scene.getJointMapManager().getJointMap('zebra2')
rachelSkeleton = scene.getSkeleton('ChrRachel.sk')
zebra2Map.applySkeleton(rachelSkeleton)
zebra2Map.applyMotionRecurse('ChrRachel')

# Establish lip syncing data set
scene.run('init-diphoneDefault.py')

# Set up character face definition
scene.run('face-definition.py')

# Load and turn on deformable mesh and GPU
rachel.setDoubleAttribute('deformableMeshScale', .01)
rachel.setStringAttribute('deformableMesh', 'ChrRachel.dae')
rachel.setStringAttribute("displayType", "GPUmesh")

# Set up diphone lip syncing
rachel.setStringAttribute('lipSyncSetName', 'default')
rachel.setBoolAttribute('usePhoneBigram', True)

# Use TTS Relay for voice
#rachel.setVoice('remote')
#rachel.setVoiceCode('Microsoft|Zira|Desktop')

# Use pre-recorded audio files for voice
rachel.setStringAttribute("voice", "audiofile")
rachel.setStringAttribute("voiceCode", ".")

# Set saccade mode for character to talk
bml.execBML('*', '<saccade mode="talk"/>')

# Setup character gestures, body posture, and gaze target
scene.run('BehaviorSetGestures.py')
setupBehaviorSet()
retargetBehaviorSet('ChrRachel')
bml.execBML('ChrRachel', '<body posture="ChrBrad@Idle01"/>')
