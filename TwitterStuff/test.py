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
import os
from pathlib import Path
#%%
CKEYY = "wqMfs8pY9qK7xd0L919Cg7zkd"
CSECRETT = "bNTEgxCjg6CajVOIPER2U7IxznDTXMnfbEwRl06O13Vv1vwZvO"
TOKENN = "779402207057760257-mEols8mD0CPWYbVFSzSO9Fn1LarVF0s"
ASECRETT = "T18p8v4LnQ32svd7hQ4FJivDX7KQgg05LDf2GrFdC6PTz"
auuth = OAuth1(CKEYY, CSECRETT, TOKENN, ASECRETT)
count = 0
tracker = 0
#Pulls tweets from congressperson in list congressPeople
memberTweets = {}
for member in congressPeople:
    page = requests.get("https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name="+member.lower()+"&count=200&include_rts=false", auth=auuth)
    fptweets = json.loads(page.content)
    if len(fptweets)==0:
        continue
    min_id = min([i['id'] for i in fptweets])
    page = requests.get("https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name="+member.lower()+"&count=200&include_rts=false&max_id="+str(min_id-1), auth=auuth)
    sptweets = json.loads(page.content)
    fptweets.extend(sptweets)
    memberTweets[member] = fptweets
    if count == 50:
        print(memberTweets[member])
        time.sleep(1000)
        count = 0
    count += 1
    tracker+=1
    print(str(tracker)+". "+member + " " + str(min_id))
    
#%%
#Create  a dropout that checks for missing names in the dict

def updatetweets():
    dempath = "./Democrat/"
    reppath = "./Republican/"
    for name in congressPeople:
        if name not in memberTweets.keys():
            continue#<<<<< Do it here
        elif Path(dempath+name+".txt").exists():
            with open(dempath+name+".txt", "w") as f:
                for i in range(len(memberTweets[name])):
                    f.write(memberTweets[name][i]['text'])
        elif Path(reppath+name+".txt").exists():
            with open(reppath+name+".txt", "w") as f:
                for i in range(len(memberTweets[name])):
                    f.write(memberTweets[name][i]['text'])
        else:
            print(name+ " not found in either folder.")
updatetweets()