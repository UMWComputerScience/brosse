#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 14:34:15 2018

@author: bryceanderson
"""

import nltk
from nltk.corpus import stopwords
import os
import operator
from nltk.corpus import PlaintextCorpusReader
stopwords = set(stopwords.words('english'))
corpus_root = '/Users/bryceanderson/Desktop/brosse/classifying'
rapCorpus = PlaintextCorpusReader(corpus_root, ['rap1.txt', 'rap2.txt','rap3.txt','rap4.txt','rap5.txt'])
rockCorpus = PlaintextCorpusReader(corpus_root, ['rock1.txt', 'rock2.txt', 'rock3.txt', 'rock4.txt', 'rock5.txt'])
def update_stopwords(aset):
    aset.add("'s")
    aset.add("n't")
    aset.add("'m")
    aset.add("dont")
    aset.add("im")
    return aset
stopwords = update_stopwords(stopwords)
def prettify(string):
    string = string.replace(",","")
    string = string.replace("'","")
    string = string.replace("."," ")
    string = string.replace("!"," ")
    string = string.replace("?"," ")
    string = string.replace('"',"")
    string = string.replace(";","")
    string = string.replace(":","")
    string = string.replace("\n"," ")
    string = string.replace("(","")
    string = string.replace(")","")
    string = string.replace("-","")
    string = string.replace("`","")
    string = string.replace('\'',"")
    string = string.lower()
    return string
#Tokenizes and orders words based on frequency
def prep(string, stopwords):
    zipwords = []
    tokens = nltk.word_tokenize(string)
    tokens = nltk.Text(tokens)
    filtered_tokens = []
    for w in tokens:
        if w not in stopwords:
            filtered_tokens.append(w)
        allwords = nltk.FreqDist(w.lower() for w in filtered_tokens)
        wds = list(allwords.keys())
        vals = list(allwords.values())
        zipwords = zip(vals, wds)
        zipwords = sorted(zipwords, reverse=True)
    return zipwords
def readlyrics(genre, emptylist):
    song = ""
    for rock, dirs, files in os.walk("/Users/bryceanderson/Desktop/brosse/classifying"):
        for f in files:
            if genre in f:
                emptylist.append(f)
        for file in emptylist:
            with open(file, 'r') as q:
                song += q.read()
    return song
#%%
#doc = open('raplyrics.txt','r')
#rockdoc = open('rocklyrics.txt','r')
#raw=doc.read()
#rockraw = rockdoc.read()
#raw = prettify(raw)
#rockraw = prettify(rockraw)
#rapfreq = prep(raw, stopwords)
#rockfreq = prep(rockraw, stopwords)
#Clean set of corpus words
rapWords = set(rapCorpus.words())
rockWords = set(rockCorpus.words())
def cleanSet(aset):
    badwords = []
    temp = aset
    for word in aset:
        if word in stopwords:
            badwords.append(word)
    print(badwords)
    for word in badwords:
        temp.remove(word)
    return temp
rapWords = cleanSet(rapWords)
rockWords = cleanSet(rockWords)
rap_files, r_files = [], []
raps = readlyrics('rap', rap_files)
rap_text = readlyrics('rap', r_files)
raps, rap_text = prettify(raps), prettify(rap_text)
raps = prep(raps, stopwords)
rock_files = []
rock = readlyrics('rock', rock_files)
rock = prettify(rock)
rock = prep(rock, stopwords)
#Combine the sets of vocabulary then do the sorting stuff. Text object any particularly reason.
all_words = raps + rock
all_words = sorted(all_words, reverse=True, key=operator.itemgetter(0))
rap_features = list(raps)[:75]
rock_features = list(rock)[:75]
word_features = list(all_words)[:100]

def song_features(text):
    words = set(text)
    print(words)
    features = {}
    for word in word_features:
        features["has({})".format(word[0])] = [word[0] in words]
    return features

#featuresets = [(song_features(r), 'rap') for r in ]






















