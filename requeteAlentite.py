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
from nltk.stem.lancaster import LancasterStemmer
import re, string

def getEntities(db, query, topEntities = 5):
	documents = db.engine.query(query) 	
	listeDesMots = [] #this will be a list with listOfEntities
	for documentID, score in documents: #this loops translates ID's to text and tokenizes them. 
		listeDesMots += db.entities[documentID]
	compter = Counter(listeDesMots)
	compter[query] = 0
	lePlusCommun = compter.most_common(topEntities)
	listeDesEntitesCommunes = [i[0] for i in lePlusCommun]
	queryList = query.split()
	for word in queryList:
		if (word in listeDesEntitesCommunes):
			pass
	if (len(listeDesEntitesCommunes) == 0):
		return "Sorry, no entries were found"
	return listeDesEntitesCommunes

def strip_punc(corpus):
	punc_regex = re.compile('[{}]'.format(re.escape(string.punctuation)))
	return punc_regex.sub('', corpus)

def summarize(db, documentID, stop_words, summarizeLength = 7): #attempts to summarize document
	#algorithm sourced from smmry.com
	# gant = downloadGlove()
	lemmatizer = WordNetLemmatizer()
	stemmer = LancasterStemmer()
	extra_abbreviations = ['dr', 'vs', 'mr', 'mrs', 'prof', 'inc', 'i.e']
	sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	sentence_tokenizer._params.abbrev_types.update(extra_abbreviations)

	texteBrut = db.engine.raw_text[documentID]
	stripped = strip_punc(texteBrut)
	listeDesMots = word_tokenize(stripped)
	listeDesPhrases = nltk.sent_tokenize(texteBrut)
	# print(listeDesPhrases[0].split("\n\n"), flush= True)
	title, first_sent = (listeDesPhrases[0].split("\n\n")[0], listeDesPhrases[0].split("\n\n")[1])
	listeDesPhrases[0] = first_sent
	
	listeDesRacines = []
	for mot in listeDesMots:
		racineDuMot = stemmer.stem(lemmatizer.lemmatize(mot))
		if mot not in stop_words and racineDuMot not in stop_words:
			listeDesRacines.append(racineDuMot)

	compteDesRacines = Counter(listeDesRacines) 
	sentence_scores = []
	for i, sentence in enumerate(listeDesPhrases):
		sentence_scores.append((score_sentence(sentence, compteDesRacines, stop_words), i))

	top_indices = [i for score, i in sorted(sorted(sentence_scores, key=lambda x: x[0], reverse = True)[:summarizeLength], key = lambda x:x[1])]
	if 0 not in top_indices:
		top_indices.insert(0, 0)
	return [title] + [listeDesPhrases[i] for i in top_indices]

def score_sentence(sentence, weights, stop_words):
	"""
	weights: Counter
	sentence: string
	"""
	lemmatizer = WordNetLemmatizer()
	stemmer = LancasterStemmer()
	sentence = strip_punc(sentence)
	tokens = word_tokenize(sentence)
	score = 0
	for token in tokens:
		root = stemmer.stem(lemmatizer.lemmatize(token))
		if token not in stop_words and root not in stop_words:
			score += weights[root] 
	score = sum([weights[stemmer.stem(lemmatizer.lemmatize(token))] for token in tokens if token not in stop_words and stemmer.stem(lemmatizer.lemmatize(token)) not in stop_words])
	return score

def downloadGlove():
	chemin = "C:/glove/glove.6B.50d.txt.w2v"
	gant = KeyedVectors.load_word2vec_format(chemin, binary=False)
	return gant


