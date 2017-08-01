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
from newsbuddy.summarize import summarize
from newsbuddy.nlp_stock import stop_words

db = Database("database.pkl")
app = Flask(__name__)
ask = Ask(app, '/')
Input = ""
Query = ""
Entity = ""
TotalDocs = []
stopwords = "a,able,about,above,according,accordingly,across,actually,after,afterwards,again,against,ain't,all,allow,allows,almost,alone,along,already,also,although,always,am,among,amongst,an,and,another,any,anybody,anyhow,anyone,anything,anyway,anyways,anywhere,apart,appear,appreciate,appropriate,are,aren't,around,as,aside,ask,asking,associated,at,available,away,awfully,be,became,because,become,becomes,becoming,been,before,beforehand,behind,being,believe,below,beside,besides,best,better,between,beyond,both,brief,but,by,c'mon,c's,came,can,can't,cannot,cant,cause,causes,certain,certainly,changes,clearly,co,com,come,comes,concerning,consequently,consider,considering,contain,containing,contains,corresponding,could,couldn't,course,currently,definitely,described,despite,did,didn't,different,do,does,doesn't,doing,don't,done,down,downwards,during,each,edu,eg,eight,either,else,elsewhere,enough,entirely,especially,et,etc,even,ever,every,everybody,everyone,everything,everywhere,ex,exactly,example,except,far,few,fifth,first,five,followed,following,follows,for,former,formerly,forth,four,from,further,furthermore,get,gets,getting,given,gives,go,goes,going,gone,got,gotten,greetings,had,hadn't,happens,hardly,has,hasn't,have,haven't,having,he,he's,hello,help,hence,her,here,here's,hereafter,hereby,herein,hereupon,hers,herself,hi,him,himself,his,hither,hopefully,how,howbeit,however,i'd,i'll,i'm,i've,ie,if,ignored,immediate,in,inasmuch,inc,indeed,indicate,indicated,indicates,inner,insofar,instead,into,inward,is,isn't,it,it'd,it'll,it's,its,itself,just,keep,keeps,kept,know,known,knows,last,lately,later,latter,latterly,least,less,lest,let,let's,like,liked,likely,little,look,looking,looks,ltd,mainly,many,may,maybe,me,mean,meanwhile,merely,might,more,moreover,most,mostly,much,must,my,myself,name,namely,nd,near,nearly,necessary,need,needs,neither,never,nevertheless,new,next,nine,no,nobody,non,none,noone,nor,normally,not,nothing,novel,now,nowhere,obviously,of,off,often,oh,ok,okay,old,on,once,one,ones,only,onto,or,other,others,otherwise,ought,our,ours,ourselves,out,outside,over,overall,own,particular,particularly,per,perhaps,placed,please,plus,possible,presumably,probably,provides,que,quite,qv,rather,rd,re,really,reasonably,regarding,regardless,regards,relatively,respectively,right,said,same,saw,say,saying,says,second,secondly,see,seeing,seem,seemed,seeming,seems,seen,self,selves,sensible,sent,serious,seriously,seven,several,shall,she,should,shouldn't,since,six,so,some,somebody,somehow,someone,something,sometime,sometimes,somewhat,somewhere,soon,sorry,specified,specify,specifying,still,sub,such,sup,sure,t's,take,taken,tell,tends,th,than,thank,thanks,thanx,that,that's,thats,the,their,theirs,them,themselves,then,thence,there,there's,thereafter,thereby,therefore,therein,theres,thereupon,these,they,they'd,they'll,they're,they've,think,third,this,thorough,thoroughly,those,though,three,through,throughout,thru,thus,to,together,too,took,toward,towards,tried,tries,truly,try,trying,twice,two,un,under,unfortunately,unless,unlikely,until,unto,up,upon,us,use,used,useful,uses,using,usually,value,various,very,via,viz,vs,want,wants,was,wasn't,way,we,we'd,we'll,we're,we've,welcome,well,went,were,weren't,what,what's,whatever,when,whence,whenever,where,where's,whereafter,whereas,whereby,wherein,whereupon,wherever,whether,which,while,whither,who,who's,whoever,whole,whom,whose,why,will,willing,wish,with,within,without,won't,wonder,would,wouldn't,yes,yet,you,you'd,you'll,you're,you've,your,yours,yourself,yourselves,zero"
stopWordsList = stop_words()

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
        image_msg += "Would you like a summary of this document?"
        return statement(image_msg)
    elif len(finalDocs) == 2:
        image_msg = "The top documents are {}".format(finalDocs[0]) + " and " + "{}".format(finalDocs[1])
        image_msg += "Would you like a summary of a document?"
        return statement(image_msg)
    image_msg = "The top documents are "
    for i in range(len(finalDocs) - 1):
        image_msg += "{}".format(finalDocs[i])
        image_msg += ", "
    image_msg += "and "
    image_msg += "{}".format(finalDocs[-1])
    image_msg +=  "Would you like a summary of a document?"
    global TotalDocs
    TotalDocs = finalDocs
    return statement(image_msg)

@ask.intent("YesIntent")
def summarize():
    if (TotalDocs == 1):
        summary = summarize(db, finalDocs[0], stopWordsList)
        msg = "The summary is: {}".format(summary)
        return statement(msg)
    else:
        return statement("Which document? Give a number")

@ask.intent("WhichDocIntent")
def summarizeRightDoc(number):
    documentID = TotalDocs[number - 1]
    summary = summarize(db, documentID, stopWordsList)
    msg = "The summary is: {}".format(summary)
    return statement(msg)

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

