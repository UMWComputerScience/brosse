#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 13:50:23 2018

@author: bryceanderson
"""

from requests_oauthlib import OAuth1
import requests
import json

CKEY = "9XINgUNhR5RbNWv9HA6goMrFP"
CSECRET = "rASBq7XOtra7eUV5pKaguXZWDrLvX1nwGAbcMpXPdDj70Z7JRz"
TOKEN = "779402207057760257-BWVmaSHepbGFkh5CEQ4LcLyxBmapbAL"
ASECRET = "UnjMCePkYGIsMFgYZeYaLDkslCewFAok9ZXnrlNqdsASL"

oauth = OAuth1(CKEY, CSECRET, TOKEN, ASECRET)

members = requests.get("https://api.twitter.com/1.1/lists/members.json?slug=members-of-congress&owner_screen_name=cspan&count=1000", auth=oauth)
result = json.loads(members.content)
congressPeople = []
for i in range(len(result['users'])):
    congressPeople.append(result['users'][i]['screen_name'])
memberTweets = {}
for member in congressPeople:
    memberTweets[member] = json.loads(requests.get("https://api.twitter.com/1.1/search/tweets.json?q="+member+"&result_type=recent&count=100", auth=oauth).content)