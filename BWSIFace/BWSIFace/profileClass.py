import numpy as np
class ProfileClass:
    """
    A class that represents a single profile, which consists of the name of the person, and his or her average image
    descriptor vector
    """
    def __init__(self, name, descr):
        self.name = name
        self.descr = descr
        self.count = 1
    def __repr__(self):
        return self.name
    def addDescr(self, newDescr):
        self.count+=1
        self.descr = self.descr*(self.count-1)/self.count + newDescr*1/(self.count)
    