# /////////////////////////////////////////////////////////////////////////////
#  NOvA TIME CONVERT UTILITY
#  \brief   Convert between the NOvA and unix epochs
#  \author  Justin Vasel <jvasel@indiana.edu>
#  \date    February 2018
# /////////////////////////////////////////////////////////////////////////////

# Number of clock ticks per second (64 MHz)
NOVA_TIME_FACTOR = 64000000

# Start of Nova epoch, 01-Jan-2010 00:00:00, UTC
# This is the value subtracted unix time. Since "novatime" does not have leap 
# seconds and unix time does, leap seconds which happen _after_ the NOvA epoch 
# will need to be factored in to get the correct novatime which corresponds to
# the time after the leap second.
NOVA_EPOCH = 1262304000;

# Leap seconds since NOvA epoch began:
LEAP_SECONDS = [
    1341100799, # Jun 30 23:59:59 2012 UTC
    1435708799, # Jun 30 23:59:59 2015 UTC
    1483228799  # Dec 31 23:59:59 2016 UTC
]

def convertNovaTimeToUnixTime(novaTime):
    seconds_since_nova_epoch = novaTime * 1.0 / (NOVA_TIME_FACTOR * 1.0)
    unix_time = seconds_since_nova_epoch + NOVA_EPOCH

    # Correct for leap seconds
    for leap in LEAP_SECONDS:
        unix_time -= 1 if unix_time > leap else 0

    return unix_time
