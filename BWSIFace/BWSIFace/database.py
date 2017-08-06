import pickle
import numpy as np
from .profileClass import ProfileClass
from pathlib import Path as _Path
import os as _os

_path = _Path(_os.path.dirname(_os.path.abspath(__file__)))

class Database:

    def __init__(self, file):
        """
        create a database with the associated pickle file of the existing profiles
        :param file: the pickle file of the existing profiles
        """
        self.file = file
        try:
            self.profiles = self.getDatabase()
            print("Loaded from database", flush = True)
        except EOFError:
            self.profiles = []
            
    def __repr__(self):
        """
        useful to call for clean viewing of the profiles of the database class
        :return: string that describes the list of profiles in the database
        """
        return "{}".format(self.profiles)

    def addProfile(self, profile):
        """
        This adds a profile to the database.
        :param profile: the profile to add into the database
        """
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
        """
        updates database with the current profiles stored as a list
        """
        with open(str(_path / self.file), "wb") as f:
            pickle.dump(self.profiles, f)

    def getDatabase(self):
        """
        Gets the profiles from the pickle file and stored it temporarily into the program
        into self.profiles so that we can easily acces the profiles
        :return: currentProfile, the list of profiles in the pickle file currently
        """
        # print(str(_path / self.file), flush = True)
        with open(str(_path / self.file), "rb") as f:
            currentProfile = pickle.load(f)
        return currentProfile

    def removeProfile(self, name):
        """
        Removes a profile from the database which belongs to the input name
        :param name: the name of the profile someone wants to remove from the database
        """
        for i, prof in enumerate(self.profiles):
            if (prof.name == name):
                del self.profiles[i]
        self.updateDatabase()
        print(self.profiles)
    def clear(self):
        self.profiles = []
        self.updateDatabase()
        print("profiles: {}".format(self.profiles))

    

    # getting a descripiton vector of 128,
    # getting a database of profiles (each profile is a class_ in list with each class containing self.name and self.descr
    # take input vector and compare to each descr vector
    
    def computeMatches(self, picDescr, profiles):
        """
        computes the euclidean distance between the image to recognize and the images already in the databse
        :param picDescr: the description vector of shape (128,) to compare the images already in the database
        :param profiles: the database profiles

        :return: the profile name that has the best match
        """
        distances = []
        for i, prof in enumerate(profiles):
            curDes = prof.descr
            distances.append(np.linalg.norm(picDescr - curDes))
        distances = np.array(distances)
        print(np.min(distances))
        if np.min(distances)>.45:
            return ProfileClass("Not Recognized", None)
        return profiles[np.argmin(distances)]

