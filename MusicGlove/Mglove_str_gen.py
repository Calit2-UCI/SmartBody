__author__ = 'Nathan'
### Nathanial Benjamin, UCI, Calit2, CalPlug, 2014-Feb
# Written in Python 3.3.3 (added statistics and pydub modules)
# Altered to Python 2.7 11/May/2015

from random import randrange


'''
Notes:

'''

# Grip list
GRIP_1 = 'Red'
GRIP_2 = 'Blue'
GRIP_3 = 'Green'
GRIP_4 = 'Purple'
GRIP_5 = 'Yellow'
GRIP1 = 'KEY PINCH'
GRIP2 = 'POINTER FINGER'
GRIP3 = 'MIDDLE FINGER'
GRIP4 = 'RING FINGER'
GRIP5 = 'LITTLE FINGER'
'''
GRIP_1 = 'Red Grip'
GRIP_2 = 'Blue Grip'
GRIP_3 = 'Green Grip'
GRIP_4 = 'Purple Grip'
GRIP_5 = 'Yellow Grip'
'''

POSITIVE_STRING = [
    [
        "YOU'RE DOING WELL, BUT I KNOW YOU CAN DO BETTER.",
        "LOOKS LIKE YOU KNOW WHAT YOU'RE DOING. KEEP IT UP!",
        "PRETTY GOOD JOB ON THAT LAST SET, KEEP GOING!",
        "YOU'RE GETTING BETTER, KEEP ON GOING!",
    ],
    [
        "GOOD WORK KEEP IT UP!",
        "THAT LAST SET WAS GOOD WORK!",
        "FINE JOB ON THAT LAST SET.",
        "SOLID WORK, YOU'RE DOING REALLY WELL"
    ],
    [
        "YOU'RE PLAYING AMAZINGLY! EVEN I'M IMPRESSED, AND I'M A ROBOT.",
        "YOU REALIZE YOUR LAST SET WAS PERFECT, RIGHT?",
        "WELL DONE, YOUR RESPONSE TIMES ARE UNCANNILY RAPID.",
        "NOW THAT'S WHAT I CALL ACCURATE!"
    ],
]


NEGATIVE_STRING = [
    [
        "NOT BAD, BUT I'M SURE YOU'LL DO BETTER ON THE NEXT SET.",
        "NOT BAD, BUT YOU CAN DEFINITELY IMPROVE.",
        "THAT LAST SET WAS OK, BUT WE CAN DO BETTER.",
        "JUST A BIT SLOWER BACK THERE, BUT YOU'RE DOING WELL!"
    ],
    [
        "YEAH, THAT LAST SET WAS A BIT OF A TOUGH ONE, LET'S GIVE IT ANOTHER GO.",
        "A BIT SLOW ON THAT LAST SET, BUT WE'RE GETTING BETTER.",
        "JUST A BRIEF HICCUP ON THAT LAST ONE, BUT NOTHING TO WORRY ABOUT, I SHOULD THINK.",
        "THAT LAST SET COULD HAVE GONE A LITTLE BETTER, BUT THAT'S ALRIGHT, WE'LL GET IT NEXT TIME!"
    ],
    [
        "YOU'RE SLOWING DOWN A LITTLE BIT, TRY FOCUSING ON THE POINT WHEN THE BOTTOM OF THE CIRCLE LINES UP WITH THE TARGET!",
        "PHEW, THAT LAST SET REALLY WAS A DOOZY, BUT DON'T WORRY WE'LL GET BACK ON TRACK.",
        "THAT LAST PART WAS PRETTY HARD, DON'T SWEAT IT TOO MUCH THOUGH.",
        "YEAH THOSE LAST FEW MEASURES SCARED ME TOO."
    ],
]

OVERALL_SUMMARY = [
    "Hey, you're doing better on this song than last time!",
    "I've noticed some significant improvement on this particular song. Great work!",
    "you've really got this song down don't you!?"
]

