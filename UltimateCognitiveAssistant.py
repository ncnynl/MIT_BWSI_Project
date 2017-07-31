from flask import Flask
from flask_ask import Ask, statement, question
import requests
import time
import unidecode
import json

app = Flask(__name__)
ask = Ask(app, '/')

@app.route('/')
def homepage():
    return "YEAH BOI!!!!!!!!!!!"

@ask.launch
def start_skill():
    msg = "Hello. My name is Sanjay Suraysh Rohan Gupta, but you can call me Alexa. Would you like to hear some news?"
    return question(msg)


@ask.intent("YesIntent")
def askWhichType():
    newsQ = "Alright. Let me know what you want to know about?"
    return question(newsQ)

@ask.intent("NoIntent")
def no_intent():
    msg = "Awkward. Next time you launch this app. Let me do something useful for once."
    return statement(msg)

@ask.intent("OptionOneIntent")
def oneIntent(term):
    from SearchEngine import SearchEngine
    #db = loadDatabase()
    SE = SearchEngine()
    return statement(SE.query(term))

@ask.intent("OptionTwoIntent")
def secondIntent(entity):
    from TopEntities import getTopEntities
    db = loadDatabase()
    return statement(getTopThreeEntities(db,entity))

@ask.intent("OptionThreeIntent")
def thirdIntent(query):
    from requeteAlentite import getEntities
    db = loadDatabase()
    return statement(getEntities(db,query))

def loadDatabase():
    from database import Database
    db = Database("database.pkl")
    return db


if __name__ == '__main__':
    app.run(debug=True)

