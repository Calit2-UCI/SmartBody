####################################################
#                                                  #
#                  SmartBody RIVA                  #
#                                                  #
# Stephanie Chang - Calit2 Dev Fall 2014           #
#   Python 2.7.3                                   #
####################################################

import io
import time as systime
from random import randrange

print "|--------------------------------------------|"
print "|        Starting VirtualAssistant           |"
print "|--------------------------------------------|"

####################################################
#                                                  #
#                CHARACTER SET UP                  #
#                                                  #
####################################################

# Add asset paths
scene.addAssetPath('script', 'scripts')
scene.addAssetPath('mesh', 'mesh')
scene.addAssetPath('motion', 'ChrRachel')
scene.addAssetPath('script', 'behaviorsets')
scene.addAssetPath('audio', 'speech')
scene.loadAssets()

# Set scene parameters to fit character
scene.setScale(1.0)
scene.setBoolAttribute('internalAudio', True)
scene.run('default-viewer.py')
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
rachelFace = scene.createFaceDefinition('ChrRachel')
rachelFace.setFaceNeutral('ChrRachel@face_neutral')
rachelFace.setAU(1,  "left",  "ChrRachel@001_inner_brow_raiser_lf")
rachelFace.setAU(1,  "right", "ChrRachel@001_inner_brow_raiser_rt")
rachelFace.setAU(2,  "left",  "ChrRachel@002_outer_brow_raiser_lf")
rachelFace.setAU(2,  "right", "ChrRachel@002_outer_brow_raiser_rt")
rachelFace.setAU(4,  "left",  "ChrRachel@004_brow_lowerer_lf")
rachelFace.setAU(4,  "right", "ChrRachel@004_brow_lowerer_rt")
rachelFace.setAU(5,  "both",  "ChrRachel@005_upper_lid_raiser")
rachelFace.setAU(6,  "both",  "ChrRachel@006_cheek_raiser")
rachelFace.setAU(7,  "both",  "ChrRachel@007_lid_tightener")
rachelFace.setAU(10, "both",  "ChrRachel@010_upper_lip_raiser")
rachelFace.setAU(12, "left",  "ChrRachel@012_lip_corner_puller_lf")
rachelFace.setAU(12, "right", "ChrRachel@012_lip_corner_puller_rt")
rachelFace.setAU(25, "both",  "ChrRachel@025_lips_part")
rachelFace.setAU(26, "both",  "ChrRachel@026_jaw_drop")
rachelFace.setAU(45, "left",  "ChrRachel@045_blink_lf")
rachelFace.setAU(45, "right", "ChrRachel@045_blink_rt")

rachelFace.setViseme("open",    "ChrRachel@open")
rachelFace.setViseme("W",       "ChrRachel@W")
rachelFace.setViseme("ShCh",    "ChrRachel@ShCh")
rachelFace.setViseme("PBM",     "ChrRachel@PBM")
rachelFace.setViseme("FV",      "ChrRachel@FV")
rachelFace.setViseme("wide",    "ChrRachel@wide")
rachelFace.setViseme("tBack",   "ChrRachel@tBack")
rachelFace.setViseme("tRoof",   "ChrRachel@tRoof")
rachelFace.setViseme("tTeeth",  "ChrRachel@tTeeth")

rachel = scene.createCharacter('ChrRachel', '')
rachelSkeleton = scene.createSkeleton('ChrRachel.sk')
rachel.setSkeleton(rachelSkeleton)
rachelPos = SrVec(0, 0, 0)
rachel.setPosition(rachelPos)
rachel.setHPR(SrVec(0, 0, 0))
rachel.setFaceDefinition(rachelFace)
rachel.createStandardControllers()

# Load and turn on deformable mesh and GPU
rachel.setDoubleAttribute('deformableMeshScale', .01)
rachel.setStringAttribute('deformableMesh', 'ChrRachel.dae')
rachel.setStringAttribute("displayType", "GPUmesh")

# Set up diphone lip syncing
rachel.setStringAttribute('lipSyncSetName', 'default')
rachel.setBoolAttribute('usePhoneBigram', True)

