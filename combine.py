# This script takes two files:
# - stop_times.txt
# - frequencies.txt
# And generates a bigger file called stop_times_new.txt with multiple services for each tripId on the original
# stop_times.txt.
# The frequency info is used to create the time spacing between two consecutive services.

from datetime import timedelta
from util import *

print 'Starting conversion'

timeFormat = '%H:%M:%S'
stop_times = open('stop_times.txt')
stopTimesHeader = stop_times.readline()[:-1] # reads the header
#stopTimesHeader = stop_times.readline()[3:-1] # reads the header

stopTimesHeaderSplit = stopTimesHeader.split(',')
stopTimesLabels = {}
for i in range(len(stopTimesHeaderSplit)):
    stopTimesLabels[stopTimesHeaderSplit[i]]=i

for i in stopTimesLabels:
    print i

stop_times_dct = {}

print 'analyzing stop_times.txt'

rline = stop_times.readline()[:-1]  # gets the first line
while rline:
    split = rline.split(',')
    tripId = split[0]
    new_stop = stop_times_dct.get(tripId, [])
    new_stop.append(rline)
    stop_times_dct[tripId] = new_stop
    rline = stop_times.readline()[:-1]

stop_times.close()

print 'done with stop_times.txt'
print 'creating new stop_times.txt file'
# open a new file called stop_times_new.txt and append the row names
out = open('stop_times_new.txt', 'w')
out.write(stopTimesHeader + '\n')

print 'Analyzing frequencies.txt'
# Load the frequencies
frequencies = open('frequencies.txt')
rline = frequencies.readline()[:-1]  # Discards the header
rline = frequencies.readline()[:-1]

freqSize = getFileLength('frequencies.txt')

# Position of the fields in the frequencies file
trip_id_pos=0
start_time_pos=1
end_time_pos=2
headway_secs_pos=3

# Santiago
# trip_id,arrival_time,departure_time,stop_id,stop_sequence
# Buenos Aires
# trip_id,stop_id,arrival_time,departure_time,timepoint,stop_sequence,stop_headsign,route_short_name,pickup_type,drop_off_type,shape_dist_traveled
# CDMX
# trip_id,stop_sequence,stop_id,arrival_time,departure_time,stop_headsign,route_short_name,pickup_type,drop_off_type,shape_dist_traveled

# For stop_times.txt
stop_id_pos = stopTimesLabels['stop_id']
arrival_time_pos = stopTimesLabels['arrival_time']
departure_time_pos = stopTimesLabels['departure_time']
timepoint_pos = stopTimesLabels.get('timepos', None)
stop_sequence_pos = stopTimesLabels['stop_sequence']

# Extra rows
stop_headsign_pos = stopTimesLabels.get('stop_headsign',None)
route_short_name_pos = stopTimesLabels.get('route_short_name',None)
pickup_type_pos = stopTimesLabels.get('pickup_type',None)
drop_off_type_pos = stopTimesLabels.get('drop_off_type',None)
shape_dist_traveled_pos = stopTimesLabels.get('shape_dist_traveled',None)


# As we have to rename all the trips, we create a dictionary in which we relate the original trip Id and an array of
# New Trip IDs. E.g. trip0 -> [trip0_service0, trip0_service1, ...]
newTripIdDct = {}

print_progress(0, freqSize, prefix='Progress', suffix='Complete', decimals=2, bar_length=50)
c = 0
while rline:
    split = rline.split(',')
    tripId = split[trip_id_pos]
    thisTrip = stop_times_dct.get(tripId, [])

    if c % 10:
        print_progress(c, freqSize, prefix='Progress', suffix='Complete', decimals=2, bar_length=50)

    if not thisTrip:
        print 'The trip', tripId, "doesn't exist in the stop_times.txt file"
    else:  # Place a copy of that trip, starting at the start time of the trip

        startTime = toDatetime(split[start_time_pos], timeFormat)
        endTime = toDatetime(split[end_time_pos], timeFormat)

        # TripId + startTime + service
        firstServiceTime = startTime.strftime("%H%M")

        # Offset (some agencies report trip times that doesn't start at 00:00:00 but rather at, say, 05:00:00,
        # so we actually need to substract 5hs to every trip so that it starts at the correct time.
        o = thisTrip[0].split(',')
        offset = datetime.strptime(o[arrival_time_pos], timeFormat)


        # Keep sending buses until the current time is greater than the end time.
        # Each bus will be headway_secs seconds apart from each other
        service = 0
        while startTime < endTime:

            newLine = {}
            # New Trip ID is a combination of the old trip ip and the service number (0,1,...)
            newTripId = tripId + "_" + firstServiceTime + "_" + str(service)
            newLine['trip_id'] = newTripId

            # Save the new Trip ID into the tripId dictionary
            tripArray = newTripIdDct.get(tripId, [])
            tripArray.append(newTripId)
            newTripIdDct[tripId] = tripArray

            for i in thisTrip:
                # Rename the Trip ID so that it has a reference to this 'service'
                # 'i' has all the fields from the original stop_times.txt, except from the first one, since
                # we're overwriting the tripId field.
                s = i.split(',')
                arr_time = toDatetime(s[arrival_time_pos], timeFormat)
                #arr_time = datetime.strptime(s[arrival_time_pos],   timeFormat)
                dep_time = toDatetime(s[departure_time_pos], timeFormat)
                newLine['stop_sequence'] = s[stop_sequence_pos]
                newLine['stop_id'] = s[stop_id_pos]
                if timepoint_pos:
                    newLine['timepoint'] = s[timepoint_pos]

                if stop_headsign_pos:
                    newLine['stop_headsign'] = s[stop_headsign_pos]

                if route_short_name_pos:
                    newLine['route_short_name'] = s[route_short_name_pos]

                if pickup_type_pos:
                    newLine['pickup_type'] = s[pickup_type_pos]

                if drop_off_type_pos :
                    newLine['drop_off_type'] = s[drop_off_type_pos]

                if shape_dist_traveled_pos:
                    newLine['shape_dist_traveled'] = s[shape_dist_traveled_pos]

                # Add the start time, minus the offset
                #startTimeMinusOffset = startTime - timedelta(hours=offset.hour, minutes=offset.minute, seconds=offset.second)
                arr_time = startTime + timedelta(days=(arr_time.day-offset.day), hours=(arr_time.hour-offset.hour), minutes=(arr_time.minute-offset.minute), seconds=(arr_time.second-offset.second))
                dep_time = startTime + timedelta(days=(dep_time.day-offset.day), hours=(dep_time.hour-offset.hour), minutes=(dep_time.minute-offset.minute), seconds=(dep_time.second-offset.second))

                # Convert back to string
                newLine['arrival_time'] = datetimeToString(arr_time, timeFormat)
                newLine['departure_time']= datetimeToString(dep_time, timeFormat)

                # Write a new line, in the order that we have it in the stop_times file
                line = ''
                for k in range(len(stopTimesHeaderSplit)):
                    line += (newLine.get(stopTimesHeaderSplit[k], ''))
                    if k != (len(stopTimesHeaderSplit)-1):
                        line += ','
                out.write(line+'\n')

            service = service+1
            startTime = startTime + timedelta(seconds=int(split[headway_secs_pos]))

    # Read another line
    rline = frequencies.readline()[:-1]
    c = c+1

