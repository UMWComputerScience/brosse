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
from nltk.tokenize import RegexpTokenizer
from nltk.text import TextCollection
import operator
import random
import sklearn
#%% Functions
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
    strings = strings.replace("-","")
    strings = strings.replace("`","")
    strings = strings.replace('\'',"")
    strings = strings.replace("/", "")
    strings = strings.lower()
    return strings
def cleanup(Corpus):
    words = prettify(Corpus.raw())
    text = []
    pt = nltk.PorterStemmer()
    for file in Corpus.fileids():
        text.append(nltk.Text(Corpus.raw(file).split(" ")))
    words = [pt.stem(word) for word in words.split(" ")]
    words = [word for word in words if word not in stopwords.words('english')]
    return words, text
#%%
port = nltk.PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')
corpus_root = "/Users/bryceanderson/Desktop/brosse/TwitterStuff"
DemCorpus = PlaintextCorpusReader("./Democrat",".*\.txt")
RepCorpus = PlaintextCorpusReader("./Republican",".*\.txt")
demWords, demText = cleanup(DemCorpus)
repWords, repText = cleanup(RepCorpus)