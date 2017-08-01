from flask import Flask
from flask_ask import Ask, statement, question
import requests
import time 
import unidecode 
import json 
from newsbuddy.database import Database
from newsbuddy.querying import getEntities
from newsbuddy.querying import getTopEntities
from newsbuddy.SearchEngine import query

db = Database("database.pkl")
app = Flask(__name__)
ask = Ask(app, '/')
Input = ""
Query = ""
Entity = ""

@app.route('/')
def homepage():
    return "Hello, this is the natural language processing capstone"

@ask.launch
def start_skill():
    msg = "Hello. What would you like to know more about?"
    return question(msg)

@ask.intent("getInputIntent")
def askWhichType(input):
    global Input
    Input = "{}".format(query)
    newsQ = "Alright. Please specify if you this is an entity or query"
    return question(newsQ)

@ask.intent("QueryIntent")
def askWhichQueryType():
    global Query
    Query = Input
    msg = "Do you want a list of documents or a list of entities relating to this query"
    return question(msg)

@ask.intent("EntityIntent")
def entityToEntity():
    global Entity
    Entity = Input
    finalEnts = getTopEntities(Entity, db)
    if len(finalEnts) == 1:
        image_msg = "The top entity is {}".format(finalEnts[0])
        return statement(image_msg)
    elif len(finalEnts) == 2:
        image_msg = "The top entities are {}".format(finalEnts[0]) + " and " + "{}".format(finalEnts[1])
        return statement(image_msg)
    image_msg = "The top entities are "
    for i in range(len(finalEnts) - 1):
        image_msg += "{}".format(finalEnts[i])
        image_msg += ", "
    image_msg += "and "
    image_msg += "{}".format(finalEnts[-1])
    return statement(image_msg)

@ask.intent("QuerytoEntityIntent")
def queryToEntity():
    finalEntities = getEntities(db, Query)
    if len(finalEntities) == 1:
        image_msg = "The top entity is {}".format(finalEntities[0])
        return statement(image_msg)
    elif len(finalEntities) == 2:
        image_msg = "The top entities are {}".format(finalEntities[0]) + " and " + "{}".format(finalEntities[1])
        return statement(image_msg)
    image_msg = "The top entities are "
    for i in range(len(finalEntities) - 1):
        image_msg += "{}".format(finalEntities[i])
        image_msg += ", "
    image_msg += "and "
    image_msg += "{}".format(finalEntities[-1])
    return statement(image_msg)

@ask.intent("QueryToDocumentIntent")
def queryToDocument():
    finalDocs = query(Query, 3)
    finalDocs = [i[0] for i in finalDocs]
    if len(finalDocs) == 1:
        image_msg = "The top document is {}".format(finalDocs[0])
        return statement(image_msg)
    elif len(finalDocs) == 2:
        image_msg = "The top documents are {}".format(finalDocs[0]) + " and " + "{}".format(finalDocs[1])
        return statement(image_msg)
    image_msg = "The top documents are "
    for i in range(len(finalDocs) - 1):
        image_msg += "{}".format(finalDocs[i])
        image_msg += ", "
    image_msg += "and "
    image_msg += "{}".format(finalDocs[-1])
    return statement(image_msg)

@ask.intent("NoIntent")
def no_intent():
    msg = "Awkward. Next time you launch this app. Let me do something useful for once."
    return statement(msg)

def loadDatabase():
    from database import Database
    db = Database("database.pkl")
    return db

if __name__ == '__main__':
    app.run(debug=True)