# Use TTS Relay for voice. Set the voice code
#rachel.setVoice('remote')
#rachel.setVoiceCode('Microsoft|Zira|Desktop')

# Use pre-recorded audio files for voice
rachel.setStringAttribute("voice", "audiofile")
rachel.setStringAttribute("voiceCode", ".")

# Set saccade mode for character to talk
bml.execBML('*', '<saccade mode="talk"/>')

# Add pawns in scene for character gaze
gazeTarget = scene.createPawn('gazeTarget')
gazeTarget.setPosition(SrVec(4, 1.58, 1.5))		# Set gaze right

# Setup character gestures, body posture, and gaze target
scene.run('BehaviorSetGestures.py')
setupBehaviorSet()
retargetBehaviorSet('ChrRachel')
bml.execBML('ChrRachel', '<body posture="ChrBrad@Idle01"/>')
bml.execBML('ChrRachel', '<gaze sbm:joint-range="EYES CHEST" target="gazeTarget"/>')


####################################################
#                                                  #
#                       MAIN                       #
#                                                  #
####################################################


# Open the input file generated from the script
file_path = r'C:\MusicGlove\musicglove_1366x768\resources\saves\temp\RIVA_log.txt'

# Global variables to control character timing in the Update script
last = 0
delay = 5					# Seconds between when script will check MusicGlove CSV for new text

move_gaze = False 			# When true, continue moving the gaze
gaze_direction = 'right'	# Gaze direction defaulted to right
gazeX = 4 					# x-coord of gaze
dirX = 1   					# Value to increment/decrement x-coord of gaze (1 or -1)
turn_speed = 0.07 			# Speed to turn gaze

# Default x-coord gaze values
forward_gaze = 0.04
right_gaze = 4
left_gaze = -4

end = 0 					# Time before turning back away from the user
turn = 0 					# Randomly determines whether or not to turn towards the user when speaking
							# Will always turn towards the user on the first go, as it is set to 0 and the condition
								# is turn <= 5

previous = 'Intro_str'

class VirtualAssistant(SBScript):
	def update(self, time):
		global last, delay, end, turn
		global move_gaze, gazeX, dirX, turn_speed
		global forward_gaze, right_gaze, left_gaze, gaze_direction
		global previous

		diff = time - last

		# Responsible for character movements
		if move_gaze:
			if gaze_direction == 'right':		# move her towards forward
				if turn <= 5:					# make this random so she doesn't always turn towards user (Currently 50/50 chance)
					if gazeX > forward_gaze:
						dirX = -1
					elif gazeX <= forward_gaze:
						gaze_direction = 'forward'
						end = int(time) + 5 	# change this depending on how long it takes to speak a sentence
						turn = randrange(10)
						move_gaze = False
					gazeX = gazeX + turn_speed * dirX
					gazeTarget.setPosition(SrVec(gazeX, 1.58, 1.5))
				else:
					turn = randrange(10)
					move_gaze = False
		if gaze_direction == 'forward':			# move her towards right
			if int(time) > end:
				move_gaze = True
				if gazeX < right_gaze:
					dirX = 1
				elif gazeX > right_gaze:
					move_gaze = False
					gaze_direction = 'right'
				gazeX = gazeX + turn_speed * dirX
				gazeTarget.setPosition(SrVec(gazeX, 1.58, 1.5))

		# Check if CSV file has new line of output to speak. If not, do not do anything.
		if diff >= delay:
			with io.open(file_path, 'r') as f:
				line = f.readline()
			if previous not in line:
				move_gaze = True
				line = line.split(":")
				speak_wav(str(line[-1]))			# based on current format of csv file
				gesture()
				last = time
				previous = str(line[-1])


def speak_tts(sentence):
	'''
	Constructs the BML to make the virtual character speak the given sentence (string)
	'''
	# Happy Expression
	bml.execBML('ChrRachel', '<face type="facs" au="6" amount="1"/><face type="facs" au="12" amount="1"/>')
	# speak template: bml.execBML('ChrRachel', '<speech type="text/plain">' + sentence + '</speech>')
	bml.execBML('ChrRachel', '<speech type="text/plain">' + sentence + '</speech>')


