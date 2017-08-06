from flask import Flask
from flask_ask import Ask, statement, question
import requests
import time 
import unidecode 
import json 
from database import Database
from querying import getEntities
from querying import getTopEntities
from SearchEngine import SearchEngine
from summarize import summarize
from nlp_stock import stop_words
from datacollection import *
import feedparser


db = Database(file = "./database.pkl")
db.clear()

cnn_texts = feedparser.parse("http://www.cnn.com/services/rss/")["entries"]
reuters_texts = feedparser.parse("http://feeds.reuters.com/reuters/topNews")["entries"]
wiki_urls = ["https://en.wikipedia.org/wiki/Mathematics"]

for url in wiki_urls:
	rawText = get_text_from_wikipedia(url)
	db.addDocument(url, rawText)
for entry in cnn_texts:
	url= entry["link"]
	rawText = get_text_from_cnn(url)
	db.addDocument(url, rawText)
for entry in reuters_texts:
	url = entry["link"]
	rawText = get_text_from_reuters(url)
	db.addDocument(url, rawText)