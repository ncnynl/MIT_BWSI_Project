from flask import Flask
from flask_ask import Ask, statement, question
from face_recog.datalock import Datalock
from face_recog.module import imgarray
from face_recog.module import detect
from face_recog.profileLock import ProfileLock
import numpy as np
import getpass
import re
import skimage.io as io
import sys
from pathlib import Path as _Path
import os as _os	
import time

app = Flask(__name__)
ask = Ask(app, '/')

db = Datalock("profileLock.pkl") #Loading the current database into the variable
img_array = 0 #Global Variable to store the picture-array
FaceGot = 0 #stores the detcted face as a global variable to allow interactions between functions
Name = "" #stores the name inputed by the user to 
Boolean = False #stores whether the user is a new person
BestMatch = None #stores who the computer recognizes as the best match in the image taken by the computer
Passwords = [] #stores the passwords the user appended

@app.route('/')
def homepage():
    return "Hello"

@ask.launch
def start_skill():
    msg = "Hello, Would you like to retrieve your passwords or store a password?"
    return question(msg)

def get_image():
	"""
	This takes an image and formats it into an array
	Return: Image array
	"""
	img_array = imgarray()
	return img_array

@ask.intent("RetrievePasswordIntent") 
def retrieve_passwords():
	"""
	Takes an image and then detects the face in the image.  After, find the best match for the person in the image. Then, retrieves
	the person corresponding to the password. Goes through the password and determines if the password is weak or strong.  If the 
	password is weak, Alexa says the password outloud forcing you to change the password.  It then prints out all the passwords 
	corresponding to your name. If the person is not recognized, Alexa will not allow you to see the passwords.   

	Returns: All weak passwords OR an error message
	"""
	img_array = get_image()
	global BestMatch
	faceGot = detect(img_array, False)
	descript = faceGot[0]
	BestMatch = db.computeMatches(descript[0], db.profiles)
	global Passwords 
	if (BestMatch.passwords is not None):
		print(BestMatch, flush = True)
		Passwords = list(BestMatch.passwords) 
		passwords = BestMatch.passwords
		print(passwords, flush = True)
		scores = password_strengths()
		print(scores, flush = True)
		msg = ""
		if (not(len(scores) == 0)):
			msg += "You have a weak password, it is"
		for i, score in enumerate(scores):
			if score < 40:
				indexer = Passwords[i].index(":")
				msg += " {} and".format((Passwords[i])[indexer+1 : ])
		msg += " I printed out all the passwords for you"
		return statement(msg)
	else:
		msg = "I don't recognize you, stop trying to hack into passwords"
		return statement(msg)	

@ask.intent("StoreIntent")
def store_password():
	"""
	Gets an image and then detects the face.  If the database is empty, then it immediately prompts for your name to create a new
	profile.  If the database is not empty but the computer can not recognize you, it prompts for your name to create a new profile. 
	Otherwise, it asks you which website do you want to save the password to.   
	"""
	global descript
	global Boolean 
	global FaceGot
	img_array = get_image()
	FaceGot = detect(img_array, False)
	global BestMatch
	print(len(db.profiles), flush = True)
	if (not(len(db.profiles)) == 0):
		BestMatch = db.computeMatches((FaceGot[0])[0], db.profiles)
		print(BestMatch, flush = True)
		if (BestMatch in db.profiles):
			msg = "What website do you want to save a password to. After you enter a website, follow the instructions in the computer console"
			return question(msg)
		else:
			Boolean = True
			msg = "Tell me your name"
			return question(msg)
	else: 
		Boolean = True
		msg = "Tell me your name"
		return question(msg)

@ask.intent("AppendPasswordsIntent")
def add_passwords(website):
	"""
	Parameter: Website name
	Asks the user to type their password to the corresponding website and then adds it to the profile in the database
	"""
	password = input("Enter the password for the website.\n")
	password = "{}".format(password)
	website = "{}".format(website)
	print(password, flush = True)
	passwords = website + ":" + password
	passwords = passwords.split()
	global Passwords
	global BestMatch
	Passwords = passwords
	if (Boolean):
		newProfile = ProfileLock(Name, FaceGot, passwords)
		db.addProfile(newProfile) 
	else:
		for i, password in enumerate(passwords):
			BestMatch.addPass(password)
	message = "Okay got it!"
	return statement(message)

@ask.intent("AddNewProfileIntent")
def add_profile(name):
	"""
	Parameter: User Name
	Asks for the name of the user.  
	"""
	global Name
	Name = "{}".format(name) 
	msg = "What website do you want to save a password to.  After you enter a website, follow the instructions in the computer console"
	return question(msg)

def password_strengths():
	"""
	Determines the password strength of a password through an algorithm.  You get rewarded for longer passwords and ones with upper 
	and lower cases but get penalized if you have consecutive upper cases or lower cases.  There is more nuance but that is the 
	general overview.  

	Returns: Scores
	"""
	scores = []
	print(Passwords)
	for i, password in enumerate(Passwords):
		indexer = password.index(":")
		password = password[indexer + 1]
		print(password, flush = True)
		score = 0
		score += len(password) * 4
		if password.isalpha():
			score -= len(password)
		if password.isdigit():
			score -= len(password) 
		for letter in password:
			upperCount = 0
			lowerCount = 0
			numberCount = 0
			characterCount = 0
			if (letter.isupper()):
				upperCount += 1 
			if (letter.islower()):
				lowerCount += 1
			if (letter.isdigit()):
				numberCount += 1 
			score += (len(password) - upperCount)*2
			score += (len(password) - lowerCount)*2
			score += numberCount * 4
			if (not (i == 1) and letter.lower() == password[i-1].lower()):
				score -= 1
			if (not(i == 1) and letter.isupper() and password[i-1].isupper()):
				score -= 1
			if (not(i == 1) and letter.islower() and password[i-1].islower()):
				score -= 1
			if (not(i == 1) and letter.isdigit() and password[i-1].isdigit()):
				score -= 1
		scores.append(score)
	return scores

@ask.intent("NoIntent")
def no_intent():
	"""
	Intent that is intialized if the user wants to cancel action  
	"""
    msg = "Ok, thanks. Have a nice day."
    return statement(msg)

if __name__ == '__main__':
    app.run(debug=True)