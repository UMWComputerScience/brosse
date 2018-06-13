#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 14:34:15 2018

@author: bryceanderson
"""

import nltk
from nltk.corpus import stopwords
from collections import Counter
from nltk.corpus import PlaintextCorpusReader
import operator
import random
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
#Make this more sexy
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

#%%
#doc = open('raplyrics.txt','r')
#rockdoc = open('rocklyrics.txt','r')
#raw=doc.read()
#rockraw = rockdoc.read()
#raw = prettify(raw)
#rockraw = prettify(rockraw)
#rapfreq = prep(raw, stopwords)
#rockfreq = prep(rockraw, stopwords)
#Want a list of strings containing the lyrics to each song (by genre)
#Want a list of Text objects that contain each song (by genre)
def getLyrics(Corpus):
    lyrics = []
    text = []
    for file in Corpus.fileids():
        temp = ""
        temp += rapCorpus.raw(file)
        temp = prettify(temp)
        lyrics.append(temp)
        text.append(nltk.Text(temp.split(" ")))
    return lyrics, text
rapLyrics, rapText = getLyrics(rapCorpus)
rockLyrics, rockText = getLyrics(rockCorpus)
allWords = Counter(nltk.word_tokenize(" ".join(rapLyrics))) + Counter(nltk.word_tokenize(" ".join(rockLyrics)))
sortVocab = sorted(allWords.items(), reverse=True, key=operator.itemgetter(1))
word_features = list(sortVocab)[:100]

# For every word in the features list check to see if it exist in the song label (True || False)w
def song_features(text):
    words = set(text)
    features = {}
    for word in word_features:
        features["has({})".format(word[0])] = [word[0] in words]
    return features

# For every song in ___Text run song_features and create a tuple with those features
featuresets = [(song_features(r), 'rap') for r in rapText]
featuresets += [(song_features(r), 'rock') for r in rockText]
random.shuffle(featuresets)
ntrain = int(len(featuresets) * .7)
trainset, testest = featuresets[:ntrain], featuresets[ntrain:]
rapOrRock = nltk.NaiveBayesClassifier.train(trainset)
