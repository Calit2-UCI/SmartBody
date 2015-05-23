__author__ = 'Nathan'
### Nathanial Benjamin, UCI, Calit2, CalPlug, 2014-Feb
# Written in Python 3.3.3 (added statistics and pydub modules)
# Altered to Python 2.7 11/May/2015

### - Hard-coded end of song summary to overall_summary #3. for the demo, as .wav concatenation is not finished yet.
### - Took name out of intro sentances for demo. for the demo, as TTS on-the-fly is not finished yet.


######################################################
#                                                    #
#                       MAIN                         #
#                                                    #
######################################################
import sys
sys.path.append("D:\RIVA\SmartBody\data\MusicGlove")

import CSV_functions
import Mglove_str_gen
from CSV_functions import read_csv, make_csv
from Interface import gather_info, parse_csv, evaluate_worst_grip, evaluate_best_grip, what_song, \
    grip_times, abs_val_list
from Mglove_str_gen import grip_avg_summary_str, summary_generator, emo_less_feedback
from Send_to_voice_server import reset_RIVA_log, text_to_RIVA, to_no_voice_log
from time import sleep, strftime
from user_stats import User_Stats

'''
    -Fix selector to prioritize training prompts
'''
SONG_OVER_CHECK_TIME = 10
TIME_BETWEEN_FEEDBACK = 30        # Must be a multiple of SONG_OVER_CHECK_TIME


