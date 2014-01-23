import ConfigParser
from twitter import Twitter, OAuth
import time
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
chant_start = 0

# time between tweets in a burst
beat = int(config.get('Schedule','beat'))

# total duration of a chant
duration = int(config.get('Schedule','duration'))


def chant(chant):

    interval = duration / (len(chant.bursts) - 1)

    rest = interval - len(chant.lines) * beat
    print "rest: %d" % rest

    for burst in chant.bursts:
        for line in burst:
            print line
            time.sleep(beat)

        time.sleep(rest)


# burn in to appropriate starting chant
#for i in range(chant_start):
#    chants.next()

# chants = itertools.cycle(chants)
print(chants[0].lines)
print(chants[1].lines)
print(chants[2].lines)
chant(chants[0])
