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
    return "ddddd"

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
    from ..MITThirdProject.NewsBuddy.SearchEngine import query
    #db = loadDatabase()
    return statement(query(term))

@ask.intent("OptionTwoIntent")
def secondIntent(entity):
    from ..MITThirdProject.NewsBuddy.TopEntities import getTopThreeEntities
    db = loadDatabase()
    return statement(getTopThreeEntities(db,entity))

@ask.intent("OptionThreeIntent")
def thirdIntent(query):
    from ..MITThirdProject.NewsBuddy.requeteAlentite import getEntities
    db = loadDatabase()
    return statement(getEntities(db,query))

def loadDatabase():
    from ..MITThirdProject.NewsBuddy.database import Database
    db = Database("C:/Users/nares_000/PycharmProjects/NewMITCodeSurface/MITThirdProject/NewsBuddy/database.pkl")
    return db


if __name__ == '__main__':
    app.run(debug=True)

