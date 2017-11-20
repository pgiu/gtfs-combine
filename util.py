# -*- coding: utf-8 -*-
import sys
import pickle
from datetime import datetime
from datetime import timedelta

# Print iterations progress
def print_progress (iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar

    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '#' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

# Loads data from a pickle file
def loadFromPicke (filename):
    print "Loading pickle:",filename
    f = open(filename, 'rb')
    read = pickle.load(f)
    f.close()
    return read

def getFileLength (fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

# Converts a string to date time object.
# It handles the pathological case in which some people write 00:00:00 as 24:00:00
def toDatetime(input, timeFormat):

    if len(input) > 2:
        hour = int(input[0:2])
        if hour>=24:
            newTime = str(hour%24)+input[2:]
            d = datetime.strptime(newTime, timeFormat)
            return d + timedelta(days=(hour/24))
        else:
            return datetime.strptime(input, timeFormat)


def datetimeToString(ind, timeformat):

    if ind.day>1:
        result = str(24 * (ind.day-1) + ind.hour) + ind.strftime(':%M:%S')
        return result
    return ind.strftime(timeformat)


def getHeaderCategories(stopTimesHeader):

    stopTimesHeaderSplit = stopTimesHeader.split(',')
    stopTimesLabels = {}
    for i in range(len(stopTimesHeaderSplit)):
        stopTimesLabels[stopTimesHeaderSplit[i]] = i

    for i in stopTimesLabels:
        print i