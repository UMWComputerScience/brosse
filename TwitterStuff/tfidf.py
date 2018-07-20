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
import os.path
from nltk.classify import SklearnClassifier
from sklearn.svm import SVC
import random
# Given the location of a Democrat/Republican corpus, return a list of tuples,
# each of which is (0) a Series of features (whose keys are stems, and whose
# values are TF/IDF values) and (1) the class label.
def get_tfidf_featureset(
    corpus_root="/Users/bryceanderson/Desktop/brosse/TwitterStuff",
    idf_range=(.3,.6), rebuild=False):

    if not rebuild and os.path.isfile("tfidf.pickle"):
        print("* Returning pickled feature set *")
        with open("tfidf.pickle","rb") as f:
            return pickle.load(f)

    DemCorpus = PlaintextCorpusReader("./Democrat",".*\.txt")
    RepCorpus = PlaintextCorpusReader("./Republican",".*\.txt")
    FullCorpus = PlaintextCorpusReader(".", "(Republican|Democrat)/.*\.txt")

    print("processing dems...")
    demStems = classifier.get_stems_dict(DemCorpus,True)
    print("processing reps...")
    repStems = classifier.get_stems_dict(RepCorpus,True)

    print("computing IDFs...")
    fullStems = demStems.copy()
    fullStems.update(repStems)
    stemSets = { f:set(sl) for f,sl in fullStems.items() }
    listOfAllStems = list(set.union(*stemSets.values()))

    idfs = pd.Series({ stem: 
        sum([ stem in stem_list for _,stem_list in stemSets.items() ]) 
        for stem in listOfAllStems }) / len(FullCorpus.fileids())
    idfs = idfs[idfs.between(*idf_range)]

    print("computing TFs...")
    featureset = []
    for demStemDict in demStems.values():
        featureset.append((compute_tfidf(demStemDict, idfs), 'D'))
    for repStemDict in repStems.values():
        featureset.append((compute_tfidf(repStemDict, idfs), 'R'))

    print("* Pickling feature set *")
    with open("tfidf.pickle","wb") as f:
        pickle.dump((featureset,idfs),f)

    return (featureset, idfs)


# Compute the TF/IDF vector for a single item, given its dictionary of
# stems-to-counts, and the corpus's IDFs (a Series of stems-to-fractions).
def compute_tfidf(stemDict, idfs):
    tfs = pd.Series(nltk.FreqDist(stemDict))
    tfs /= tfs.sum()
    tfs = tfs.reindex(idfs.index, fill_value=0.0)
    tfs /= idfs
    return tfs



def classify_manual(the_classifier, manual_text):

    this_tfidf = compute_tfidf(classifier.get_stems(manual_text), idfs)

    probability = the_classifier.prob_classify(this_tfidf).prob('R')
    print("P(R): {:.2f}".format(probability))
    return probability

def run_cv(featureset, k=100):
    random.shuffle(featureset)
    ntrain = int(len(featureset))
    trainset = featureset[:ntrain]
    subSize = int(len(trainset)/k)
    perc = []
    for i in range(k):
        print("Testing slice " + str(i) + "...")
        correct = 0
        test = trainset[i*subSize:][:subSize]
        train = trainset[:i*subSize] + trainset[(i+1)*subSize:]
        the_classifier = SklearnClassifier(SVC(probability=True), sparse=False).train(train)
        for item in test:
            choice = ""
            probD = the_classifier.prob_classify(item[0]).prob('R')
            if probD > .5:
                choice = 'R'
            else:
                choice = 'D'
            if choice == item[1]:
                correct+=1
        perc.append((correct/len(test))*100)
    return perc

print("Building classifier...")
featureset, idfs = get_tfidf_featureset(".",rebuild=True)
nonpandas_fs = [ (s.to_dict(), l) for s,l in featureset ]
print("Running Cross Validation...")
accs = run_cv(nonpandas_fs)
print("...done!")

text = input("Enter text (or name of file in 'quotes'): ")
while text != 'done':
    if text[0] == "'" and text[-1] == "'":
        f = open(text[1:-1],"r")
        text = f.read()
    classify_manual(the_classifier, text)
    text = input("Enter text ('done' to quit): ")
