__author__ = 'Nathan'
### Nathanial Benjamin, UCI, Calit2, CalPlug, 2014-Feb
# Written in Python 3.3.3 (added statistics and pydub modules)
# Altered to Python 2.7 11/May/2015 (removed all iSpeech related functions, as they have a pydub dependancy and
#   pydub is a python 3.3+ supported library)


### RIVA log file
RIVA_LOG = "C:\\Users\\Stephanie\\Desktop\\RIVA\\Log\\RIVA_log.txt"
NO_VOICE_LOG = "D:\\RIVA\\musicglove_1366x768\\resources\\saves\\temp\\NORIVA_log.txt"         # (local computer)


def reset_RIVA_log():
    """ Clears The RIVA_LOG File """
    #print("entering reset_RIVA_log")
    with open(RIVA_LOG, 'w') as file:
        file.write('')


def text_to_RIVA(*args):
    """ Takes an undefined number of audio file names, and formats them to be concatenated by VirtualAssistant.py script
    """
    RIVA_message = ''
    for msg in args:
        if len(RIVA_message) < 1:
            RIVA_message += msg
        else:
            RIVA_message += ";" + msg
    print(RIVA_message)
    with open(RIVA_LOG, 'w') as outfile:
        outfile.write(RIVA_message)


def to_no_voice_log(message):
    """ Takes a message string, then sends it to Musicglove's logfile
    """
    #print("entering to_no_voice_log")
    with open(NO_VOICE_LOG, 'w') as outfile:
        outfile.write(message)
        #print(message)


if __name__ == '__main__':
    print("To run experiments please run 'RIVA_Main.py'")
    test = 'Keep up the good work! I noticed that you were having a little trouble with the Blue Grip. But I also noticed you have improved quite a bit on the Yellow Grip!'
    print(test)
    print("To run experiments please run 'RIVA_Main.py'")