# Close all the files
frequencies.close()
out.close()

# Save the dictionary as a pickle
pickle.dump(newTripIdDct, open("newTripIdDct.pickle", "wb"))

# Uncomment this to avoid running everything from scratch
# newTripIdDct = loadFromPicke('newTripIdDct.pickle')

# Now open the trips file
print 'Creating the new trips file'
out = open('trips_new.txt', 'w')

tripsSize = getFileLength('trips.txt')

trips = open('trips.txt')
#tripsHeader = trips.readline()[3:-1] # reads the header minus the first 3 bytes, because I asume it's UTF-8
tripsHeader = trips.readline()[:-1] # reads the header minus the first 3 bytes, because I asume it's UTF-8

out.write(tripsHeader+"\n")

tripsHeaderSplit = tripsHeader.split(',')
tripsLabels = {}
# Create a dictionary with the position of each column name
for i in range(len(tripsHeaderSplit)):
    tripsLabels[tripsHeaderSplit[i]]=i
print 'Position of the labels of trips.txt in this file'
for i in tripsLabels:
    print i,':', tripsLabels[i]

# Basic indexes (they should be there)
trip_id_pos = tripsLabels['trip_id']
route_id_pos = tripsLabels['route_id']
service_id_pos = tripsLabels.get('service_id', None)
direction_pos = tripsLabels.get('direction_id', None)
# Extra indexes
trip_short_name_pos = tripsLabels.get('trip_short_name', None)
trip_headsign_pos =  tripsLabels.get('trip_headsign', None)
route_short_name_pos = tripsLabels.get('route_short_name', None)
block_id_pos = tripsLabels.get('block_id', None)
shape_id_pos = tripsLabels.get('shape_id', None)
wheelchair_accessible_pos = tripsLabels.get('wheelchair_accessible', None)
trip_bikes_allowed_pos = tripsLabels.get('trip_bikes_allowed', None)
bikes_allowed_pos = tripsLabels.get('bikes_allowed', None)


tripsPos = [[trip_id_pos, 'trip_id'],
            [route_id_pos, 'route_id'],
            [service_id_pos, 'service_id'],
            [direction_pos, 'direction_id'],
            [trip_short_name_pos, 'trip_short_name'],
            [trip_headsign_pos, 'trip_headsign'],
            [route_short_name_pos, 'route_short_name'],
            [block_id_pos , 'block_id'],
            [shape_id_pos, 'shape_id'],
            [wheelchair_accessible_pos, 'wheelchair_accessible'] ,
            [trip_bikes_allowed_pos , 'trip_bikes_allowed'],
            [bikes_allowed_pos, 'bikes_allowed']
            ]

rline = trips.readline()[:-1]  # gets the first line
c = 0
while rline:
    split = rline.split(',')
    newLine = {}

    # Copy all the line info to the array
    for i in tripsPos:
        if i[0] != None:
            newLine[i[1]] = split[i[0]]

    # This has to be there
    tripId = newLine['trip_id']

    if c % 10:
        print_progress(c, tripsSize, prefix='Progress', suffix='Complete', decimals=2, bar_length=50)

    newTripIds = newTripIdDct.get(tripId, [])
    if not newTripIds:
        print "WARNING: Couldn't find a list of trips for tripId:", tripId
        print "Copying the line as it was in the original file"
        out.write(rline+"\n")

    else:
        for t in newTripIds:
            newLine['trip_id'] = t
            #out.write(split[0] + "," + t + ",0,,,,0,,,,,\n")
            # Write a new line, in the order that we have it in the stop_times file
            for k in range(len(tripsHeaderSplit)):
                out.write(newLine.get(tripsHeaderSplit[k], ''))
                if k != (len(tripsHeaderSplit) - 1):
                    out.write(',')
            out.write('\n')

    # read a new line
    rline = trips.readline()[:-1]

trips.close()
out.close()
print 'Conversion ended'

