from flask import Flask
from flask_ask import Ask, statement, question
from BWSIFace.datalock import Datalock
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