#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
To run this, type:
$ nohup ./database.py > database_output.txt &
Created on Tue Jul  3 13:50:34 2018

@author: bryceanderson


To-Do:
    - add some sort of tracking progress system
    - set up skeleton code for database
"""
import psycopg2
from nltk.corpus import stopwords
import nltk 
import pickle
from nltk.classify import SklearnClassifier
from sklearn.svm import SVC
import classifier
import tfidf
def create_Labels(corpus_root, word_features=None, classify=None):
    print("Building classifier...")
    featureset, idfs = tfidf.get_tfidf_featureset(".")
    nonpandas_fs = [ (s.to_dict(), l) for s,l in featureset ]
    #Classifier below
    DemorRep = SklearnClassifier(SVC(probability=True), sparse=False).train(nonpandas_fs)
    print("...built!")

    #Change limit value to 0 for whole table
    #limit = int(input("How many users would you like to label? (Enter 0 for whole table): "))
    conn = psycopg2.connect(dbname="brosse", user="banders6")
    conn.autocommit = True
    user_cur = conn.cursor()
    count = 0
    print("Fetching userids...")
    #if limit != 0:
     #   user_cur.execute("Select userid from users limit {}".format(limit))
    #else:
    user_cur.execute("select userid from users")
    userID = user_cur.fetchall()
    #Loops through Users table collecting the User ID

    for ID in userID:
        print("For user {}: ".format(ID[0]))
        tweet_cur = conn.cursor()
        tweet_cur.execute("Select text from tweets where userid="+str(ID[0]))
        rows = tweet_cur.fetchall() 
        print("Cursor fetched: {} tweets".format(len(rows)))
        text = ""
        for row in rows:
            text += row[0]
        probability = tfidf.classify_manual(DemorRep, text)

        #Updates table and Verifies change
        print("Updating Table...")
        result = conn.cursor()
        result.execute("Update users set party={} where userid={}".format(((2*probability)-1), ID[0]))
        label = conn.cursor()
        label.execute("Select party from users where userid={}".format(ID[0]))
        party = label.fetchone()
        print("Pulled {} from user {}".format(party, ID[0]))
        count += 1
        print("Completed {} Users".format(count))


#rn = input("Do you want to run this program?(y/n): ")
#if rn=='y':
#    create_Labels(".")
#else:
#    print("Program Terminated...")
create_Labels(".")
print("Finished!")
