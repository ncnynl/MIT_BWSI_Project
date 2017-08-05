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


db = Database(file = "./database.pkl")
db.clear()
cnn_texts = collect("http://rss.cnn.com/rss/cnn_topstories.rss")
reuters_texts = collect("http://feeds.reuters.com/reuters/topNews")
wiki_urls = ["https://en.wikipedia.org/wiki/Mathematics", ]
rawText = get_text_from_wikipedia(url)
db.addDocument(url, rawText)
