#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 16:19:57 2018

@author: bryceanderson
"""

import nltk
from nltk.corpus import stopwords
from collections import Counter
from nltk.corpus import PlaintextCorpusReader
from nltk.text import TextCollection
import operator
import random
import sklearn
import re
#%% Functions
port = nltk.PorterStemmer()
def update_stopwords(aset):
    aset.add("'s")
    aset.add("n't")
    aset.add("'m")
    aset.add("dont")
    aset.add("im")
    return aset
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
    strings = strings.replace("`","")
    strings = strings.replace('\'',"")
    strings = strings.replace("/", "")
    strings = strings.lower()
    return strings

def cleanup(Corpus):
    words = []
    text = []
    for file in Corpus.fileids():
        temp = Corpus.raw(file)
        temp = prettify(temp)
        words.append(temp)
        text.append(nltk.Text(nltk.word_tokenize(temp)))
    print(text[0])
    return words, text

def portStem(listofStrings):
    for i in range(len(listofStrings)):
        temp = ""
        for word in listofStrings[i].split(" "):
            temp += port.stem(word) + " "
        listofStrings[i] = temp
    return listofStrings

#%%
corpus_root = "/Users/bryceanderson/Desktop/brosse/TwitterStuff"
DemCorpus = PlaintextCorpusReader("./Democrat",".*\.txt")
RepCorpus = PlaintextCorpusReader("./Republican",".*\.txt")
demWords, demText = cleanup(DemCorpus)
repWords, repText = cleanup(RepCorpus)
#%%
demWords = portStem(demWords)
repWords = portStem(repWords)
totVocab = nltk.FreqDist(nltk.word_tokenize(" ".join(demWords))) + nltk.FreqDist(nltk.word_tokenize(" ".join(repWords)))
#%%
sortedVocab = sorted(totVocab.items(), reverse=True, key=operator.itemgetter(1))
word_features = list(sortedVocab)[:int(len(totVocab)*.01)]
def getFeatures(text):
    words = set(text)
    features = {}
    for word in word_features:
        features["has({})".format(word[0])] = (word[0] in words)
    return features
featureset = [(getFeatures(t), 'D') for t in demText]
featureset += [(getFeatures(t), 'R') for t in repText]
random.shuffle(featureset)
ntrain = int(len(featureset) * .7)
trainset, testset = featureset[:ntrain], featureset[ntrain:]
classifier = nltk.NaiveBayesClassifier.train(trainset)
classifier.show_most_informative_features(5)
#%%

perc = []

for i in range(100):
    correct = 0
    for item in testset:
        choice = ""
        probD = classifier.prob_classify(item[0]).prob('D')
        probR = classifier.prob_classify(item[0]).prob('R')
        if probD > probR:
            choice = 'D'
        else:
            choice = 'R'
        if choice == item[1]:
            correct+=1
    perc.append(100*(correct/len(testset)))
    print(str(i) + "...")
print(sum(perc)/100)