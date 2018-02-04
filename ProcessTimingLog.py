__version__ = 'v0.1.0'

# Python modules
import argparse
# App-specific modules
import Database

# Argument parsing
parser = argparse.ArgumentParser(description = 'Timing System Log File Parser')

parser.add_argument('logfile', help = 'Path to logfile to process')

# parser.add_argument('-f', action = 'store', dest = 'logfile',
#                     help = 'Path to logfile to process')

parser.add_argument('--version', action = 'version', version = '%(prog)s {}'.format(__version__))

results = parser.parse_args()
