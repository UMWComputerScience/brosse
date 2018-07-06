#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 17:32:30 2018

@author: bryceanderson
"""
from nltk.corpus import stopwords
import nltk
port = nltk.PorterStemmer()
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
    return words, text


def portStem(listofStrings):
    for i in range(len(listofStrings)):
        temp = ""
        for word in listofStrings[i].split(" "):
            temp += port.stem(word) + " "
        listofStrings[i] = temp
    return listofStrings

def noHandles(string):
    tm = ""
    text = string
    words = [word for word in text.split(" ") if "@" not in word]
    for word in words:
        tm += word + " "
    return tm

def noStopWords(string):
    tm = ""
    text = string
    words = [word for word in text.split(" ") if word not in stopwords.words('english')]
    for word in words:
        tm += word + " "
    return tm