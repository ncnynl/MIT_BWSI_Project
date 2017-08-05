from collections import Counter
from database import Database
import itertools
def getTopEntities(entity, database, numEntities = 4):
    """
    Parameters: Entity, the instance of database, and a keyword argument of the number of Entities wanted 
    in the return

    Gets all the entities relating the to input entity.  ##I NEED RISHI'S DOCUMENTATION HERE

    Return: List of entities or an error message
    """
    IDs = database.engine.get_matches_term(entity)
    allEnts = []
    for ID in database.entities.keys():
        allEnts.append(database.entities[ID])
    allEnts = list(itertools.chain.from_iterable(allEnts))
    allEnts = Counter(allEnts)
    topEnts = allEnts.most_common(numEntities)
    finalEnts = set([i[0] for i in topEnts])
    finalEnts = list(finalEnts)
    trulyFinalEnt = []
    us = "US"
    united = "United States"
    if (entity in finalEnts):
        finalEnts.remove(entity)
    for ent in finalEnts:
        print(ent, flush = True)
        ent = "{}".format(ent)
        ent = ent.replace(".", "")
        if str(ent) == 'United States' and us in finalEnts:
            continue
        if str(ent) == 'US' and united in finalEnts:
            continue    
        else:
            trulyFinalEnt.append(ent)
    print(trulyFinalEnt, flush = True)
    trulyFinalEnt = set(finalEnts)
    if (len(trulyFinalEnt) < numEntities):
        print("Sorry, the article was not long enough to return top " + str(numEntities) + " entities")
    return list(trulyFinalEnt)

def getEntities(db, query, topEntities = 5):
    """
    Parameters: Instance of database, query input, a keyword argument of number of Entities returned

    Gets all the documents relating to the query, and then iterates through them to get the Entities into a counter.
    Afterwards, gets the top K entities as specified and returns them in a list.  (Pardon my French)

    Returns: List of entities relating to query
    """
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