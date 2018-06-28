#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 13:50:23 2018

@author: bryceanderson
"""

from requests_oauthlib import OAuth1
import requests
import json
#%%
CKEY = "bOBSVsmIyfocAJkMYKMw6p2zO"
CSECRET = "Oh9nbfQhPkYkm8J7pR972L68JjrqAPS3WdGUyQ4CUdPRmnRPwW"
TOKEN = "779402207057760257-dG6x21WPk3AQUUg8cR9mJdajTBL1Oqd"
ASECRET = "PBtJVfknEOFqR19G36epwn9JxCmqxckF8A01T2Vhk3zev"
counter = 0
oauth = OAuth1(CKEY, CSECRET, TOKEN, ASECRET)

members = requests.get("https://api.twitter.com/1.1/lists/members.json?slug=members-of-congress&owner_screen_name=cspan&count=600", auth=oauth)
result = json.loads(members.content)
congressPeople = []
for i in range(len(result['users'])):
    congressPeople.append(result['users'][i]['screen_name'])
lastSection = congressPeople[180:]