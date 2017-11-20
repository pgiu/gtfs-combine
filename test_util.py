from util import *

tests = ['24:00:10', '09:00:10', '25:00:10', '28:01:01', '49:10:11', '00:00:00', '00:00:01', '23:59:59', '18:00:01']

timeFormat = '%H:%M:%S'
for t in tests:
    print '-------------'
    print 'Input:', t
    d = toDatetime(t, timeFormat)
    print 'Converted:', d
    s = datetimeToString(d, timeFormat)
    print 'Converted back (should be the same as input):', s
    if s == t:
        print 'test passed'
    else:
        print 'test FAILED!!!!!!!!!!!!!!!!!!!!!!!'
