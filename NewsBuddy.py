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
from newsbuddy.summarize import getTitle
from newsbuddy.nlp_stock import stop_words
from newsbuddy.datacollection import *
 
db = Database(file = "./newsbuddy/database.pkl")
app = Flask(__name__)
ask = Ask(app, '/')
Input = "" #If the search input is an entity or a query
Query = "" #Stores the query
Entity = "" #stores the entity
TotalDocs = [] #The list of documents returned from a query
stopwords = "a,able,about,above,according,accordingly,across,actually,after,afterwards,again,against,ain't,all,allow,allows,almost,alone,along,already,also,although,always,am,among,amongst,an,and,another,any,anybody,anyhow,anyone,anything,anyway,anyways,anywhere,apart,appear,appreciate,appropriate,are,aren't,around,as,aside,ask,asking,associated,at,available,away,awfully,be,became,because,become,becomes,becoming,been,before,beforehand,behind,being,believe,below,beside,besides,best,better,between,beyond,both,brief,but,by,c'mon,c's,came,can,can't,cannot,cant,cause,causes,certain,certainly,changes,clearly,co,com,come,comes,concerning,consequently,consider,considering,contain,containing,contains,corresponding,could,couldn't,course,currently,definitely,described,despite,did,didn't,different,do,does,doesn't,doing,don't,done,down,downwards,during,each,edu,eg,eight,either,else,elsewhere,enough,entirely,especially,et,etc,even,ever,every,everybody,everyone,everything,everywhere,ex,exactly,example,except,far,few,fifth,first,five,followed,following,follows,for,former,formerly,forth,four,from,further,furthermore,get,gets,getting,given,gives,go,goes,going,gone,got,gotten,greetings,had,hadn't,happens,hardly,has,hasn't,have,haven't,having,he,he's,hello,help,hence,her,here,here's,hereafter,hereby,herein,hereupon,hers,herself,hi,him,himself,his,hither,hopefully,how,howbeit,however,i'd,i'll,i'm,i've,ie,if,ignored,immediate,in,inasmuch,inc,indeed,indicate,indicated,indicates,inner,insofar,instead,into,inward,is,isn't,it,it'd,it'll,it's,its,itself,just,keep,keeps,kept,know,known,knows,last,lately,later,latter,latterly,least,less,lest,let,let's,like,liked,likely,little,look,looking,looks,ltd,mainly,many,may,maybe,me,mean,meanwhile,merely,might,more,moreover,most,mostly,much,must,my,myself,name,namely,nd,near,nearly,necessary,need,needs,neither,never,nevertheless,new,next,nine,no,nobody,non,none,noone,nor,normally,not,nothing,novel,now,nowhere,obviously,of,off,often,oh,ok,okay,old,on,once,one,ones,only,onto,or,other,others,otherwise,ought,our,ours,ourselves,out,outside,over,overall,own,particular,particularly,per,perhaps,placed,please,plus,possible,presumably,probably,provides,que,quite,qv,rather,rd,re,really,reasonably,regarding,regardless,regards,relatively,respectively,right,said,same,saw,say,saying,says,second,secondly,see,seeing,seem,seemed,seeming,seems,seen,self,selves,sensible,sent,serious,seriously,seven,several,shall,she,should,shouldn't,since,six,so,some,somebody,somehow,someone,something,sometime,sometimes,somewhat,somewhere,soon,sorry,specified,specify,specifying,still,sub,such,sup,sure,t's,take,taken,tell,tends,th,than,thank,thanks,thanx,that,that's,thats,the,their,theirs,them,themselves,then,thence,there,there's,thereafter,thereby,therefore,therein,theres,thereupon,these,they,they'd,they'll,they're,they've,think,third,this,thorough,thoroughly,those,though,three,through,throughout,thru,thus,to,together,too,took,toward,towards,tried,tries,truly,try,trying,twice,two,un,under,unfortunately,unless,unlikely,until,unto,up,upon,us,use,used,useful,uses,using,usually,value,various,very,via,viz,vs,want,wants,was,wasn't,way,we,we'd,we'll,we're,we've,welcome,well,went,were,weren't,what,what's,whatever,when,whence,whenever,where,where's,whereafter,whereas,whereby,wherein,whereupon,wherever,whether,which,while,whither,who,who's,whoever,whole,whom,whose,why,will,willing,wish,with,within,without,won't,wonder,would,wouldn't,yes,yet,you,you'd,you'll,you're,you've,your,yours,yourself,yourselves,zero".split(',')
#All the stop words
Wiki_URL = "https://en.wikipedia.org/w/index.php?search="

@app.route('/')
def homepage():
    return "Hello, this is the natural language processing capstone"

@ask.launch
def start_skill():
    msg = "What would you like to know more about?"
    return question(msg)

@ask.intent("getInputIntent")
def askWhichType(input):
    """
    Paramter: What the user wants to know more about
    This function is used for control flow
    Return: Asks if this is an entity or a query
    """
    global Input
    Input = "{}".format(input)
    print(Input, flush = True)
    newsQ = "Alright. Please tell me if this is an entity or query"
    return question(newsQ) 

