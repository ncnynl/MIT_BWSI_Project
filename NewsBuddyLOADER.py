from flask import Flask
from flask_ask import Ask, statement, question
import requests
import time 
import unidecode 
import json 
from newsbuddy.database import Database
from newsbuddy.querying import getEntities
from newsbuddy.querying import getTopEntities
from newsbuddy.SearchEngine import SearchEngine
from newsbuddy.summarize import summarize
from newsbuddy.nlp_stock import stop_words
from newsbuddy.datacollection import *


db = Database(file = "./newsbuddy/database.pkl")

url = "https://en.wikipedia.org/wiki/Mathematics"
rawText = get_text_from_wikipedia(url)
db.addDocument(url, rawText)
#print(summarize(db, url, stop_words()))
#print(len(summarize(db, url, stop_words())))