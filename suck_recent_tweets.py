#!/usr/bin/env python3

from requests_oauthlib import OAuth1
import requests
import json
import os
import sys

force = False
if len(sys.argv) not in [2,3]:
    sys.exit("Usage: suck_tweets.py [-f] screenname.")
elif len(sys.argv) == 3 and sys.argv[1] != "-f":
    sys.exit("Usage: suck_tweets.py [-f] screenname.")
elif len(sys.argv) == 3 and sys.argv[1] == "-f":
    force = True
    screenname = sys.argv[2]
else:
    screenname = sys.argv[1]
if screenname[0] == '@': screenname = screenname[1:]
if not force and os.path.exists(screenname + ".tweets"):
    sys.exit("File {}.tweets exists! (Use -f flag to overwrite)".format(
        screenname))
    

cons_key = 'FEOcBkKzrJ9DgHv7nk09IdbPC'
cons_secret = 'Ag2goeTRfhkh6Gs9FsYMxjen4okGYLueHi4KHAv9HbjXARqcAR'
access_token = '1019144197-FgFWoxmpftMTd3UFp2ga7WGeLgohrT9Td6woWtG'
access_secret = 'Z2ngO1ivCsMyvKeuvD8D6bAFkEZPMFlPYdgDoNEev5w2Y'

oauth = OAuth1(cons_key, cons_secret, access_token, access_secret)


payload = requests.get("https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={}&count=200".format(screenname),auth=oauth)
tweets = json.loads(payload.content)

mode = "w+" if force else "w"
with open(screenname + ".tweets",mode) as f:
    for i in range(len(tweets)):
        print(tweets[i]['text'], file=f)
