from flask import Flask
from flask_ask import Ask, statement, question
from BWSIFace.datalock import Datalock
from BWSIFace.cameras import imgarray
from BWSIFace.detection import detect
from BWSIFace.profileLock import ProfileLock

db = Datalock("profileLock.pkl")
#app = Flask(__name__)
#ask = Ask(app, '/')
img = 0 #this is for file 
img_array = 0 #this is for camera
FaceGot = 0
Name = ""
Boolean = False
BestMatch = None
Passwords = []

#@app.route('/')
def homepage():
    return "Hello, this is an application where we use your face to manage passwords"

#@ask.launch
def start_skill():
    msg = "Hello, Would you like to retrieve your passwords or store a password?"
    return question(msg)

def get_image():
    img_array = imgarray()
    return img_array

#@ask.intent("RetrievePasswordIntent") 
def retrieve_passwords():
	img_array = get_image()
	global BestMatch
	faceGot = detect(img_array, False)
	descript = faceGot[0]
	BestMatch = db.computeMatches(descript, db.profiles)
	print(BestMatch)
	passwords = BestMatch.passwords
	print(passwords)
	scores = password_strengths()
	msg = ""
	for i, score in enumerate(scores):
		if score < 40:
			msg += "You have a weak password, it is {}".format(Passwords[i])
	msg += "Okay, I printed out all the passwords for you"
	return statement(msg)

#@ask.intent("StoreIntent")
def store_password():
	global descript
	global Boolean
	img_array = get_image()
	print(img_array)
	FaceGot = detect(img_array, False)
	global BestMatch
	print((FaceGot[0])[0])
	print(len(db.profiles))
	if (not(len(db.profiles)) == 0):
		BestMatch = db.computeMatches((FaceGot[0])[0], db.profiles)
		print(BestMatch)
		if (BestMatch in db.profiles):
			msg = "Enter all your passwords please"
			#return statement(msg)
		else:
			Boolean = True
			msg = "Tell me your name"
			#return statement(msg)
	else:
		Boolean = True
		msg = "Tell me your name"
		#return statement(msg)

#@ask.intent("AppendPasswordsIntent")
def add_passwords(passwords): #issues with typing vs saying the passwords, no need to separate by oommas
	passwords = "{}".format(passwords)
	passwords = passwords.split()
	global Passwords
	global BestMatch
	Passwords = passwords
	print(Name)
	print(Passwords)
	print(Boolean)
	if (Boolean):
		newProfile = ProfileLock(Name, FaceGot, passwords)
		db.addProfile(newProfile)
		print(newProfile)
		for i, password in enumerate(passwords):
			newProfile.addPass(password)
	else:
		for i, password in enumerate(passwords):
			BestMatch.addPass(password)
	message = "Okay got it!"
	#return statement(message)

#@ask.intent("AddNewProfileIntent")
def add_profile(name):
	global Name
	Name = "{}".format(name)
	msg = "Enter all your passwords please"
	#return statement(msg)

def password_strengths():
	scores = []
	for i, password in enumerate(Passwords):
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

#@ask.intent("NoIntent")
def no_intent():
    msg = "Ok, thanks. Have a nice day."
    return statement(msg)

#if __name__ == '__main__':
    #app.run(debug=True)

store_password()
add_profile("Brandon")
add_passwords("My project sucks")