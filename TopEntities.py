#get one entity, and a database(search engine, entities)
#find top three entities
#get all documents that contain my entity
from database import Database
import itertools
from collections import Counter

def getTopEntities(entity, database, numEntities = 3):
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
    """for ent in topEnts:
        if(ent[0] != entity):
            finalEnts.append(ent[0])"""
    if (len(finalEnts) < numEntities):
        print("Sorry, the article was not long enough to return top " + str(numEntities) + " entities")
    return finalEnts

entity = "White House"
database = Database("database.pkl")
print(getTopEntities(entity, database))

