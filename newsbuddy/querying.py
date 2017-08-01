from collections import Counter
from database import Database
import itertools
def getTopEntities(entity, database, numEntities = 4):
    IDs = database.engine.get_matches_term(entity)
    allEnts = []
    for ID in database.entities.keys():
        allEnts.append(database.entities[ID])
    allEnts = list(itertools.chain.from_iterable(allEnts))
    allEnts = Counter(allEnts)
    topEnts = allEnts.most_common(numEntities)
    finalEnts = set([i[0] for i in topEnts])
    if (entity in finalEnts):
        finalEnts.remove(entity)
    if (len(finalEnts) < numEntities):
        print("Sorry, the article was not long enough to return top " + str(numEntities) + " entities")
    return list(finalEnts)

def getEntities(db, query, topEntities = 5):
    documents = db.engine.query(query)  
    listeDesMots = [] #this will be a list with listOfEntities
    for documentID, score in documents: #this loops translates ID's to text and tokenizes them. 
        listeDesMots += db.entities[documentID]
    compter = Counter(listeDesMots)
    compter[query] = 0
    lePlusCommun = compter.most_common(topEntities)
    listeDesEntitesCommunes = [i[0] for i in lePlusCommun]
    queryList = query.split()
    for word in queryList:
        if (word in listeDesEntitesCommunes):
            pass
    if len(listeDesEntitesCommunes) == 0:
        return "Sorry, no entries were found"
    return listeDesEntitesCommunes