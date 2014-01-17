import ConfigParser
from twitter import Twitter, OAuth
import time
import re

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

## testing with some odyssey text

sleep_time_line = 10
sleep_time_burst = 30
sleep_time_chant = 60


with open(source) as f:
    for line in f:
        if re.match(r'^\s*$',line) is not None:
            time.sleep(sleep_time_burst)
            pass

        else:
            try:
                status = hash_line(line)
                t.statuses.update(status=status)
                print(status)
                time.sleep(sleep_time_line)
            except:
                pass

