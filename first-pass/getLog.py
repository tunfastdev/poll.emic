import os
import sys
import simplejson as json
from pprint import pprint as pp
from authtwitter import twitter
from twitter import TwitterHTTPError
import time

SLEEP = 10

USE_TWITTER_LOG = False
LOG_PATH = "log/"

def load_snowball():
    SNOWBALL_PATH = "snowball-47545000-3.json"
    if len(sys.argv) > 1:
        SNOWBALL_PATH = sys.argv[1]

    if os.path.isfile("%s" % (SNOWBALL_PATH)):
        snowball_file = open("%s" % (SNOWBALL_PATH),'r')
        snowball = json.loads(snowball_file.read())
        return snowball
    else:
        print "error"


if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

snowball = load_snowball()

def use_twitter_log(screen_name):
        cmd = "twitter-log " + screen_name + " > " + LOG_PATH + screen_name + ".txt"
        print cmd
        os.system(cmd)

def use_statuses_api(screen_name):
    log_path = "%s%s.json" % (LOG_PATH, screen_name)

    if os.path.isfile(log_path):
        print "File %s already exists, not overwriting" % (log_path)
    else:
        try:
            tweets = twitter.statuses.user_timeline(screen_name=screen_name,count=200,include_rts=1)
            pp(tweets)
            file = open(log_path, 'w')
            file.write(json.dumps(tweets))
            time.sleep(SLEEP)
        except TwitterHTTPError as e:
            print(e) # need to print more about exception here
            #sleep, then try again
            time.sleep(30)
            #use_statuses_api(screen_name)


for u_id, metadata in snowball.items():
    #print "crawling: ", line
    if metadata.has_key('screen_name'):
        screen_name = metadata['screen_name']
        
        if USE_TWITTER_LOG:
            use_twitter_log(screen_name)
        else:
            use_statuses_api(screen_name)
    else:
        print 'No screen name for %s'%(u_id)



 
