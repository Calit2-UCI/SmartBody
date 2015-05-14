####################################################
#                                                  #
#                  SmartBody RIVA                  #
#                                                  #
# Stephanie Chang - Calit2 Dev 2014-2015           #
#   Python 2.7.3                                   #
####################################################

import io
import time as systime
from random import randrange

print "|--------------------------------------------|"
print "|        Starting VirtualAssistant           |"
print "|--------------------------------------------|"

# Setup SmartBody Character
scene.run('setup-character.py')

######################################################
#                                                    #
#                        MAIN                        #
#                                                    #
######################################################

# Open the input file generated from the script
file_path = r'D:\RIVA\musicglove_1366x768\resources\saves\temp\RIVA_log.txt'
input_file = io.open(file_path, 'r')

# Global variables to control character timing in the Update script
last = 0
delay = 5					# Seconds between when script will check Music Glove CSV for new line

move_gaze = False 			# When true, continue moving the gaze
gaze_direction = 'forward'	# Gaze direction defaulted to right
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
				if turn <= 3:					# make this random so she doesn't always turn towards user (Currently 50/50 chance)
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
			#input_file = io.open(file_path, 'r')
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
