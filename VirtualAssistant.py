####################################################
#                                                  #
#                  SmartBody RIVA                  #
#                                                  #
# Stephanie Chang - Calit2 Dev 2014-2015           #
#   Python 2.7.3                                   #
####################################################

import contextlib
import io
import wave
from random import randrange
from threading import Thread

print "|--------------------------------------------|"
print "|        Starting VirtualAssistant           |"
print "|--------------------------------------------|"

######################################################
#                                                    #
#                        SETUP                       #
#                                                    #
######################################################

# Add asset paths
scene.addAssetPath('script', 'scripts')
scene.addAssetPath('mesh', 'mesh')
scene.addAssetPath('motion', 'ChrRachel')
scene.addAssetPath('script', 'behaviorsets')
scene.addAssetPath('audio', 'speech')
scene.addAssetPath('script', 'MusicGlove')
scene.loadAssets()

# Setup SmartBody Character
scene.run('setup-character.py')

# Add pawns in scene for character gaze
gazeTarget = scene.createPawn('gazeTarget')
gazeTarget.setPosition(SrVec(0.03, 1.58, 1.5))		# set right
bml.execBML('ChrRachel', '<gaze sbm:joint-range="EYES CHEST" target="gazeTarget"/>')

######################################################
#                                                    #
#                        MAIN                        #
#                                                    #
######################################################

# Open the input file generated from the script
file_path = r'D:\RIVA\musicglove_1366x768\resources\saves\temp\RIVA_log.txt'
input_file = io.open(file_path, 'r')

# Default x-coord gaze values
forward_gaze = 0.04
right_gaze = 4
left_gaze = -4

class VirtualAssistant(SBScript):

	# Control character action timing
	last = 0
	delay = 0						# Seconds between when script will check Music Glove CSV for new line

	introduction = True         	# Check if introduction should be spoken
        move_allowed = True
	move_gaze = False 				# When true, continue moving the gaze
	gaze_direction = 'right'		# Gaze direction defaulted towards the right
	gazeX = forward_gaze			# x-coord of gaze
	dirX = 1  						# Value to increment/decrement x-coord of gaze (1 or -1)
	turn_speed = 0.07 				# Speed to turn gaze

	end = 0 						# Time before turning back away from the user
	turn = 0 						# Randomly determines whether or not to turn towards the user when speaking
									# Will always turn towards the user at first, as the condition is turn <= 5
	previous_wav = 'Welcome_str'	# Keep track of previously spoken wav file name
	wav_duration = 7            	# Duration of Welcome_str

	def speak_wav(self, response):
            '''
            Executes the given prerecorded voice file
            '''
            # Happy Expression
            bml.execBML('ChrRachel', '<face type="facs" au="6" amount="1"/><face type="facs" au="12" amount="1"/>')
            # example: bml.execBML('ChrRachel', '<speech ref="NEG_TRAINING_RESPONSE_0_Blue"/>')
            bml.execBML('ChrRachel', '<speech ref="' + response + '"/>')

	def gesture(self):
            '''
            Randomly executes a gesture for the character
            * Gestures chosen randomly from neutral motions
            * All gestures can be found in "data\behaviorsets\Gestures2\motions"
            * TODO: Gesture based on positive/negative feedback
            '''
            # 12 gestures
            gesture_list = ["ChrBrad@Idle01_OfferLf01", "ChrBrad@Idle01_OfferBoth01",
                            "ChrBrad@Idle01_YouLf03", "ChrBrad@Idle01_ExampleLf01",
                            "ChrBrad@Idle01_HoweverLf01", "ChrBrad@Idle01_InclusivityPosBt01",
                            "ChrBrad@Idle01_IndicateLeftBt01", "ChrBrad@Idle01_IndicateLeftLf01",
                            "ChrBrad@Idle01_IndicateRightBt01", "ChrBrad@Idle01_IndicateRightRt01",
                            "ChrBrad@Idle01_ReceiveRt01", "ChrBrad@Idle01_YouLf01"]

            gesture_index = randrange(20)		# Range is larger than number of gestures so character does not move every time

            if gesture_index < 12:
                bml.execBML('ChrRachel', '<animation name="' + gesture_list[gesture_index] + '"/>')

	def read_csv(self):
            '''
            Read the contents of the CSV file and return the wav file to speak
            '''
            with io.open(file_path, 'r') as f:
                    line = f.readline()
            line = line.split(":")
            wav = str(line[-1])
            wav_file = 'D:\\RIVA\\SmartBody\\data\\speech\\'
            if wav != '':
                with contextlib.closing(wave.open(wav_file + wav + '.wav', 'r')) as f:
                    self.wav_duration = f.getnframes() / float(f.getframerate())
                    return wav
            else:
                self.move_allowed = False

        def move_character(self, time):
            '''
            Move the avatar appropriately between gaze directions
            '''
            if self.move_allowed:
                if self.move_gaze:
                        if self.gaze_direction == 'right':		# move her towards forward
                                if self.turn <= 7:					# make this random so she doesn't always turn towards user
                                        if self.gazeX > forward_gaze:
                                                self.dirX = -1
                                        elif self.gazeX <= forward_gaze:
                                                self.gaze_direction = 'forward'
                                                self.end = int(time) + self.wav_duration + 1	# change this depending on how long it takes to speak a sentence
                                                self.turn = randrange(10)
                                                self.move_gaze = False
                                        self.gazeX = self.gazeX + self.turn_speed * self.dirX
                                        gazeTarget.setPosition(SrVec(self.gazeX, 1.58, 1.5))
                                else:
                                        self.turn = randrange(10)
                                        self.move_gaze = False
                if self.gaze_direction == 'forward':			# move her towards right
                        if int(time) > self.end:
                                self.move_gaze = True
                                if self.gazeX < right_gaze:
                                        self.dirX = 1
                                elif self.gazeX > right_gaze:
                                        self.move_gaze = False
                                        self.gaze_direction = 'right'
                                self.gazeX = self.gazeX + self.turn_speed * self.dirX
                                gazeTarget.setPosition(SrVec(self.gazeX, 1.58, 1.5))

	def update(self, time):

            diff = time - self.last

            self.move_character(time)

            if self.introduction:
                    self.delay = 15
                    wav = self.read_csv()
            else:
                    self.delay = 5

            # Check if CSV file has new line of output to speak. If not, do not do anything.
            if diff >= self.delay:
                try:
                    if self.introduction:
                        self.speak_wav(wav)
                        self.introduction = False
                    else:
                        wav = self.read_csv()

                        if wav != self.previous_wav and wav != '':
                            self.move_gaze = True
                            self.speak_wav(wav)
                            self.gesture()
                            self.last = time
                            self.previous_wav = wav
                except TypeError:
                    pass

def songLoop():
        scene.run('RIVA_Main.py')

# Call MusicGlove Script
thread = Thread(target = songLoop)
thread.daemon = True            # die when the main thread dies
thread.start()

# START THE PROGRAM -> RUN THE UPDATE SCRIPT
virtualassistant = VirtualAssistant()
scene.addScript('virtualassistant', virtualassistant)
