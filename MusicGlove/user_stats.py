__author__ = 'Nathan'
### Nathanial Benjamin, UCI, Calit2, CalPlug, 2014-Feb
# Written in Python 3.3.3 (added statistics and pydub modules)

### if overall avg <0 tell user they're reacting too early
### if overall avg >0 tell user they're reacting too late
''' When we do training vs neg/pos
    how do we implement the scale?
'''

from Interface import gather_info, parse_csv, abs_val_list
from collections import namedtuple

Difference = namedtuple('Difference', 'red blue green purple yellow')

class User_Stats:
    def __init__(self, neg_quart=25, pos_quart=25, new_song=False):
        self.negative_quartile_range = neg_quart
        self.positive_quartile_range = pos_quart
        self._old_red_avg = 0
        self._old_blue_avg = 0
        self._old_green_avg = 0
        self._old_purple_avg = 0
        self._old_yellow_avg = 0
        self._old_overall_avg = 0
        self._red_avg = 0
        self._blue_avg = 0
        self._green_avg = 0
        self._purple_avg = 0
        self._yellow_avg = 0
        self._overall_avg = 0
        self._difference = Difference(0,0,0,0,0)
        self._followup = None        # The grip which the user was last assigned to concentrate on.
        if new_song == True:
            self.set_quartile_ranges()
        pass

    def set_quartile_ranges(self):
        """ Updates the upper and lower quartile ranges. input should be the size of range required:
                i.e. if you want to use the entire range over 75% you would enter 25 for positive feedback (75-100%)
        """
        self.positive_quartile_range = int(input("Please enter the percentage range for RIVA's positive feedback: "))
        self.negative_quartile_range = int(input("Please enter the percentage range for RIVA's negative feedback: "))

    def get_negative_quartile_range(self):
        return self.negative_quartile_range

    def positive_quartile_range(self):
        return self.positive_quartile_range

    def set_grips(self, grips) :
        """ Updates old grips to those from the last call,
                and sets the new grip averages to match those since the last call.
        """
        #print("entering set_grips")
        self._old_red_avg = self._red_avg
        self._old_blue_avg = self._blue_avg
        self._old_green_avg = self._green_avg
        self._old_purple_avg = self._purple_avg
        self._old_yellow_avg = self._yellow_avg
        self._red_avg = grips[0]
        self._blue_avg = grips[1]
        self._green_avg = grips[2]
        self._purple_avg = grips[3]
        self._yellow_avg = grips[4]
        self.set_difference()
        self.set_overall_avg()

    def get_grip_avg(self, grip_number=0, grip=None, old=False):
        """ Takes an int (1-5), or a string ('worst' or 'best'), representing a grip and returns that grip's average"""
        #print("entering get_grip_avg()")
        avgs = [self._red_avg, self._blue_avg, self._green_avg, self._purple_avg, self._yellow_avg]
        if old == True:
            avgs = [self._old_red_avg, self._old_blue_avg, self._old_green_avg,
                    self._old_purple_avg, self._old_yellow_avg]
        if grip_number != 0:
            #print("grip_number = ", grip_number)
            for i in range(5):
                if i == grip_number-1:
                    #print("grip_number = ", grip_number)
                    #print("avgs[{}] = {}".format(i+1,avgs[i]))
                    return avgs[i]
        elif grip == "best":
            return min(avgs)
        return max(avgs)

    def new_overall_avg(self):
        """ Calculates the new_overall average
        """
        #print("entering _overall_avg")
        sum = (self._red_avg+self._green_avg+self._blue_avg+self._purple_avg+self._yellow_avg)
        if sum == 0:
            return 0
        return sum / 5

    def set_overall_avg(self):
        """ Updates old to match the overall average from the last call, and new overall average to match this call.
        """
        #print("entering set_overall_avg")
        self._old_overall_avg = self._overall_avg
        self._overall_avg = (self._overall_avg + self.new_overall_avg())/2
        #print("in set_overall_avg: overall avg = ", self._overall_avg)

    def get_overall_avg(self):
        return self._overall_avg

    def get_old_overall_avg(self):
        return self._old_overall_avg

    def set_followup(self, grip) :
        self._followup = grip

    def get_followup(self):
        return self._followup

    def set_difference(self):
        """ Sets the difference tuple to show the  average error difference between the past 30 seconds and the current
            30 seconds
        """
        #print("entering set_difference")
        self._difference = Difference(abs(self._old_red_avg) - abs(self._red_avg),
                                     abs(self._old_blue_avg) - abs(self._blue_avg),
                                     abs(self._old_green_avg) - abs(self._green_avg),
                                     abs(self._old_purple_avg) - abs(self._purple_avg),
                                     abs(self._old_yellow_avg) - abs(self._yellow_avg))

    def get_difference(self):
        return self._difference

    def quartiles(self, qlist) :
        qlist.sort()
        q1 = qlist[int(len(qlist)/100) * self.negative_quartile_range]
        q2 = qlist[int((len(qlist)/100) * (100 - self.positive_quartile_range))]
        return [q1,q2]

    def get_scale_points(self, userList) :
        """Returns a list of four points which represent the boundaries of the user scale"""
        #print("userList = ", userList)
        sortedList = sorted(userList)

        if len(sortedList) == 0:            # if the list is empty
            #print("empty grip list in get_scale_points()")
            return [0,0,0,0]
        IQR = self.quartiles(sortedList)
        minimum = sortedList[0]
        maximum = sortedList[len(sortedList)-1]
        print('In get_scale_points(), Minimum = {} Q1 = {} Q2 = {} Maximum = {}'.format(minimum,IQR[0],
                                                                                        IQR[1], maximum))
        pointsList = [minimum, IQR[0], IQR[1], maximum]
        return pointsList

    def find_worst_grip_scale(self, grip_list):
        """ Finds the worst grip's value level for the previous 30 second block.
        """
        sortedList = sorted(abs_val_list(grip_list))
        scale = self.get_scale_points(sortedList)
        temp_list = []
        for i in sortedList:
            if scale[2] <= i <= scale[3]:
                temp_list.append(i)
        #print("scale is between {} and {}".format(scale[2], scale[3]))
        #print("over_all_avg = ", self.new_overall_avg())
        scale = self.get_scale_points(temp_list)
        if scale[2] <= self.new_overall_avg() <= scale[3]:
            return 1
        elif scale[1] <= self.new_overall_avg() <= scale[2]:
            return 2
        return 3

    def find_best_grip_scale(self, grip_list):
        """ Finds the positive value level for the previous 30 second block.
        """
        sortedList = sorted(abs_val_list(grip_list))
        scale = self.get_scale_points(sortedList)
        temp_list = []
        for i in sortedList:
            if scale[0] <= i <= scale[1]:
                temp_list.append(i)
        #print("scale is between {} and {}".format(scale[0], scale[1]))
        #print("over_all_avg = ", self.new_overall_avg())
        scale = self.get_scale_points(temp_list)
        if scale[2] <= self.new_overall_avg() <= scale[3]:
            return 3
        elif scale[1] <= self.new_overall_avg() <= scale[2]:
            return 2
        return 1


