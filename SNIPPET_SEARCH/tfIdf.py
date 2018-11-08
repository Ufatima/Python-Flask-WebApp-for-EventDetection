from __future__ import unicode_literals

import sys
from itertools import product
from nltk.corpus import stopwords,wordnet
import re, csv
from string import punctuation
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet as wn

with open('twitter_en.txt', 'r') as f:
    stopwords_list = []
    for line in f:
        stopwords_list.append(line)
    stopwords_list[:] = [line.rstrip('\n') for line in stopwords_list]

stopwords = set(stopwords.words('english'))
pun = list(punctuation)


class tf_idf(object):
    def __init__(self):
        # self.docs = docs
        pass

    def stripNonAlphaNum(self, text):
        texts = re.compile(r'\W+', re.UNICODE).split(text)
        return texts

    def removeStopwords(self, wordlist, stopwords):
        text = [w for w in wordlist if w not in stopwords]
        text = [w for w in text if not w.isnumeric()]
        return text

    def remove_punctuaions(self, wordlist, pun):
        text = [w for w in wordlist if w not in pun]
        return text

    def wordListToFreqDict(self, wordlist):
        wordfreq = [wordlist.count(p) for p in wordlist]
        return dict(zip(wordlist, wordfreq))

    def sortFreqDict(self, freqdict):
        aux = [(freqdict[key], key) for key in freqdict]
        aux.sort()
        aux.reverse()
        return aux

    def generate_tfidf_topic(self, doc_complete):
        text_string = ', '.join(doc_complete)
        fullwordlist = self.stripNonAlphaNum(text_string)
        word_list = self.removeStopwords(fullwordlist, stopwords)
        word_list = [w for w in word_list if w not in stopwords_list]
        word_list = self.remove_punctuaions(word_list, pun)
        dictionary = self.wordListToFreqDict(word_list)
        sortdict = self.sortFreqDict(dictionary)


        # extracted top 3 terms considered as an event
        top3_terms = sortdict[:3]
        tfIdf_event = []
        for s in sortdict[:3]:
            tfIdf_event.append(s[1])
        return tfIdf_event

    def generate_tfIdf_frequency_array(self, doc_complete):
        text_string = ', '.join(doc_complete)
        fullwordlist = self.stripNonAlphaNum(text_string)
        word_list = self.removeStopwords(fullwordlist, stopwords)
        word_list = [w for w in word_list if w not in stopwords_list]
        word_list = self.remove_punctuaions(word_list, pun)
        dictionary = self.wordListToFreqDict(word_list)
        sortdict = self.sortFreqDict(dictionary)
        return sortdict