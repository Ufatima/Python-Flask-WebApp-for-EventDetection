from sys import path
from pathlib import Path, PureWindowsPath
path.extend(['SNIPPET_SEARCH'])
from os import path
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS



from SNIPPET_SEARCH.snippet_search import SNIPPET_SEARCH
from SNIPPET_SEARCH.LDA import lda_modeling
from SNIPPET_SEARCH.tfIdf import tf_idf

filename = Path("C:/Users/spark/PycharmProjects/webapp/snippet_twitter.txt")

class SnippetInstance(object):
    def __init__(self):
        self.snippets_ob = SNIPPET_SEARCH()
        self.lda_ob = lda_modeling()
        self.tf_idf_ob = tf_idf()


    def snippets(self, str_input, date, number):
        result = self.snippets_ob.snippets(str_input, date, number)
        return result


    def generate_topic(self, result):
        lda_topics = self.lda_ob.generate_topic(result)
        return lda_topics


    def generate_tfidf_topic(self, result):
        tf_idf_topic = self.tf_idf_ob.generate_tfidf_topic(result)
        return tf_idf_topic


    def create_wordcloud(self):
        file = open("snippet_twitter.txt", "r", encoding='utf8')
        text = file.read()
        currdir = path.dirname(__file__)

        # create numpy araay for wordcloud mask image
        mask = np.array(Image.open(path.join(currdir, "cloud.png")))

        # create set of stopwords
        stopwords = set(STOPWORDS)

        # create wordcloud object
        wc = WordCloud(background_color="white",
                       max_words=200,
                       mask=mask,
                       stopwords=stopwords)

        # generate wordcloud
        wc.generate(text)

        # save wordcloud
        wc.to_file(path.join(currdir, "static/img/h.jpg"))


    def create_tf_idf_dic(self, result):
        tf_idf_sorted_dictionary = self.tf_idf_ob.generate_tfIdf_frequency_array(result)
        return tf_idf_sorted_dictionary

