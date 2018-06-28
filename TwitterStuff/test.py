#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 13:37:31 2018

@author: bryceanderson
"""
from requests_oauthlib import OAuth1
import requests
import json
import time
#%%
CKEYY = "fUdsdDTsHsSxbaL21imsdV8PT"
CSECRETT = "E7yNVukQMsoLposqPn7WcUhBZQjsJAROZwsftvvu81lEXA56zr"
TOKENN = "779402207057760257-ehJ9yp3V1HHpCO9fSpicI6ptviF2CF7"
ASECRETT = "bHUpcpIN1LDz0NSoYbh8AdzJ6MSR8rVEeBi8EB1i8DvLz"
auuth = OAuth1(CKEYY, CSECRETT, TOKENN, ASECRETT)
count = 0



memberTweets = {}
for member in congressPeople:
    if count == 100:
        time.sleep(1000)
        count = 0
    memberTweets[member] = json.loads(requests.get("https://api.twitter.com/1.1/search/tweets.json?q="+member+"&result_type=recent&count=100", auth=auuth).content)
    count += 1
#%%
    
for name in congressPeople:
    tweet = ""
    for i in range(len(memberTweets[name]['statuses'])):
        tweet += memberTweets[name]['statuses'][i]['text']
        with open(name+".txt", "w") as f:
            f.write(tweet)