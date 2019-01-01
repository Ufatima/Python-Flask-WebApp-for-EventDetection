import csv
import re
from string import punctuation
from pathlib import Path
from nltk import WordNetLemmatizer, wordnet
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

from string import punctuation
import numpy as np
from nltk.corpus import stopwords, wordnet

with open('twitter_en.txt', 'r') as f:
    stopwords_list = []
    for line in f:
        stopwords_list.append(line)
    stopwords_list[:] = [line.rstrip('\n') for line in stopwords_list]
stopwords = set(stopwords.words('english'))


class lda_modeling(object):

    def __init__(self):
        # self.docs = docs
        pass

    def display_topics(self, H, W, feature_names, documents, no_top_words, no_top_documents):
        topics = []
        for topic_idx, topic in enumerate(H):
            # print("Topic %d:" % (topic_idx))
            topic = " ".join([feature_names[i]
                              for i in topic.argsort()[:-no_top_words - 1:-1]])
            topics.append(topic)
        return topics

    def generate_topic(self, doc_complete):
        lemma = WordNetLemmatizer()
        normalized_texts = []
        for doc in doc_complete:
            doc = doc.replace("#", "").replace("_", " ")  # Removing HASH symbol
            doc = re.sub(r'[^\x00-\x7f]', r'', doc)  # Removing the Hex characters(emoji)
            stop_free = " ".join([i for i in doc.lower().split() if i not in stopwords])
            stop_free = " ".join([i for i in stop_free.lower().split() if i not in stopwords_list])
            # removing punctuations
            text = re.sub(r'[^a-zA-Z0-9@\S]', ' ', stop_free)
            remove_pun = str.maketrans({key: None for key in punctuation})
            punc_free = text.translate(remove_pun)
            normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
            normalized_texts.append(normalized)
        # print(normalized_texts)

        # Remove new line characters
        documents = [re.sub('\s+', ' ', sent) for sent in normalized_texts]
        # Remove distracting single quotes
        documents = [re.sub("\'", "", sent) for sent in documents]

        # LDA can only use raw term counts for LDA because it is a probabilistic graphical model
        no_features = 1000
        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=0.03, max_features=no_features, stop_words='english')
        tf = tf_vectorizer.fit_transform(documents)
        tf_feature_names = tf_vectorizer.get_feature_names()

        no_topics = 5

        # Run LDA
        lda_model = LatentDirichletAllocation(n_topics=no_topics, max_iter=5, learning_method='online',
                                              learning_offset=50.,
                                              random_state=0).fit(tf)
        lda_W = lda_model.transform(tf)
        lda_H = lda_model.components_

        no_top_words = 5
        no_top_documents = 3
        lda_topic = self.display_topics(lda_H, lda_W, tf_feature_names, documents, no_top_words, no_top_documents)
        return lda_topic
