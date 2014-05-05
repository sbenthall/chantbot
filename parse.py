import ConfigParser
import re
import math

config= ConfigParser.ConfigParser()
config.read('config.cfg')

def hash_word(match):
    return '#' + match.group()

def hash_line(line,kw_re):
    for kr in kw_re:
        line = re.sub(kr, hash_word, line)

    return line

def prepare_chants(source,num_bursts,keywords):
    """
    prepare_chants(source) -> list of Chants

    Read in the text from the source file and
    return a list whose elements are 
    """

    chants = []

    f = open(source)

    text = ""

    kw_re = [re.compile(r'\b%s\b' % kw,flags=re.I) for kw in keywords]

    for line in f:
        if re.match(r'^\s*$',line) is not None:
            if text is not "":
                chants.append(Chant(text,num_bursts))
                text = ""
        else:
            # add hashtags where necessary
            text += hash_line(line,kw_re)

    f.close()

    return chants


class Chant:

    lines = []
    bursts = []
    # lines per burst
    lpb = 0

    def __init__(self,text,num_bursts):
        self.lines = text.split("\n")

        if self.lines[-1] is "":
            self.lines = self.lines[0:-1]

        # lines per burst
        self.lpb = int(math.ceil(float(len(self.lines)) / num_bursts))

        self.bursts = [self.lines[i:i+self.lpb] for i 
                       in xrange(0,len(self.lines),self.lpb)]

        if len(self.bursts) < num_bursts:
            self.bursts.append([])
