import numpy as np
class ProfileLock:
    def __init__(self, name, descr, passwords):
        self.name = name
        self.descr = descr
        self.count = 1
        self.passwords = passwords
    def __repr__(self):
        return [self.name, self.passwords]
    def addDescr(self, newDescr):
        self.coun	
        self.descr = self.descr*(self.count-1)/self.count + newDescr*1/(self.count)
    def addPass(self, passwords):
    	if(len(passwords == 1)):
    		self.passwords.append(passwords)
    	else:
    		self.passwords.extend(passwords)





    #We can assume that the medicalID and birthday will remain constant so it'll be a one time thing.  