TRAINING_PROMPT_LIST = [
    "So... I noticed on that last playthrough that the {Grip} is a bit off, so let's focus a bit more on that one for now.",
    "You are doing great, but I think we ought to focus on the {Grip} for the next little bit!",
    "On this next set, try focusing on the {Grip}!",
    "I noticed that you were having a little trouble with the {Grip}! Let's work on that one.",
    "Overall, that was a great playthrough, but I noticed you were having trouble with the {Grip}. Why don't we focus on that one for the next few measures?",
    "Great work. We could still do a little more work on the {Grip} though. So Let's try and focus on that for a little bit."
]

POS_TRAINING_RESPONSE = [
    "Wow, great work improving your {Grip}. There's been a pretty nice jump in your response times with that grip.",
    "Hey what did I tell you! Focusing on your {Grip} really paid off. I've noticed a pretty substantial improvement in that grip's response times.",
    "what did I tell ya?! Focusing on the {Grip} really paid off! Great work!"
]

NEG_TRAINING_RESPONSE = [
    "What happened to the {Grip}?! I thought we were going to focus on it this time?",
    "I know you can do better than that! Let's try focusing on the {Grip} again.",
    "I didn't see much improvement on the {Grip} this time. Remember to concentrate on it this next time!"
]

ENCOURAGEMENT_STR_LIST = [
    'You did very well!',
    'Good job on that last set!',
    'You have improved a lot!',
    'Excellent work!',
    'Have you been practicing?!',
    'Keep up the good work!'
]

WORST_GRIP_STR_LIST = [
    "I noticed that you were having a little trouble with the ", #blue grip...for example
    "Next time try focusing on the ",
    "You still need a little more work on the ",
    "On the next song, why don't we focus on the ",
    "We should keep working on the "
]

BEST_GRIP_STR_LIST = [
    "But, I noticed you have improved quite a bit on the", #blue grip...for example
    "Though, You did well on the",
    "Though, You seem quite proficient with the",
    "But, you obviously do not need any more practice on the",
    "But, you are doing great with the"
]

def training_response(last_worst_grip, old_grip_avg, new_grip_avg):
    """ last_worst_grip: int, old_grip_avg: float, new_grip_avg: float
        Takes the worst grip, it's average, and it's average last session. Checks for improvement, then returns a
        2-tuple where the first element is the string type of response and the second is an appropriate string and
        whether the response was positive or negative if there was improvement congratulate them.
        Else recommit them, note that system asked for a given outcome... or simply call training_prompt()?
        pass failure/success to select_response() function
    """
    if old_grip_avg < new_grip_avg:
        return ("training_prompt",
                "NEG_TRAINING_RESPONSE_{}_{}".format(randrange(len(NEG_TRAINING_RESPONSE)),grip_selector(last_worst_grip)))
    return ("training_response",
            "POS_TRAINING_RESPONSE_{}_{}".format(randrange(len(POS_TRAINING_RESPONSE)),
                                                 grip_selector(last_worst_grip)))

def negative_response(scale):
    """ scale: int
        Returns a scaled negative response
    """
    # return NEGATIVE_STRING[scale-1][randrange(len(NEGATIVE_STRING[scale-1]))]
    return "NEGATIVE_STRING_{}_{}".format((scale-1),randrange(len(NEGATIVE_STRING[scale-1])))


def positive_response(scale):
    """ scale: int
        Returns a scaled positive response
    """
    # return POSITIVE_STRING[scale-1][randrange(len(POSITIVE_STRING[scale-1]))]
    return "POSITIVE_STRING_{}_{}".format((scale-1),randrange(len(POSITIVE_STRING[scale-1])))


def training_prompt(last_worst_grip):
    """ last_worst_grip: int
        Takes a worst grip and provides a string prompting user to improve that grip
    """
    # prompt = TRAINING_PROMPT_LIST[randrange(len(TRAINING_PROMPT_LIST))].format(Grip = grip_selector(last_worst_grip))
    # print(prompt)
    prompt = "TRAINING_PROMPT_LIST_{}_{}".format(randrange(len(TRAINING_PROMPT_LIST)),
                                                 grip_selector(last_worst_grip))
    return prompt


