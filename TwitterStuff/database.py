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
    
    #Classifier below
    DemorRep = SklearnClassifier(SVC(probability=True), sparse=False)
    print("...built!")

    conn = psycopg2.connect(dbname="brosse", user="banders6")
    user_cur = conn.cursor()
    user_cur.execute("Select userid from users limit 10")
    userID = user_cur.fetchall()
    #Loops through Users table collecting the User ID

    for ID in userID:
        print("For user {}: \n".format(ID[0]))
        tweet_cur = conn.cursor()
        tweet_cur.execute("Select text from tweets where userid="+str(ID[0]))
        rows = tweet_cur.fetchall() 
        print("Cursor fetched: " + str(len(rows))+ "tweets")
        text = ""
        for row in rows:
            text += row[0]
        probability = tfidf.classify_manual(DemorRep, text)
        print(probability)
        """print("Prettifying...")
        text = classifier.prettify(text)
        print("De-Handlefying...")
        text = classifier.noHandles(text)
        print("De-Stopwordifying...")
        text = classifier.noStopWords(text)
        print("Creating FreqDist...")
        text = nltk.Text(nltk.word_tokenize(text))
        print("Creating feature list for user...")
        textFeatures = classifier.getFeatures(word_features,text)
        print(textFeatures)
        probability = DemorRep.prob_classify(textFeatures).prob('R')
        probability = float((probability * 2) - 1)
        print("PROB({}): ".format(ID[0]))
        result = conn.cursor()
        result.execute("Update temp_users set party={}".format(probability) + " where userid="+str(ID[0]))
        label = conn.cursor()
        label.execute("Select party from temp_users where userid="+str(ID[0]))
        party = label.fetchone()
        print(str(party) + "sent to "+ str(ID[0]))"""


rn = input("Do you want to run this program?(y/n): ")
if rn=='y':
    create_Labels(".")
else:
    print("Program Terminated...")
