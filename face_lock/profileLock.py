import numpy as np
class ProfileLock:
    def __init__(self, name, descr, passwords):
        """
        Parameters: Name of profile, image array of profile, passwords corresponding to the profile
        Initailizes everything
        """
        self.name = name
        self.descr = descr
        self.count = 1
        self.passwords = passwords
    def __repr__(self):
        """
        Return: A string representation of a profile, shows name and passwords
        """
        return "{}".format([self.name, self.passwords])
    def addDescr(self, newDescr):
        """
        Parameter: Image array
        Averages new image array into the existing average of image arrays
        """
        self.count+=1
        self.descr = self.descr*(self.count-1)/self.count + newDescr*1/(self.count)
    def addPass(self, passwords):
        """
        Adds on the password to the existing list of passwords
        """
        self.passwords.extend(passwords)