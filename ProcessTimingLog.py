__version__ = 'v0.1.0'

# Python modules
import argparse
import re
import sys
# App-specific modules
import Config as config
import Database as db

# Argument parsing
parser = argparse.ArgumentParser(description = 'Timing System Log File Parser')
parser.add_argument('logfile', help = 'Path to logfile to process')
parser.add_argument('--version', action = 'version', version = '%(prog)s {}'.format(__version__))
args = parser.parse_args()

# Open log file
log = open(args.logfile, 'r')
lines = log.readlines()

# Check with database about log file
logfilename = args.logfile.split('/')[-1]
if db.session.query(db.Logfile).filter(db.Logfile.filename == logfilename).first() == None:
    print "Adding {} to the database".format(logfilename)
    db.session.add(db.Logfile(filename = logfilename))

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
        if config.DEBUG == True:
            print('I will process a {} message type'.format(msgType))

    if msgType == 'TimeDrift':
        if config.DEBUG == True:
            print('I will process a {} message type'.format(msgType))

    if msgType == 'HeartBeat':
        if config.DEBUG == True:
            print('I will process a {} message type'.format(msgType))

    if msgType == 'TimeSync':
        if config.DEBUG == True:
            print('I will process a {} message type'.format(msgType))

    # print "Next line: ", lines[lineno + 1].rstrip()

    if lineno > 100:
        break

db.session.commit()
