"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow
import datetime
import dateutil.parser
import logging

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers

       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)

       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet

    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """

    #table with min speed data
    min_table = [(1000, 13.333),
                (600, 11.428),
                (400, 15),
                (200, 15),]

    #Rule 9 table
    brev_table = [(1000, 75, 0),
                (600, 40, 0),
                (400, 27, 0),
                (300, 20, 0),
                (200, 13, 30)]

    total_dist = control_dist_km
    brevet_dist = brevet_dist_km

    hours = 0
    minutes = 0

    #if control = 0, close is 1 hour after start
    if (total_dist == 0): hours += 1

    #if control is larger than brevit
    elif (total_dist >= float(brevet_dist)):

        for brev in brev_table:
            brvt, brv_h, brv_m = brev

            if (int(brevet_dist) == int(brvt)):
                hours += brv_h
                minutes += brv_m

    else:
        for dist in min_table: #for line in min_table
            d_range, time = dist #d_range = top of range
                                 #time = amount to be used in equation

            while (total_dist-d_range > 0):

                increm = (total_dist - d_range) / time #get float to be used on time
                total_dist = d_range

                h, m = divmod(increm, 1) #split float @. to get hour/min
                hours += h #increment hours
                minutes += (m*60) #mult m by 60 to get out of decimal form

        if (total_dist <= 600):

            increm = total_dist / 15 #get float to be used on time
            h, m = divmod(increm, 1) #split float @. to get hour/min
            hours += h #increment hours
            minutes += (m*60) #mult m by 60 to get out of decimal form

    datetime_str = brevet_start_time
    some_datetime_obj = dateutil.parser.parse(datetime_str)  # Convert to datetime object

    while (hours >= 24):

        some_datetime_obj = some_datetime_obj + datetime.timedelta(days=1)
        hours -= 24

    some_datetime_obj = some_datetime_obj + datetime.timedelta(hours=hours)
    some_datetime_obj = some_datetime_obj + datetime.timedelta(minutes=minutes)

    datetime_str = some_datetime_obj.isoformat() # Convert back to ISO 8601 format

    return datetime_str



def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.

    """

    #table with max speed data
    min_table = [(1000, 26),
                (600, 28),
                (400, 30),
                (200, 32),]

    total_dist = control_dist_km
    brevet_dist = brevet_dist_km

    hours = 0
    minutes = 0

    #If control = 0, do nothing!
    if (total_dist == 0): print("Start!")

    else:

        #if control is larger than brevet
        if (total_dist >= float(brevet_dist)):
            total_dist = int(brevet_dist)

        for dist in min_table: #for line in min_table
            d_range, time = dist #d_range = top of range
                                 #time = amount to be used in equation

            while (total_dist-d_range > 0):

                increm = (total_dist - d_range) / time #get float to be used on time
                total_dist = d_range

                h, m = divmod(increm, 1) #split float @. to get hour/min
                hours += h #increment hours
                minutes += (m*60) #mult m by 60 to get out of decimal form

        if (total_dist <= 200):

            increm = total_dist / 34 #get float to be used on time
            h, m = divmod(increm, 1) #split float @. to get hour/min
            hours += h #increment hours
            minutes += (m*60) #mult m by 60 to get out of decimal form

    datetime_str = brevet_start_time
    some_datetime_obj = dateutil.parser.parse(datetime_str)  # Convert to datetime object

    #Update days accordingly
    while (hours >= 24):
        some_datetime_obj = some_datetime_obj + datetime.timedelta(days=1)
        hours -= 24

    #increment time accordingly
    some_datetime_obj = some_datetime_obj + datetime.timedelta(hours=hours)
    some_datetime_obj = some_datetime_obj + datetime.timedelta(minutes=minutes)

    datetime_str = some_datetime_obj.isoformat() # Convert back to ISO 8601 format

    return datetime_str
