#!/usr/bin/env python3
# Totally ratchet code to get more than one set of 200 tweets for POTUS.

from requests_oauthlib import OAuth1
import requests
import json
import os
import sys
import pprint

screenname = 'realdonaldtrump'
    
cons_key = 'FEOcBkKzrJ9DgHv7nk09IdbPC'
cons_secret = 'Ag2goeTRfhkh6Gs9FsYMxjen4okGYLueHi4KHAv9HbjXARqcAR'
access_token = '1019144197-FgFWoxmpftMTd3UFp2ga7WGeLgohrT9Td6woWtG'
access_secret = 'Z2ngO1ivCsMyvKeuvD8D6bAFkEZPMFlPYdgDoNEev5w2Y'

oauth = OAuth1(cons_key, cons_secret, access_token, access_secret)


payload = requests.get("https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={}&count=200".format(screenname),auth=oauth)
tweets = json.loads(payload.content)
min_id = min([ t['id'] for t in tweets ])
payload = requests.get("https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={}&count=200&max_id={}".format(screenname,min_id-1),auth=oauth)
tweets2 = json.loads(payload.content)
tweets.extend(tweets2)

with open("donald.tweets","w") as f:
    for t in tweets:
        print("tweet #{}: {}".format(t['id'], 
            ' '.join(t['text'].split()[0:4]) + "..."),
            file=f)

