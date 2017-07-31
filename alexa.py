from flask import Flask
from flask_ask import Ask, statement, question
import requests
import time
import unidecode
import json

app = Flask(__name__)
ask = Ask(app, '/')
db = Database("database.pkl")

@app.route('/')
def homepage():
    return "Hello"

@ask.launch
def start_skill():
    msg = "Hello. Would you like to enter a Query or Entity"
    return question(msg)

def get_headlines():
    # Don't worry about this implementation yet. Just return a string.
    return "Newsy news, blah blah weather news news."

@ask.intent("QueryIntent")
def get_Similar_Entities(Slot1, NumEntities = 5): #option #3
    entities = getEntities(db, slot1, NumEntities)
    entity_msg = "The most similar entities are, {}".format(entity for entity in entities)
    return statement(entity_msg)

@ask.intent("TermIntent") #option #1
def get_all_docs():
    pass

@ask.intent("") #fill in the last entity name (for option #2)
def get_top_entities():
    pass

@ask.intent("CancelIntent")
def no_intent():
    msg = "Ok, thanks. Have a nice day."
    return statement(msg)

if __name__ == '__main__':
    app.run(debug=True)
