from database import Database
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
import re, string
from nlp_stock import strip_punc

Title = "" #Title of the document AFTER calling summarize function

def summarize(db, documentID, stop_words, summarizeLength = 4):
	"""
	Parameters: Instance of database, Document URL, stop words, a keyword argument of how many sentences 
	the user wants the summary to be.  
	
	##I NEED SKIES DOCUMENTATION OF WHAT THIS FUNCTION DOES

	Return: The summary of the article specified
	"""
	#algorithm sourced from smmry.com
	lemmatizer = WordNetLemmatizer()
	stemmer = LancasterStemmer()
	extra_abbreviations = ['dr', 'vs', 'mr', 'mrs', 'prof', 'inc', 'i.e']
	sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	sentence_tokenizer._params.abbrev_types.update(extra_abbreviations)
	texteBrut = db.engine.raw_text[documentID]
	stripped = strip_punc(texteBrut)
	listeDesMots = word_tokenize(stripped)
	listeDesPhrases = nltk.sent_tokenize(texteBrut)
	title, first_sent = (listeDesPhrases[0].split("\n\n")[0], listeDesPhrases[0].split("\n\n")[1])
	global Title
	Title = title
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
	Parameters weights: Counter, sentence: string
	#I NEED SKIES DOCUMENTATION
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

def getTitle():
	"""
	Gets Title
	Return: Title of the document 
	"""
	return "{}".format(Title)