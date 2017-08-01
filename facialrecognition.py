from flask import Flask
from flask_ask import Ask, statement, question
from BWSIFace.database import Database
from BWSIFace.cameras import imgarray
from BWSIFace.detection import detect
from BWSIFace.profileClass import ProfileClass
import requests
import time
import unidecode
import json

db = Database("profiles.pkl")

app = Flask(__name__)
ask = Ask(app, '/')
img = 0 #this is for file
img_array = 0 #this is for camera

@app.route('/')
def homepage():
    return "Hello, this is a test for basic facial recognition"

@ask.launch
def start_skill():
    msg = "Hello, Would you like to save an image using the camera, or recognize an image?"
    return question(msg)

def get_image():
    img_array = imgarray()
    return img_array

@ask.intent("TakePictureIntent")
def take_image():
    global img_array
    img_array = get_image()
    msg = "Who's in the photo? (separate names by commas and spaces)"
    return question(msg)

"""@ask.intent("FileAskerIntent")
def just_for_asking():
    msg = "What file do you want to save?"
    return statement(msg)

@ask.intent("SavePictureIntent") #probably need a slot with a label file name
def save_image(file):
    global img
    img = io.imread(file)
    msg = "Who's in the photo? (separate names by comma space)"
    return statement(msg)
"""
@ask.intent("ClearIntent")
def clear():

    db.clear()
    return statement("lmao")

@ask.intent("RecognizeIntent")
def recognize_image():
    img_array = get_image()
    facesGot = detect(img_array, False)
    bestMatches = []
    for face in facesGot:
        descript = face[0]
        bestMatch = db.computeMatches(descript, db.profiles)
        bestMatches.append(bestMatch)
    print(bestMatches)
    if len(bestMatches) == 1:
        image_msg = "The person in the image is {}".format(bestMatches[0])
        print(image_msg)
        return statement(image_msg)
    elif len(bestMatches) == 2:
        image_msg = "The person in the image is {}".format(bestMatches[0]) + " and " + "{}".format(bestMatches[1])
        return statement(image_msg)
    image_msg = "The person in the image is "
    for i in range(len(bestMatches) - 1):
        image_msg += "{}".format(bestMatches[i])
        image_msg += ", "
    image_msg += "and "
    image_msg += "{}".format(bestMatches[-1])
    print(image_msg)
    return statement(image_msg)

"""@ask.intent("FileNameIntent"):
def ask_for_name_file(names):
    if img.shape[2] == 4:
        img = img[:, :, 0:3]
    faces = detect(img)
    names = names.lower().split()
    for i, face in enumerate(faces):
        descr, (l, r, t, b) = face
        profile = ProfileClass(names[i], descr)
        db.addProfile(profile)
    imgMessage = "Okay, saved to the database!"
    return statement(imgMessage)
"""
@ask.intent("CameraNameIntent")
def ask_for_name(camnames):
    camnames = "{}".format(camnames)
    print(camnames)
    faces = detect(img_array, showImg = False)
    camnames = camnames.lower().split()
    for i, face in enumerate(faces):
        descr = face[0]
        profile = ProfileClass(camnames[i], descr)
        db.addProfile(profile)
    imgMessage = "Okay got it!"
    return statement(imgMessage)

@ask.intent("NoIntent")
def no_intent():
    msg = "Ok, thanks. Have a nice day."
    return statement(msg)

if __name__ == '__main__':
    app.run(debug=True)

t#ake_image()
#print(ask_for_name("brandon"))