@ask.intent("QueryIntent")
def askWhichQueryType():
    """
    Used for control low
    Return: Asks if the user wnats a list of docs or a list of entities
    """
    global Query
    Query = Input
    msg = "Do you want a list of documents or a list of entities"
    return question(msg)

@ask.intent("EntityIntent")
def entityToEntity():
    """
    Uses the inputed entity and gets all the top entities relating to the entity
    Return: All the entities relating to the inputed entity
    """
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
    print(image_msg, flush = True)
    return statement(image_msg)

@ask.intent("QuerytoEntityIntent")
def queryToEntity():
    """
    Gets a query and returns all the entities that are relating to the query
    Return: The entities
    """
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
    """
    Uses the inputted query and returns all the documents relating to the query.  It then prompts the user if they want a summary
    of a document.  
    Return: All documents relating to query and a question if the user wants a summary
    """
    finalDocs = db.engine.query(Query, 3)
    finalDocs = [i[0] for i in finalDocs]
    print(finalDocs, flush = True)
    wikipediaString = "wikipedia"
    cnnString = "cnn"
    reuterString = "reteurs"
    global TotalDocs
    if len(finalDocs) == 0:
        return statement("Sorry I could not find any documents")
    if len(finalDocs) == 1:
        if wikipediaString in finalDocs[0]:
            source = wikipediaString
        elif cnnString in finalDocs[0]:
            source = cnnString
        elif reuterString in finalDocs[0]:
            source = reuterString
        summary = summarize(db, finalDocs[0], stopwords)
        title = getTitle()
        image_msg = "The top document is {}".format(title) + " from {}".format(source) + "."
        image_msg += " Would you like a summary of this document?"
        TotalDocs = finalDocs
        return question(image_msg)
    elif len(finalDocs) == 2:
        if wikipediaString in finalDocs[0]:
            source1 = wikipediaString
        if cnnString in finalDocs[0]:
            source1 = cnnString 
        if reuterString in finalDocs[0]:
            source1 = reuterString
        if wikipediaString in finalDocs[1]: 
            source2 = wikipediaString 
        if cnnString in finalDocs[1]:
            source2 = cnnString
        if reuterString in finalDocs[1]:
            source2 = reuterString
        filler = summarize(db, finalDocs[0], stopwords)
        title1 = getTitle() 
        filler2 = summarize(db, finalDocs[1], stopwords)[0]
        title2 = getTitle()
        image_msg = "The top documents are {}".format(title1) + " from {}".format(source1) + " and " + "{}".format(title2) + " from {}".format(source2) + "."
        image_msg += " Would you like a summary of a document?"
        TotalDocs = finalDocs
        return question(image_msg)
    image_msg = "The top documents are "
    for i in range(len(finalDocs) - 1): 
        if wikipediaString in finalDocs[i]:
            source = wikipediaString
        elif cnnString in finalDocs[i]: 
            source = cnnString
        elif reuterString in finalDocs[i]:
            source = reuterString  
        #filler = summarize(db, finalDocs[i], stopwords, summarizeLength = 5)
        #title = getTitle()
        image_msg += "{}".format(finalDocs[i]) + " from {}".format(source)
        image_msg += ", "
    image_msg += "and "
    fillerrr = summarize(db, finalDocs[-1], stopwords)  
    titleLast = getTitle()
    image_msg += "{}".format(titleLast)
    image_msg +=  " Would you like a summary of a document?"
    TotalDocs = finalDocs
    return statement(image_msg)

@ask.intent("YesIntent")
def summarize_official():
    """
    If there is only one document, gets the summary of that document.  Otherwise, asks the user which document do they want to 
    summarize. 

    Return: Summary or a question of which doc do they want to summarize
    """
    print(len(TotalDocs), flush = True)
    if (len(TotalDocs) == 1):
        summary = summarize(db, TotalDocs[0], stopwords, summarizeLength = 2)
        print(len(summary), flush = True)
        print("{}".format(summary), flush = True)
        msg = "The summary is: {}".format(summary)
        return statement(msg)
    else:   
        return question("Which document? Give a number")

@ask.intent("WhichDocIntent") 
def summarizeRightDoc(Number):
    """
    Parameter: The number corresponding to the document in which the user wants a summary

    Goes to the corresponding document and gets the summary for that document

    Return: Summary of specified document
    """
    Number = "{}".format(Number)
    print(Number, flush = True)
    documentID = TotalDocs[int(Number) - 1]
    summary = summarize(db, documentID, stopwords, summarizeLength = 2)
    print("{}".format(summary), flush = True)
    msg = "The summary is: {}".format(summary)
    return statement(msg)

@ask.intent("NoIntent")
def no_intent():
    """
    Intent that is intialized if the user wants to cancel action  
    """
    msg = "Awkward. Next time you launch this app. Let me do something useful for once."
    return statement(msg)

def loadDatabase():
    """
    Loads database
    Return: Instance of the database
    """
    from database import Database
    db = Database("database.pkl")
    return db

if __name__ == '__main__':
    app.run(debug=True)

