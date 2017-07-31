import numpy as np
import nltk, pickle as pkl
from nltk.tokenize import word_tokenize
from database import Database
from collections import Counter
import re
from collections import defaultdict
import time
import gensim
from gensim.models.keyedvectors import KeyedVectors
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt

from nltk.stem import WordNetLemmatizer
import re, string
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from datacollection import *
from requeteAlentite import *

# text = get_text_from_cnn("http://www.cnn.com/2017/07/28/politics/north-korea-missile-test/index.html?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+rss%2Fcnn_topstories+%28RSS%3A+CNN+-+Top+Stories%29")

# db.addDocument()

t0 = time.time()

stops = []
with open("stopwords.txt", 'r') as r:
    for line in r:
        stops += [i.strip() for i in line.split('\t')]

print("Loaded Stop Words", flush = True)

db = Database("database.pkl")
db.clear()
print("cleared db")
url = "http://www.cnn.com/2017/07/31/health/climate-change-two-degrees-studies/index.html?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+rss%2Fcnn_topstories+%28RSS%3A+CNN+-+Top+Stories%29"
text = get_text_from_cnn(url)
print("Loaded text")
db.addDocument(url, text)
sentences = summarize(db, url, stops, summarizeLength = 7)
title = sentences[0]
sentences = sentences[1:]
print("Title: {}".format(title))
for sentence in sentences:
	print(sentence)
db.removeDocument(url)

t1 = time.time()
print("elapsed " + str(t1 - t0) + "s")