class MusicGloveSong:

    def __init__(self, user, restart=False):
        self. _feedback_plat = 'RIVA'   # possible choices: RIVA, iSpeech, and Text
        self. _grip_count = 0
        self. _last_line = self._read_lastline()
        self. _last_30_sec = []
        self. _csv_result = []
        self. _song_over = True
        self. _last_worst_grip = 1
        self. _RIVA_message_num = 0
        self. _last_response = ''
        self. _all_grips = []
        self.user_stats = 'null'
        # tells RIVA which side of it's screen the Musicglove screen is on
        self._RIVA_focus_direction = 'right'
        self.user_name = user   # input("Please enter user name: ")
        if restart == True:
            self.user_stats = User_Stats(neg_quart=25, pos_quart=25, new_song=False)
        else:
            self.user_stats = User_Stats()
        reset_RIVA_log()
        pass

    def _check_completion(self):
        """ waits 7 seconds then check if lastline matches past iteration's lastline
        """
        sleep(SONG_OVER_CHECK_TIME)        ###Wait 10 seconds
        #print("entering _check_completion")
        csv_lastline = self._read_lastline()
        #print('system time = {}'.format(strftime("%H:%M:%S")))
        #print("csv_lastline = ", csv_lastline)
        #print("self._last_line = ", self._last_line)
        if csv_lastline == self._last_line or csv_lastline == "Empty File":
            self._song_over = True
            print("Song Over")
        else:
            self._last_line = csv_lastline
            self._song_over = False
        #print("Song Over = ", self._song_over)
        #print('system time = {}'.format(strftime("%H:%M:%S")))
        #print("self._last_line = ", self._last_line)
        return

    def _summarize_period(self):
        """ Call time_5_sec() 6 times, if the song ends return immediately,
            otherwise return once iterations are complete.
        """
        #print("entering _summarize_period()")
        for i in range(TIME_BETWEEN_FEEDBACK // SONG_OVER_CHECK_TIME):    ### Wait 30 seconds
            self._check_completion()
            if self._song_over is True:
                break
        self._set_last_30_sec()
        return

    def _set_last_30_sec(self):
        """ sets the grip list for the past 30 seconds of the song
        """
        #print("entering set_last_30")
        grip_list = read_csv(CSV_functions.MUSICGLOVE, test=True)
        self._all_grips = parse_csv(grip_list)
        #print("grip_list = ", grip_list)
        if self._grip_count == 0:
            self._grip_count = len(grip_list)
        else:
            for j in range(self._grip_count):
                #print("j = {} and grip_list = {}".format(j, len(grip_list)))
                grip_list.remove(grip_list[0])
            self._grip_count += len(grip_list)
            #self._all_grips += parse_csv(read_csv(CSV_functions.MUSICGLOVE))
        self._last_30_sec = grip_list
        return

    def _read_lastline(self):
        """ Returns the last line of the csv containing the user's grip information
        """
        #print("entering _read_lastline()")
        #print(read_csv(CSV_functions.MUSICGLOVE))
        try:
            last_line = parse_csv(read_csv(CSV_functions.MUSICGLOVE))[-1]
        except IndexError:
            return "Empty File"
        return last_line

    def _compile_result(self, summary):
        """ summary: str
            Extends the result that will be added to the log.csv
        """
        #print("entering _compile_result()")
        self._csv_result.append(summary)
        return

    def select_response(self):
        """ Chooses an appropriate response based upon user's performance. Returns a
        2-tuple where the first element is the string type of response and the second is that appropriate response string"""
        #print("RIVA msg number: ", self._RIVA_message_num)
        overall_avg = self.user_stats.new_overall_avg()
        scale_points = self.user_stats.get_scale_points(abs_val_list(grip_times(self._all_grips)))
        #print("overall avg: {}\n scale point 1: {} scale point 2: {}".format(overall_avg,scale_points[1],scale_points[2]))
        # if self._RIVA_message_num == 1:
        #     return self.response_welcome()
        if self._last_response == "training_prompt":
            return self.response_training_response()
            '''elif self.user_stats.get_grip_avg(grip_number=self._last_worst_grip) > \
                     self.user_stats.get_scale_points(abs_val_list(grip_times(self._all_grips)))[2]:
                return self.response_training_prompt()
            '''
        elif overall_avg > scale_points[2]:
            #print("Q2", scale_points[2])
            return self.response_negative()
        elif overall_avg < scale_points[1]:
            #print("Q1", scale_points[1])
            return self.response_positive()
        return self.response_training_prompt()

    def response_welcome(self):
        """ Returns a welcome string for the user, including their name, giving the system a chance to analyze their
            skill
        """
        self._last_response = "Welcome"
        self._last_worst_grip = 0
        ### return "Alright " + self.user_name + ", are you ready to really get started!?"
        return "Welcome_str"

    def response_training_response(self):
        """ Analyzes the user's performance on a given grip, returns a string appropriate to their success/failure"""
        training_response = Mglove_str_gen.training_response(
            self.user_stats.get_followup(),
            self.user_stats.get_grip_avg(grip_number=self.user_stats.get_followup(), old=True),
            self.user_stats.get_grip_avg(grip_number=self.user_stats.get_followup()))
        self._last_response = training_response[0]
        return training_response[1]

    def response_training_prompt(self):
        """ Analyzes user's last 30 seconds, returns string prompt suggesting a grip to work on (the worst grip)"""
        self._last_response = "training_prompt"
        #print("Training Prompt")
        self.user_stats.set_followup(self._last_worst_grip)
        return Mglove_str_gen.training_prompt(self.user_stats.get_followup())

    def response_negative(self):
        """ Returns a scaled string telling the user they need to improve their overall reaction time"""
        #print("Negative Response")
        self._last_response = "negative_response"
        #print("scale = ", self.user_stats.find_worst_grip_scale(grip_times(self._all_grips)))
        return Mglove_str_gen.negative_response(self.user_stats.find_worst_grip_scale(grip_times(self._all_grips)))

    def response_positive(self):
        """ Returns a scaled string telling the user that their overall reaction time is good/great"""
        self._last_response = "positive_response"
        #print("Positive Response")
        #print("scale =", self.user_stats.find_best_grip_scale(grip_times(self._all_grips)))
        return Mglove_str_gen.positive_response(self.user_stats.find_best_grip_scale(grip_times(self._all_grips)))

    def test_for_restart(self):
        """ Tests whether the a new song has been started
        """
        #print("entering test_for_restart()")
        self._compile_result("UserName: " + self.user_name)
        msg = "Welcome_str"
        if self._feedback_plat == "RIVA":
            self._RIVA_message_num += 1
            text_to_RIVA(msg)
        else:# self._feedback_plat == "Text":
            self._RIVA_message_num += 1
            to_no_voice_log("NewData:{};TTS:{}".format(self._RIVA_message_num, msg))
        ###else:
        ###    text_to_ispeech(ispeech_formatter(msg))
        while True:
            self._check_completion()
            if self._song_over is False:
                #print("Song Started")
                if self._feedback_plat == "RIVA":
                    reset_RIVA_log()
                    self._RIVA_message_num += 1
                    text_to_RIVA(self.response_welcome())
                elif self._feedback_plat == "Text":
                    to_no_voice_log((emo_less_feedback(0, 0, 0)))
                self.execute_song()
                #print("Re-entered Test_for_restart()")
                if self._song_over is True:
                    interface_info = gather_info(
                        parse_csv(read_csv(CSV_functions.MUSICGLOVE)))
                    #print(interface_info)
                    #print("Song_over min/max = ", min_max)
                    self.user_stats.set_grips(interface_info)
                    self._compile_result(grip_avg_summary_str(interface_info))
                    evaluated_info = [evaluate_worst_grip(interface_info, self._last_worst_grip),
                                      evaluate_best_grip(interface_info)]
                    summary = summary_generator(evaluated_info[0], evaluated_info[1])
                    if self._feedback_plat == "RIVA":
                        self._RIVA_message_num += 1
                        #print("message_num={} summary={}".format(self._message_num, summary))
                        text_to_RIVA(summary)
                    else:# self._feedback_plat == "Text":
                        to_no_voice_log(emo_less_feedback(self._RIVA_message_num, evaluated_info[0], evaluated_info[1]))
                    ###else:
                    ###    text_to_ispeech(ispeech_formatter(summary))
                    self._last_30_sec = []
                    self._compile_result(summary)
                    self._csv_result.extend(read_csv(CSV_functions.MUSICGLOVE))
                    make_csv(self._csv_result, CSV_functions.M_GLOVE_SUMMARIES, what_song(self._grip_count))
                    self.__init__(self.user_name, restart=True)
                    self._RIVA_message_num = 1
            else:
                pass
        return

    def execute_song(self):
        """ organizes methods, and runs a song
        """
        #print("entering execute_song()")
        while self._song_over is False:
            self._summarize_period()
            grip_info = gather_info(parse_csv(self._last_30_sec))
            self.user_stats.set_grips(grip_info)
            best_grip = evaluate_best_grip(grip_info)
            self._compile_result(grip_avg_summary_str(grip_info))
            self._last_worst_grip = evaluate_worst_grip(grip_info, self._last_worst_grip)
            summary = self.select_response()
            self._compile_result(summary)
            self._compile_result('system time = {}'.format(strftime("%H:%M:%S")))
            self._compile_result(' ')
            if self._song_over is True:
                # print('Number of grips this song = ', self._grip_count)
                return
            if self._feedback_plat == "RIVA":
                self._RIVA_message_num += 1
                text_to_RIVA(summary)
            else:#if self._feedback_plat == "Text":
                self._RIVA_message_num += 1
                to_no_voice_log(emo_less_feedback(self._RIVA_message_num, self._last_worst_grip, best_grip))
            ###else:
            ###    self._RIVA_message_num += 1
            ###    text_to_ispeech(ispeech_formatter(summary))
        #print("leaving execute_song()")
        return

if __name__ == "__main__":
    MusicGloveSong(user=raw_input("Please enter user name: ")).test_for_restart()
