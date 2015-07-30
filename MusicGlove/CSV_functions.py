__author__ = 'Nathan'
__editor__ = 'Jessica'
### Nathanial Benjamin, UCI, Calit2, CalPlug, 2014-Feb
# Written in Python 3.3.3 (added statistics and pydub modules)
### JessicaZeng, UCI, Cali2, CalPlug,2015-May
# Edied in Python 2.7


import csv
from time import strftime

### The file where user grip data for current song is stored
MUSICGLOVE = 'R:\\resources\\saves\\temp\\temp.csv'                                         # CalPlug server
#MUSICGLOVE = 'Z:\\resources\\saves\\temp\\temp.csv' # Local Computer

### Sets a unique timestamped filename, in the summaries directory, for the stats of the current song
M_GLOVE_SUMMARIES = "R:\\summaries\\"                                     # CalPlug server
#M_GLOVE_SUMMARIES = "D:\\RIVA\\musicglove_1366x768\\summaries\\" # Local Computer
TIMESTAMP = strftime("%a,%d_%b_%Y_%H;%M;%S")
def current_time():
    return strftime("%a,%d_%b_%Y_%H;%M;%S")

def read_csv(file_path, test = False):
    """ile_path: str, test = False) -> list:
    Read data from a .csv file, and return a list containing
       the actual and expected fingers, and the time difference from expected.
    """
    #print("entering read_csv")
    stat_list = []
    with open(file_path,'rb') as infile:
        
    #with open(file_path, 'r') as infile:

        for line in infile:
            #if test == True:
                #print("line =", line)
                #print('line.strip().split(",") = ', line.strip().split(","))
            temp_stat = line.strip().split(",")
            stat_list.append(temp_stat)
        #if test == True:
            #print("stat_list = ", stat_list)
    return stat_list

def make_csv(stat_list, filename, optional_str=''):
    """ stat_list: list, filename: str, optional_str=''
        Takes a list of stats and/or strings and writes them into .csv file format
            -if optional_str defined, uses as the first line in the file.
    """
    #print("entering make_csv")
    #print(len(read_csv(MUSICGLOVE)))
    if filename == M_GLOVE_SUMMARIES:
        filename += "{}.csv".format(strftime("%a,%d_%b_%Y_%H;%M;%S"))
        #print(filename)
    with open(filename,'wb') as csvfile:
 
        
    #with open(filename, 'w', newline = '') as csvfile:
    
        csv_writer = csv.writer(csvfile, delimiter=',')
        if optional_str != '':
            #print(optional_str)
            csv_writer.writerow([optional_str])
            csv_writer.writerow([])
        for i in stat_list:
            if type(i) is str:
                csv_writer.writerow([i])
                csv_writer.writerow([])
            else:
                csv_writer.writerow(i)
    return


if __name__ == '__main__':
    print("To run experiments please run 'RIVA_Main.py'")
    from time import sleep
    test_result = ['Red Grip avg: 22.563200000001142; Blue Grip avg: 32.978142857142494;Green Grip avg: 27.25257142857195; Purple Grip avg: 60.543199999996794; Yellow Grip avg: 0',
                   'You have improved a lot! I noticed that you were having a little trouble with the Purple Grip',
                   'Red Grip avg: 27.56714285715134; Blue Grip avg: 20.77307692311073;Green Grip avg: 23.33925494792493; Purple Grip avg: 19.787199999965377; Yellow Grip avg: 0',
                   'Keep up the good work! We could still do a little more work on the Red Grip',
                   'Red Grip avg: 20.37581818212427; Blue Grip avg: 28.34021052646935;Green Grip avg: 42.730400000229324; Purple Grip avg: 21.73633333367373; Yellow Grip avg: 0',
                   'You are doing very well! On this next set lets try focusing on the Purple Grip You seemed most proficient with the Yellow Grip!']
    make_csv(test_result, M_GLOVE_SUMMARIES)
    #print(read_csv(M_GLOVE_SUMMARIES)) #fix path for test
    sleep(5)
    make_csv(test_result, M_GLOVE_SUMMARIES)
    sleep(5)
    test_result.extend(read_csv(MUSICGLOVE))
    make_csv(test_result, M_GLOVE_SUMMARIES)
    print("To run experiments please run 'RIVA_Main.py'")
