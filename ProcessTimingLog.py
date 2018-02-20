# /////////////////////////////////////////////////////////////////////////////
#  NOvA TIMING SYSTEM LOG PARSER
#  \brief   A script to parse a timing system log file and write information
#           to the database
#  \author  Justin Vasel <jvasel@indiana.edu>
#  \date    February 2018
# /////////////////////////////////////////////////////////////////////////////

__version__ = 'v0.1.0'

# Python modules
import argparse
import re
import sys
import logging

# App-specific modules
import Config as config
import Database as db
from Utilities import NovaTimeConvert, progressBar

# Argument parsing
parser = argparse.ArgumentParser(description = 'Timing System Log File Parser')
parser.add_argument('logfile', help = 'Path to logfile to process')
parser.add_argument('--version', action = 'version', version = '%(prog)s {}'.format(__version__))
args = parser.parse_args()

# Configure logging
logging.basicConfig(level = logging.DEBUG if config.DEBUG else logging.INFO, \
                    format = '%(asctime)-15s %(message)s')

# Open log file
log = open(args.logfile, 'r')
lines = log.readlines()

# Check with database about log file
logfilename = args.logfile.split('/')[-1]
if db.session.query(db.Logfile).filter(db.Logfile.filename == logfilename).first() == None:
    logging.info('Adding {} to the database'.format(logfilename))
    db.session.add(db.Logfile(filename = logfilename))

# Loop over each line of the log file
for lineno in range(0, len(lines)):
    line = lines[lineno].rstrip()    
    if lineno % 1000 == 0:
        progressBar(lineno, len(lines))

    # Get the message type
    match = re.match(r'%MSG-i (.*): .*', line, re.M|re.I)
    if match == None:
        continue
    msgType = match.group(1)

    # Perform an appropriate action depending on the message type
    if msgType == 'SpillSent':
        logging.debug('I will process a {} message type'.format(msgType))
        msgBody = lines[lineno + 1].rstrip()

        # Parse message body
        match = re.match(r'Spilltype: (.*)\((\d+)\) \(evt (.*)\) novaTime .* (\d+)', msgBody, re.M|re.I)
        spillTypeName = match.group(1)
        spillTypeID   = int(match.group(2))
        spillAccelEvt = match.group(3)
        spillTime     = NovaTimeConvert.convertNovaTimeToUnixTime(int(match.group(4)))

        logging.debug('Found spill type {} ({}), event code {} at time {}'.format(spillTypeName, spillTypeID, spillAccelEvt, spillTime))

        # Update database with spill type
        if db.session.query(db.SpillType).filter(db.SpillType.id == spillTypeID).first() == None:
            logging.info("Adding spill type {} ({}) to the database".format(spillTypeID, spillTypeName))
            db.session.add(db.SpillType(id = spillTypeID, name = spillTypeName, evtcode = spillAccelEvt))

        # Update database with spill
        db.session.add(db.Spill(spill_type_id = spillTypeID, time_spillserver = spillTime))

    if msgType == 'TimeDrift':
        logging.debug('I will process a {} message type'.format(msgType))

    if msgType == 'HeartBeat':
        logging.debug('I will process a {} message type'.format(msgType))

    if msgType == 'TimeSync':
        logging.debug('I will process a {} message type'.format(msgType))

    if lineno > 100:
        break

db.session.commit()
