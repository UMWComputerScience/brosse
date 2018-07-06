#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 13:50:34 2018

@author: bryceanderson


To-Do:
    - add some sort of tracking progress system
    - set up skeleton code for database
"""
import psycopg2
import nltk
conn = psycopg2.connect(dbname="brosse_test", user="banders6") #Need database name and rest or params



def create_Labels(): #<pass in a cursor maybe>
    user_cur = conn.cursor()
    user_cur = user_cur.execute("Select userid from temp_users")
    userID = user_cur.fetchone()
    """Loop through Users table collecting the User ID"""
    while userID is not None:
        tweet_cur = conn.cursor()
        tweet_cur.execute("Select Text from temp_tweets where userid="+str(userID[0])+"")
        rows = tweet_cur.fetchall()
        text = ""
        for row in rows:
            text += row[0]
        """Do text stuff"""
        print("For user {}".format(userID[0]) + ": " + text)
        userID = user_cur.fetchone()
#    text = prettify(text)                   #Make a module file for these methods
#    text = noHandles(text)                                  #<----
#    text = noStopWords(text)                                #<----
#    text = sorted(nltk.FreqDist(nltk.Text(nltk.word_tokenize(text))))
#    textFeatures = getFeatures(text)                        #<----
#    Dem = classifier.prob_classify(textFeatures).prob('D')
#    Rep = classifier.prob_classify(textFeatures).prob('R')
#    result = conn.cursor()
#    if Dem > Rep:
#         #Send Dem to table
#        result.execute("Update temp_users set party={}".format(Dem) + " where userid={}".format(userID))
#    else:  #Rep > Dem
#        result.execute("Update temp_users set party={}".format(Rep) + " where userid={}".format(userID))
#Send Rep to table
create_Labels()