# Stop_times - frequencies merger

This python script takes two GTFS files (`stop_times.txt` and `frequencies.txt`) and generates a new `stop_times_new.txt` 
with the combinations of both files. 

The stop_times defines when a bus will arrive at each stop

## How it works

Assume these are the contents of the two files.

**frequencies.txt**

    tripId,start_time,end_time,headway_secs
    1,06:00:00,08:00:00,120
    1,08:00:00,12:00:00,240

**stop_times.txt**

    trip_id,stop_id,arrival_time,departure_time,
    0,stop1,00:00:00,00:00:00
    0,stop2,00:01:14,00:01:14
    0,stop3,00:02:28,00:02:28
    ...
    
The output will be something like this: 

    trip_id,stop_id,arrival_time,departure_time,
    0_0600_0,stop1,06:00:00,06:00:00
    0_0600_0,stop2,06:01:14,06:01:14
    0_0600_0,stop3,06:02:28,06:02:28
    ...    
    0_0600_1,stop1,06:02:00,06:00:00
    0_0600_1,stop2,06:03:14,06:03:14
    0_0600_1,stop3,06:05:28,06:05:28
    ...    
    0_0600_2,stop1,06:04:00,06:04:00
    0_0600_2,stop2,06:05:14,06:05:14
    0_0600_2,stop3,06:06:28,06:06:28
    ...                     
    (will insert a new trip after *headway* seconds, 
    until the arrival time of the first bus is greater
    than the end_time stated in the frequencies file)
    0_0800_0,stop1,08:00:00,08:00:00
    0_0800_0,stop2,08:01:14,08:01:14
    0_0800_0,stop3,08:02:28,08:02:28
    ...    
    0_0800_1,stop1,08:04:00,08:04:00
    0_0800_1,stop2,08:05:14,08:05:14
    0_0800_1,stop3,08:06:28,08:06:28
    ...    
    0_0800_2,stop1,08:04:00,08:04:00
    0_0800_2,stop2,08:05:14,08:05:14
    0_0800_2,stop3,08:06:28,08:06:28
    ...     

A few things to notice: 

1. The `trip_id` of each trip is updated. The format is like this: 
    <old_trip_id>_<hour_of_first_service>_<service#>
    Where service number is a counter that starts from 0 and increments by one, with each new service.
2. The code will span new services until the time of the first bus exceeds the end_time described in frequencies.
   DT is the Headway.
    
    
        start_time ________________________________________ end_time
            | First Bus
            <- DT-> | Second Bus
                            |Third
                                    ....
                                                         | Last bus
                                                                |<-- can't add a new bus


## How to run it 

1. Copy `stop_times.txt`, `trips.txt` and `frequencies.txt` to the source directory
2. Open a terminal and run `python.py combine`
3. After a while you should have 2 new files: `stop_times_new.txt` and `trips_new.txt`
