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
img = 0 #this is image array for file
img_array = 0 #this is image array for camera

@app.route('/')
def homepage():
    return "Hello, this is a test for basic facial recognition test"

@ask.launch
def start_skill():
    msg = "Hello, Would you like to save an image using the camera, or recognize an image?"
    return question(msg)

def get_image():
    """
    This takes an image and formats it into an array
    Return: Image array
    """
    img_array = imgarray()
    return img_array

@ask.intent("TakePictureIntent")
def take_image():
    """
    Takes an image, gets the image array from get_image() and then asks who is in the photo
    """
    global img_array
    img_array = get_image()
    msg = "Who's in the photo?"
    return question(msg)

@ask.intent("ClearIntent")
def clear():
    """
    Clears the database
    """
    db.clear()
    return statement("Done!")

@ask.intent("RecognizeIntent")
def recognize_image():
    """
    Takes an image and gets the image array.  Uses this array to detect the faces in the image.  Goes through the faces and 
    calculates the best match for each one by referencing the database.  Alexa then says who is in the image after some formatting
    Returns: People in the image 
    """
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

@ask.intent("CameraNameIntent")
def ask_for_name(camnames):
    """
    Parameter: The names of the people in the image
    Gets the names of the people in the image and then uses the image arrays to create new profiles
    """
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

