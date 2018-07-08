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
from nltk.corpus import stopwords
import nltk
from bryce import *
 #Need database name and rest or params
nltk.download('stopwords')
nltk.download('punkt')

def create_Labels(): #<pass in a cursor maybe>
    conn = psycopg2.connect(dbname="brosse_test", user="banders6")
    user_cur = conn.cursor()
    user_cur.execute("Select userid from temp_users limit 10")
    userID = user_cur.fetchall()
    """Loop through Users table collecting the User ID"""
    for ID in userID:
        print("For user {}".format(ID))
        tweet_cur = conn.cursor()
        tweet_cur.execute("Select text from temp_tweets where userid="+str(ID[0]))
        rows = tweet_cur.fetchall()
        text = ""
        for row in rows:
            text += row[0]
        """Do text stuff"""
        text = prettify(text) #Make a module file for these methods
        text = noHandles(text)                               #<----
        text = noStopWords(text)                                #<----
        text = sorted(nltk.FreqDist(nltk.Text(nltk.word_tokenize(text))))
        print(text)
    #textFeatures = getFeatures(text)                        #<----
    #Dem = classifier.prob_classify(textFeatures).prob('D')
    #Rep = classifier.prob_classify(textFeatures).prob('R')
    #result = conn.cursor()
    #if Dem > Rep:
         #Send Dem to table
     #   result.execute("Update temp_users set party={}".format(Dem) + " where userid={}".format(userID))
    #else:  #Rep > Dem
     #   result.execute("Update temp_users set party={}".format(Rep) + " where userid={}".format(userID))
#Send Rep to table
create_Labels()