if __name__ == '__main__':
    print("To run experiments please run 'RIVA_Main.py'")
    test_csv = [['1', '1', '-1'], ['4', '4', '-4'], ['3', '3', '-3'],
                ['3', '3', '3'], ['3', '3', '3'], ['2', '2', '2'],
                ['2', '2', '2'], ['3', '3', '3'], ['2', '2', '2'],
                ['1', '1', '1'], ['2', '2', '-2'], ['1', '1', '1'],
                ['4', '4', '-4'], ['3', '3', '-3'], ['3', '3', '-3'],
                ['3', '3', '-3'], ['2', '2', '-2'], ['2', '2', '-2'],
                ['3', '3', '-3'], ['2', '2', '-2'], ['1', '1', '-1'],
                ['2', '2', '-2'], ['3', '3', '-3'], ['2', '2', '-2'],
                ['1', '1', '-1'], ['1', '1', '1'], ['4', '4', '4'],
                ['3', '3', '-3'], ['2', '2', '2'], ['1', '1', '-1'],
                ['1', '1', '-1'], ['4', '4', '4'], ['3', '3', '3'],
                ['3', '3', '-3'], ['3', '3', '-3'], ['2', '2', '-2'],
                ['2', '2', '-2'], ['3', '3', '-3'], ['2', '2', '-2'],
                ['1', '1', '-1'], ['2', '2', '-2'], ['1', '1', '1']]
    print(test_csv)
    print(parse_csv(test_csv))
    test_info = gather_info(parse_csv(test_csv))
    print(test_info)
    test = User_Stats()
    test.set_grips(test_info)
    print()
    print("new values: {}, {}, {}, {}, {}, {}".format(test._red_avg,test._blue_avg, test._green_avg, test._purple_avg, test._yellow_avg, test._overall_avg))
    print("_difference = ", test._difference)
    print("old values: {}, {}, {}, {}, {}, {}".format(test._old_red_avg,test._old_blue_avg, test._old_green_avg, test._old_purple_avg, test._old_yellow_avg, test._old_overall_avg))
    print("test 1 = " + test.select_feedback())
    for t in [1,2,3,4,5]:
        print("t= {}; avg= {}; old_avg= {}".format(int(t), test.get_grip_avg(t), test.get_old_grip_avg(t)))
    '''test.set_overall_avg(-1)
    print("test 2 = " + test.select_feedback())
    test.set_overall_avg(14.003)
    print("test 3 = " + test.select_feedback())
    test.set_overall_avg(1)
    print("test 4 = " + test.select_feedback())
    test.set_overall_avg(3)
    test._followup = "red"
    print("test 5 = " + test.select_feedback())
    '''
    print("To run experiments please run 'RIVA_Main.py'")