def grip_avg_summary_str(grip_avg_list):
    """ grip_avg_list: list
        Returns a string showing the average times for all grips (includes grips that may have been unused this song)
    """
    return "Red Grip avg: {}; Blue Grip avg: {};Green Grip avg: {}; Purple Grip avg: {}; Yellow Grip avg: {}".format(
        grip_avg_list[0], grip_avg_list[1], grip_avg_list[2], grip_avg_list[3], grip_avg_list[4])


def encouraging_str_generator():
    """ Make an encouraging statement
    """
    return ENCOURAGEMENT_STR_LIST[randrange(len(ENCOURAGEMENT_STR_LIST))]


def worst_grip_str_generator(worst_grip):
    """ worst_grip: int
        Join an encouragement string with an appropriate worst grip string"""
    grip_string = ('{} {}.'.format(WORST_GRIP_STR_LIST[randrange(len(WORST_GRIP_STR_LIST))], grip_selector(worst_grip)))
    return '{} {} {}'.format(encouraging_str_generator(), WORST_GRIP_STR_LIST[randrange(len(
        WORST_GRIP_STR_LIST))], grip_selector(worst_grip))


def grip_selector(grip):
    """ grip: int
        Returns the string representation of the grip's color corresponding to the grip number of(grip)
    """
    if grip == 1:
        return GRIP_1
    elif grip == 2:
        return GRIP_2
    elif grip == 3:
        return GRIP_3
    elif grip == 4:
        return GRIP_4
    elif grip == 5:
        return GRIP_5
    elif grip == 0:
        return 'hello'


def summary_generator(worst_grip, best_grip):
    """ worst_grip,best_grip: int
        Returns 3 sentences: an encouragement_str, worst_grip_str, best_grip_str
    """
    #print("Entering summary_generator()")
    # Original summary return replaced with overall summary #3 for the demo, as .wav concatenation is not finished yet.
    '''
    return '{}... {} {}!'.format(worst_grip_str_generator(worst_grip),
                            BEST_GRIP_STR_LIST[randrange(len(BEST_GRIP_STR_LIST))],
                            grip_selector(best_grip))
    '''
    return "OVERALL_SUMMARY_2"


###Depreciated Function
def RIVA_translator(msg_number, worst_grip, best_grip, RIVA_direc, message=''):
    """ msg_number, worst_grip, best_grip: int
        RIVA_direc, message: str
        Takes a generated feedback string, prepends number for RIVA's facial generator
        RIVA_direc may be added later to inform which side of the screen the virtual agent should face.
    """
    ###Depreciated Function
    return 'Iteration:{};Expression:1;TTS:{}'.format(str(msg_number), message) # Add RIVA_direc to the returned string


def emo_less_feedback(msg_num, worst_grip, best_grip=0):
    """ msg_number, worst_grip, best_grip: int
        Takes a worst grip and optional best grip, and returns an emotionless string representation
    """
    result = ["Worst Grip = " + grip_selector(worst_grip)]
    if best_grip != 0:
        result.append("Best Grip = " + grip_selector(best_grip))
    else:
        result.append('')
    return "NewData:{};TTS:{}\n{}".format(msg_num,result[0],result[1])


if __name__ == '__main__':
    print("To run experiments please run 'RIVA_Main.py'")
    print('RIVA_translator() = ',RIVA_translator(1,3,0))
    print('RIVA_translator() = ',RIVA_translator(2,1,5))
    print('emo_less_feedback() = ',emo_less_feedback(3,2))
    print('emo_less_feedback() = ',emo_less_feedback(1,5,4))
    print('summary_generator() = ',summary_generator(1,2))
    print('summary_generator() = ',summary_generator(4,1))
    print('summary_generator() = ',summary_generator(5,3))
    print('summary_generator() = ',summary_generator(2,5))
    print('summary_generator() = ',summary_generator(3,4))
    print("To run experiments please run 'RIVA_Main.py'")
