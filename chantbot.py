import ConfigParser
from twitter import Twitter, OAuth
import time
from datetime import datetime
from datetime import time as dtime
import re
import math
import itertools

config= ConfigParser.ConfigParser()
config.read('config.cfg')

oauth = OAuth(config.get('OAuth','accesstoken'),
              config.get('OAuth','accesstokenkey'),
              config.get('OAuth','consumerkey'),
              config.get('OAuth','consumersecret'))

t = Twitter(auth=oauth)


source = config.get('Content','source')

keywords = config.get('Content','keywords').split(',')

kw_re = [re.compile(r'\b%s\b' % kw) for kw in keywords]

def hash_word(match):
    return '#' + match.group()

def hash_line(line):
    for kr in kw_re:
        line = re.sub(kr, hash_word, line)

    return line


# number of bursts per chant
num_bursts = int(config.get('Schedule','bursts'))

class Chant:

    lines = []
    bursts = []

    def __init__(self,text):
        self.lines = text.split("\n")

        # lines per burst
        lpb = int(math.ceil(float(len(self.lines)) / num_bursts))

        self.bursts = [self.lines[i:i+lpb] for i 
                       in xrange(0,len(self.lines),lpb)]
        

def prepare_chants(source):
    """
    prepare_chants(source) -> list of list of strings

    Read in the text from the source file and
    return a list whose elements are 
    """

    chants = []

    f = open(source)

    text = ""
    
    for line in f:
        if re.match(r'^\s*$',line) is not None:
            if text is not "":
                chants.append(Chant(text))
                text = ""
        else:
            # add hashtags where necessary
            text += hash_line(line)

    f.close()

    return chants

chants = prepare_chants(source)

# which chant to start with 
chantburn = int(config.get('Schedule','chantburn'))

# time between tweets in a burst
beat = int(config.get('Schedule','beat'))

# total duration of a chant
duration = int(config.get('Schedule','duration'))

def compute_start():
    start_time = dtime(*time.strptime(config.get('Schedule',
                                                 'starttime'),"%H:%M")[3:5])
    now = datetime.now()

    if now.time() < start_time:
        start_day = now
    else:
        tomorrow = tomorrow = datetime.fromordinal(now.toordinal() + 1)
        start_day = tomorrow

    start = datetime.combine(start_day,start_time)
    return start

def do_chant(chant):

    interval = duration / (len(chant.bursts) - 1)

    rest = interval - len(chant.lines) * beat
    print "interval: %d" % interval
    print "rest: %d" % rest

    for burst in chant.bursts:
        for line in burst:
            t.statuses.update(status=line)
            time.sleep(beat)

        time.sleep(rest)


chants = itertools.cycle(chants)

# burn in to appropriate starting chant
for i in range(chantburn):
    chants.next()

for chant in chants:
    start = compute_start()
    wait = start - datetime.now()
    print "Waiting to start for %s" % wait
    time.sleep(wait.total_seconds())
    do_chant(chant)
