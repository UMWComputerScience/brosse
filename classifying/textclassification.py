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
import string
stopwords = set(stopwords.words('english'))
corpus_root = '/Users/bryceanderson/Desktop/brosse/classifying'
rapCorpus = PlaintextCorpusReader(corpus_root, ['rap1.txt', 'rap2.txt','rap3.txt','rap4.txt','rap5.txt'])
rockCorpus = PlaintextCorpusReader(corpus_root, ['rock1.txt', 'rock2.txt', 'rock3.txt', 'rock4.txt', 'rock5.txt', 'rock6.txt', 'rock7.txt', 'rock8.txt'])
def update_stopwords(aset):
    aset.add("'s")
    aset.add("n't")
    aset.add("'m")
    aset.add("dont")
    aset.add("im")
    return aset
stopwords = update_stopwords(stopwords)
#Make this more sexy
def prettify(strings):
    strings = strings.replace(",","")
    strings = strings.replace("'","")
    strings = strings.replace("."," ")
    strings = strings.replace("!"," ")
    strings = strings.replace("?"," ")
    strings = strings.replace('"',"")
    strings = strings.replace(";","")
    strings = strings.replace(":","")
    strings = strings.replace("\n"," ")
    strings = strings.replace("(","")
    strings = strings.replace(")","")
    strings = strings.replace("-","")
    strings = strings.replace("`","")
    strings = strings.replace('\'',"")
    strings = strings.lower()
    return strings
#Pulls words form slected corpus and returns a list of the raw lyrics and Text object
def getLyrics(Corpus):
    lyrics = []
    text = []
    for file in Corpus.fileids():
        temp = ""
        temp += Corpus.raw(file)
        temp = prettify(temp)
        lyrics.append(temp)
        text.append(nltk.Text(temp.split(" ")))
    return lyrics, text
def portStem(listofStrings):
    for i in range(len(listofStrings)):
        temp = ""
        for word in listofStrings[i].split(" "):
            temp += port.stem(word) + " "
        listofStrings[i] = temp
    return listofStrings
#%%
lm = nltk.WordNetLemmatizer()
port = nltk.PorterStemmer()
lanc = nltk.LancasterStemmer()
rapLyrics, rapText = getLyrics(rapCorpus)
rockLyrics, rockText = getLyrics(rockCorpus)
rapLyrics = portStem(rapLyrics)
rockLyrics = portStem(rockLyrics)
allWords = Counter(nltk.word_tokenize(" ".join(rapLyrics))) + Counter(nltk.word_tokenize(" ".join(rockLyrics)))
sortVocab = sorted(allWords.items(), reverse=True, key=operator.itemgetter(1))
words_features = list(sortVocab)[:100]

# For every word in the features list check to see if it exist in the song label (True || False)
def song_features(text):
    words = set(text)
    features = {}
    for word in words_features:
        features["has({})".format(word[0])] = (word[0] in words)
    return features

# For every song in ___Text run song_features and create a tuple with those features
featuresets = [(song_features(r), 'rap') for r in rapText]
featuresets += [(song_features(r), 'rock') for r in rockText]
random.shuffle(featuresets)
ntrain = int(len(featuresets) * .7)
trainset, testset = featuresets[:ntrain], featuresets[ntrain:]
rapOrRock = nltk.NaiveBayesClassifier.train(trainset)
rapOrRock.show_most_informative_features(10)
probs = []
for item in testset:
    probs.append("Rap: "+ str(rapOrRock.prob_classify(item[0]).prob('rap'))+ " Rock: " + str(rapOrRock.prob_classify(item[0]).prob('rock')))
print(probs)

