import pickle
import numpy as np
from .profileLock import ProfileLock
from pathlib import Path as _Path
import os as _os

_path = _Path(_os.path.dirname(_os.path.abspath(__file__)))

class Datalock:

    def __init__(self, file):
        """
        Parameter: File name
        Intializes the database or calls it if one is already created
        """
        self.file = file
        try:
            self.profiles = self.getDatabase()
        except EOFError:
            self.profiles = []
            
    def __repr__(self):
        """
        Returns the string format of profiles
        """
        return "{}".format(self.profiles)

    def addProfile(self, profile):
        """
        Paramter: Profile

        Adds a new profile, if an existing one exists, it just adds the image vector and the passwords
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
            self.profiles[i].addPass(profile.passwords)
            
        self.updateDatabase()

    def updateDatabase(self):
        """
        Updates Database
        """

        with open(str(_path / self.file), "wb") as f:
            pickle.dump(self.profiles, f)

    def getDatabase(self):
        """
        Gets Database

        Return: The list of profiles
        """
        # print(str(_path / self.file), flush = True)
        with open(str(_path / self.file), "rb") as f:
            currentProfile = pickle.load(f)
        return currentProfile

    def getProfile(self, descript):
        """
        Parameter: Image vector of the image

        Returns the specified profile according to the image vector

        Returns: The profile or an error message

        """
        for i, prof in enumerate(self.profiles):
            if (prof.descript == descript):
                return self.profiles[i]
        return "Sorry profile not found"

    def removeProfile(self, name):
        """
        Parameter: Name of profile;

        Removes a profile according to the associated name
        """
        for i, prof in enumerate(self.profiles):
            if (prof.name == name):
                del self.profiles[i]
        self.updateDatabase()

    def getDescript(self):
        """
        Goes through all the profiles and gets all the image vectors and makes them into a list

        Return: A list of image vectors
        """
        descripts = []
        for i, profile in enumerate(profiles):
            descr = profile.descr
            descripts.append(descr)
        return descripts
        
    def clear(self):
        """
        Clears the database
        """
        self.profiles = []
        self.updateDatabase()
        print("profiles: {}".format(self.profiles))

    #getting a descripiton vector of 128,
    #getting a database of profiles (each profile is a class_ in list with each class containing self.name and self.descr
    #take input vector and compare to each descr vector
    
    def computeMatches(self, picDescr, profiles):
        """
        Parameter: Image vector and the profiles in a database

        Uses the image vector and iterates through the profiles to determine which profile best matches the image vector

        Return: The best matched profile or an error message
        """
        distances = []
        for i, prof in enumerate(profiles):
            curDes = prof.descr
            distances.append(np.linalg.norm(picDescr - curDes))
        distances = np.array(distances)
        print(np.min(distances), flush = True)
        if np.min(distances) > 1.39 :
            return ProfileLock("Not Recognized", None, None)
        return profiles[np.argmin(distances)]

