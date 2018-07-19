#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: stephen
"""
from nltk.corpus import stopwords
from nltk.corpus import PlaintextCorpusReader
import nltk
import pickle
import classifier
import pandas as pd

# Given the location of a Democrat/Republican corpus, return a list of tuples,
# each of which is (0) a Series of features (whose keys are stems, and whos
# values are TF/IDF values) and (1) the class label.
def get_tfidf_featureset(
    corpus_root="/Users/bryceanderson/Desktop/brosse/TwitterStuff"):

    DemCorpus = PlaintextCorpusReader("./Democrat",".*\.txt")
    RepCorpus = PlaintextCorpusReader("./Republican",".*\.txt")
    FullCorpus = PlaintextCorpusReader(".", "(Republican|Democrat)/.*\.txt")

    print("processing dems...")
    demStems = classifier.get_stems_dict(DemCorpus,True)
    print("processing reps...")
    repStems = classifier.get_stems_dict(RepCorpus,True)

    fullStems = demStems.copy()
    fullStems.update(repStems)
    stemSets = { f:set(sl) for f,sl in fullStems.items() }
    listOfAllStems = list(set.union(*stemSets.values()))

    print("computing IDFs...")
    idfs = {}
    for i in range(len(listOfAllStems)):
        print("Stem {} of {}...".format(i+1,len(listOfAllStems)))
        idfs[listOfAllStems[i]] = \
            sum([ listOfAllStems[i] in stem_list 
                for _,stem_list in stemSets.items() ]) 
    idfs = pd.Series(idfs)
    with open('idfs.pickle','wb') as f:
        pickle.dump(idfs,f)
        
    #idfs = pd.Series({ stem: 
    #    sum([ stem in stem_list for f,stem_list in fullStems.items() ]) 
    #    for stem in allStems })
    idfs /= len(idfs)
    import ipdb; ipdb.set_trace()
    sortedVocab = sorted(totVocab.items(), reverse=True, key=operator.itemgetter(1))
    print("building word features...")
    word_features = list(sortedVocab)[:int(len(totVocab)*.01)]
    featureset = [(getFeatures(word_features, t), 'D') for t in demText]
    featureset += [(getFeatures(word_features, t), 'R') for t in repText]
    with open("./featureset.pickle", "wb") as f:
        pickle.dump(featureset, f)
    with open("./wfeatures.pickle", "wb") as f:
        pickle.dump(word_features, f)
    return word_features, featureset


# (ignore from here down. :)
def classify_manual(corpus_root, manual_text):

    print("Building classifier...")
    word_features, classify = get_tfidf_featureset(corpus_root)

    #Actual classifier below. Use to get probability
    DemorRep = nltk.NaiveBayesClassifier.train(classify)
    print("...built!")

    text = manual_text
    #print("text = {}".format(text))
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
    textFeatures = classifier.getFeatures(word_features,text)         #<----
    print([ f for f in textFeatures if textFeatures[f] ])
    probability = DemorRep.prob_classify(textFeatures).prob('R')
    print("P(R): {:.2f}".format(probability))

#with open("wfeatures.pickle","rb") as f:
#    word_features = pickle.load(f)
#with open("featureset.pickle", "rb") as f:
#    featureset = pickle.load(f)

text = input("Enter text (or name of file in 'quotes'): ")
while text != 'done':
    if text[0] == "'" and text[-1] == "'":
        f = open(text[1:-1],"r")
        text = f.read()
    classify_manual(".", text)
    text = input("Enter text ('done' to quit): ")
