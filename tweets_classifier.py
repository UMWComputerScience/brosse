#!/usr/bin/env python3

# See section 1.3 of
# https://www.nltk.org/book/ch06.html#ref-document-classify-set/document-classification

import nltk
import operator
import random
import sys
import os
import re
import string

PROPORTION_TRAINING = .7      # Proportion of set to train on
NUM_FEATURES_TO_RETAIN = 200  # We'll use only this many most common words
NUM_MOST_INFO = 20            # Print out this many most informative features


if len(sys.argv) != 3:
    sys.exit("Usage: suck_tweets.py screenname1 screenname2.")
screennames = [ sys.argv[1], sys.argv[2] ]
for i in range(len(screennames)):
    if screennames[i][0] == '@': screennames[i] = screennames[i][1:]

def compile_texts(screenname):
    if not os.path.exists(screenname + ".tweets"):
        sys.exit("No file {}.tweets (run suck_recent_tweets.py first.)".format(
            screenname))
    with open("{}.tweets".format(screenname),"r") as f:
        tweets = f.readlines()
        texts = [ nltk.word_tokenize(
            re.sub('['+string.punctuation+']','',t.lower())) for t in tweets ]
    return texts

texts0 = compile_texts(screennames[0])
texts1 = compile_texts(screennames[1])
texts = texts0.copy()
texts.extend(texts1)
all_vocab = nltk.FreqDist([ word for text in texts for word in text ])
sorted_words = sorted(all_vocab.items(), reverse=True, 
    key=operator.itemgetter(1))
word_features = list(sorted_words)[:NUM_FEATURES_TO_RETAIN]


def tweet_features(text):
    tweet_words = set(text)
    features = {}
    for word in word_features:
        features['has({})'.format(word[0])] = (word[0] in tweet_words)
    return features

featuresets = [(tweet_features(t), screennames[0]) for t in texts0 ]
featuresets += [(tweet_features(t), screennames[1]) for t in texts1 ]
random.shuffle(featuresets)
ntrain = int(len(featuresets) * PROPORTION_TRAINING)
train_set, test_set = featuresets[:ntrain], featuresets[ntrain:]
classifier = nltk.NaiveBayesClassifier.train(train_set)

print("Here's the top {} most informative features:".format(NUM_MOST_INFO))
classifier.show_most_informative_features(NUM_MOST_INFO)

tweet = input("\nEnter a sample tweet ('done' to quit): ")
while tweet not in ["done","'done'"]:
    probs = classifier.prob_classify(tweet_features(
        nltk.word_tokenize(tweet.lower())))
    for sn in screennames:
        print("@{} probability: {:.3f}%".format(sn,100 * probs.prob(sn)))
    tweet = input("\nEnter a sample tweet: ")

