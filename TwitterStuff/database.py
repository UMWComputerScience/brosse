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
import classifier 
import pickle

def create_Labels(corpus_root, word_features=None, classify=None):
    print("Building classifier...")
    if not word_features:
        word_features, classify = classifier.get_featureset(corpus_root)
    #Actual classifier below. Use to get probability
    DemorRep = nltk.NaiveBayesClassifier.train(classify)
    print("...built!")
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
        print("Prettifying...")
        text = classifier.prettify(text) #Make a module file for these methods
        print("De-Handlefying...")
        text = classifier.noHandles(text)                               #<----
        print("De-Stopwordifying...")
        text = classifier.noStopWords(text)                                #<----
        print("Creating FreqDist...")
        text = sorted(nltk.FreqDist(nltk.Text(nltk.word_tokenize(text))))
        print("Creating feature list for user...")
        textFeatures = classifier.getFeatures(word_features,text)                        #<----
        probability = DemorRep.prob_classify(textFeatures).prob('R')
        probability = (probability * 2) - 1
        print("PROB({}): ".format(ID[0]))
        result = conn.cursor()
        result.execute("Update temp_users set party={}".format(probability) + " where userid="+str(ID[0]))


# insert pickle code here
# to hydrate the word_features object and the featureset object from the
# pickle file
with open("wfeatures.pickle","r") as f:
    word_features = pickle.load(f)
with open("featureset.pickle", "r") as f:
    featureset = pickle.load(f)
create_Labels(".", word_features, featureset)
