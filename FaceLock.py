from flask import Flask
from flask_ask import Ask, statement, question
from BWSIFace.datalock import Datalock
from BWSIFace.cameras import imgarray
from BWSIFace.detection import detect
from BWSIFace.profileLock import ProfileLock

db = Datalock("profiles.pkl")
app = Flask(__name__)
ask = Ask(app, '/')
img = 0 #this is for file 
img_array = 0 #this is for camera
FaceGot = 0
Name = ""
Boolean = False
BestMatch = None
Passwords = []

@app.route('/')
def homepage():
    return "Hello, this is an application where we use your face to manage passwords"

@ask.launch
def start_skill():
    msg = "Hello, Would you like to retrieve your passwords or store a password?"
    return question(msg)

def get_image():
    img_array = imgarray()
    return img_array

@ask.intent("RetrievePasswordIntent") 
def retrieve_passwords():
    img_array = get_image()
    faceGot = detect(img_array, False)
    descript = faceGot[0]
    bestMatch = db.computeMatches(descript, db.profiles)
    passwords = bestMatch.passwords
    print(passwords)
    msg = "Okay, I printed out the passwords for you"
    return statement(msg)

@ask.intent("StoreIntent")
def store_password():
	global descript
	img_array = get_image()
	FaceGot = detect(img_array, False)[0]
	BestMatch = db.computeMatches(FaceGot, db.profiles)
	if (BestMatch in db.profiles):
		msg = "Enter all your passwords please"
		return statement(msg)
	else:
		global Boolean
		Boolean = True
		msg = "Tell me your name"
		return statement(msg)

@ask.intent("AppendPasswordsIntent")
def add_passwords(passwords): #issues with typing vs saying the passwords, no need to separate by oommas
	passwords = "{}".format(passwords)
	passwords = passwords.split()
	global Passwords
	Passwords = passwords
	if (Boolean):
		newProfile = ProfileLock(Name, FaceGot, passwords)
		db.addProfile(newProfile)
	for i, password in enumerate(passwords):
		BestMatch.ProfileLock.addPass(password)
	message = "Okay got it!"
	return statement(message)

@ask.intent("AddNewProfileIntent")
def add_profile(name):
	global Name
	Name = "{}".format(name)
	msg = "Enter all your passwords please"
	return statement(msg)

def password_strengths():
	scores = []
	for i, password in enumerate(Passwords):
		score = 0
		score += len(password) * 4
		score += 




@ask.intent("NoIntent")
def no_intent():
    msg = "Ok, thanks. Have a nice day."
    return statement(msg)

if __name__ == '__main__':
    app.run(debug=True)

#ake_image()
#print(ask_for_name("brandon"))