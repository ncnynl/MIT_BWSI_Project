import pickle
import numpy as np
from profile import Profile
from pathlib import Path as _Path
import os as _os

_path = _Path(_os.path.dirname(_os.path.abspath(__file__)))

class Database:

    def __init__(self, file):
        self.file = file
        try:
            self.profiles = self.getDatabase()
            print("Loaded from database", flush = True)
        except EOFError:
            self.profiles = []

    def __repr__(self):
        return "{}".format(self.profiles)

    def addProfile(self, profile):
        new = True
        ind = -1
        for i, prof in enumerate(self.profiles):
            if prof.name == profile.name:
                new = False
                ind = i
        if new:
            self.profiles.append(profile)
        else:
            self.profiles[i].addDescr(profile.descr)
            
        self.updateDatabase()
        print(self.profiles)

    def updateDatabase(self):
        with open(_path / self.file, "wb") as f:
            pickle.dump(self.profiles, f)

    def getDatabase(self):
        with open(_path / self.file, "rb") as f:
            currentProfile = pickle.load(f)
        return currentProfile

    def removeProfile(self, name):
        for i, prof in enumerate(self.profiles):
            if (prof.name == name):
                del self.profiles[i]
        self.updateDatabase()
        print(self.profiles)
    def clear(self):
        self.profiles = []
        self.updateDatabase()
        print("profiles: {}".format(self.profiles))

    #getting a descripiton vector of 128,
    #getting a database of profiles (each profile is a class_ in list with each class containing self.name and self.descr
    #take input vector and compare to each descr vector
    def computeMatches(self, picDescr, profiles):
        distances = []
        for i, prof in enumerate(profiles):
            curDes = prof.descr
            distances.append(np.linalg.norm(picDescr - curDes))
        distances = np.array(distances)
        print(np.min(distances))
        if np.min(distances) > 0.45:
            return Profile("Not Recognized", None)
        return profiles[np.argmin(distances)]

