import time
from database import Database
from requeteAlentite import *
t0 = time.time()

db = Database("database.pkl")
print(db)
print(getEntities(db, "democrat"))
t1 = time.time()
print("elapsed " + str(t1 - t0) + "s")