def speak_wav(response):
	'''
	Executes the correct prerecorded voice file
	'''
	# Happy Expression
	bml.execBML('ChrRachel', '<face type="facs" au="6" amount="1"/><face type="facs" au="12" amount="1"/>')
	# example: bml.execBML('ChrRachel', '<speech ref="NEG_TRAINING_RESPONSE_0_Blue"/>')
	bml.execBML('ChrRachel', '<speech ref="' + response + '"/>')

'''
def speakWithFeedBack(sentence, positive_or_negative):
	if happy:
		# Happy Expression
		bml.execBML('ChrRachel', '<face type="facs" au="6" amount="1"/><face type="facs" au="12" amount="1"/>')
	# speak template: bml.execBML('ChrRachel', '<speech type="text/plain">' + sentence + '</speech>')
	bml.execBML('ChrRachel', '<speech type="text/plain">' + sentence + '</speech>')
'''

def gesture():
	'''
	Randomly executes a gesture for the character when called
	* Gestures chosen randomly.
	* All gestures can be found in "data\behaviorsets\Gestures2\motions"
	* There are gestures that can be associated with positive and negative behavior:
		If in the future, can add another csv output indicating positive or negative
		feedback, and play a random behavior that is either positive or negative.
		Currently, the motions are generally neutral.
	* TODO: Add a parameter that you can pass in, 0 (positive) or 1 (negative)
	'''
	gesture = randrange(20)		# 13 gestures total. Set range larger so character does not move every time
	if gesture == 0:
		# Offers with left hand
		bml.execBML('ChrRachel', '<animation name="ChrBrad@Idle01_OfferLf01"/>')
	elif gesture == 1:
		# Offers with both hands
		bml.execBML('ChrRachel', '<animation name="ChrBrad@Idle01_OfferBoth01"/>')
	elif gesture == 2:
		# Nod
		bml.execBML('ChrRachel', '<head type="NOD"/>')
	elif gesture == 3:
		# Motions with left hand
		bml.execBML('ChrRachel', '<animation name="ChrBrad@Idle01_YouLf03"/>')
	elif gesture == 4:
		# Raise arm upwards V
		bml.execBML('ChrRachel', '<animation name="ChrBrad@Idle01_ExampleLf01"/>')
	elif gesture == 5:
		# Raises arm
		bml.execBML('ChrRachel', '<animation name="ChrBrad@Idle01_HoweverLf01"/>')
	elif gesture == 6:
		# Both arms raised up
		bml.execBML('ChrRachel', '<animation name="ChrBrad@Idle01_InclusivityPosBt01"/>')
	elif gesture == 7:
		# Indicate towards left with both hands
		bml.execBML('ChrRachel', '<animation name="ChrBrad@Idle01_IndicateLeftBt01"/>')
	elif gesture == 8:
		# Indicates towards left with left hand
		bml.execBML('ChrRachel', '<animation name="ChrBrad@Idle01_IndicateLeftLf01"/>')
	elif gesture == 9:
		# Indicates towards right with both hands
		bml.execBML('ChrRachel', '<animation name="ChrBrad@Idle01_IndicateRightBt01"/>')
	elif gesture == 10:
		# Indicates towards right with right hand
		bml.execBML('ChrRachel', '<animation name="ChrBrad@Idle01_IndicateRightRt01"/>')
	elif gesture == 11:
		# Brings up right hand
		bml.execBML('ChrRachel', '<animation name="ChrBrad@Idle01_ReceiveRt01"/>')
	elif gesture == 12:
		# Motions with left hand
		bml.execBML('ChrRachel', '<animation name="ChrBrad@Idle01_YouLf01"/>')


# START THE PROGRAM -> RUN THE UPDATE SCRIPT
virtualassistant = VirtualAssistant()
scene.addScript('virtualassistant', virtualassistant)
