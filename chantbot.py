import ConfigParser
from twitter import Twitter, OAuth
import time
from datetime import datetime, date
from datetime import time as dtime
import itertools
import logging
import os
from parse import *
import sys

config= ConfigParser.ConfigParser()
config.read('config.cfg')

# Setup Twitter client
def get_twitter_client():
    oauth = OAuth(config.get('OAuth','accesstoken'),
                  config.get('OAuth','accesstokenkey'),
                  config.get('OAuth','consumerkey'),
                  config.get('OAuth','consumersecret'))

    t = Twitter(auth=oauth)

    return t

# Setup Logging

logpath = config.get('Logging','logpath')

if not os.path.exists(logpath):
    os.makedirs(logpath)

##cruft?
logger = logging.getLogger('log')
#todo: use date/time as the log file name
hdlr = logging.FileHandler(os.path.join(logpath,
                                        "%s.log" % datetime.now().isoformat()))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

# Setup chants

source = config.get('Content','source')

keywords = config.get('Content','keywords').split(',')

# number of bursts per chant
num_bursts = int(config.get('Schedule','bursts'))

# which day is the 'starting day' of the chanting
startday = time.strptime(config.get('Schedule','startday'),"%m/%d/%y")

# time between tweets in a burst
beat = int(config.get('Schedule','beat'))

def which_chant(chants):
    start = datetime.fromtimestamp(time.mktime(startday)).toordinal()
    today = date.today().toordinal()

    chant_index = (today - start) % len(chants)

    return chants[chant_index]

def main(argv=None):
    t = get_twitter_client()

    import pdb;pdb.set_trace()

    argv = sys.argv

    #index of the burst
    b = 0
        
    try:
        b = int(argv[1])
    except Exception as e:
        print e
    
    #Reads the source file and parses it into a list of chants
    chants = prepare_chants(source,num_bursts,keywords)

    chant = which_chant(chants)

    burst = chant.bursts[b]
    
    for line in burst:
        t.statuses.update(status=line)
        print line
        logger.debug(line)
        time.sleep(beat)


    return 0


if  __name__ =='__main__':
    main()
