__version__ = 'v0.1.0'

# Python modules
import argparse
import re
# App-specific modules
import Config as config
import Database

# Argument parsing
parser = argparse.ArgumentParser(description = 'Timing System Log File Parser')

parser.add_argument('logfile', help = 'Path to logfile to process')
parser.add_argument('--version', action = 'version', version = '%(prog)s {}'.format(__version__))

results = parser.parse_args()

# Open log file
log = open(results.logfile, 'r')
lines = log.readlines()

# Loop over each line of the log file
for lineno in range(0, len(lines)):
    line = lines[lineno].rstrip()

    # Get the message type
    match = re.match( r'%MSG-i (.*): .*', line, re.M|re.I)
    if match == None:
        continue
    msgType = match.group(1)

    if config.DEBUG == True:
        print('Found MSG : {}'.format(msgType))

    # Perform an appropriate action depending on the message type
    if msgType == 'SpillSent':
        print('I will process a {} message type'.format(msgType))

    if msgType == 'TimeDrift':
        print('I will process a {} message type'.format(msgType))

    if msgType == 'HeartBeat':
        print('I will process a {} message type'.format(msgType))

    if msgType == 'TimeSync':
        print('I will process a {} message type'.format(msgType))

    # print "Next line: ", lines[lineno + 1].rstrip()

    if lineno > 100:
        break
