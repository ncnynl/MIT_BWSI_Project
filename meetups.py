from googleplaces import GooglePlaces, types, lang
import googlemaps
from geopy.geocoders import Nominatim
import urllib
from urllib.request import urlopen
from flask import Flask
from flask_ask import Ask, statement, question, session
import requests
import json
import pprint


API_Key = "AIzaSyDjIdmWA4l-U9zAalsg9ySB3vy1qBxdJZs"
gmaps = googlemaps.Client(key=API_Key)
lato = 0
lono = 0
latd = 0
lond = 0
first = set()
sec = set()

app = Flask(__name__)
ask = Ask(app, '/')

@app.route('/')
def homepage():
    return "Hello"

@ask.launch
def start_skill():
    msg = "Hello. What is the first address?"
    return question(msg)

@ask.intent("FirstAddressSavingIntent")
def saveFAddress(Address):
    session.attributes["FAddress"] = Address
    addr = session.attributes["FAddress"]
    geolocator = Nominatim()
    location = geolocator.geocode('addr')
    lato = location.latitude
    lono = location.longitude

    msg = "What is the second address?"
    return question(msg)


@ask.intent("SecondAddressSavingIntent")
def saveSAddress(Address):
    session.attributes["SAddress"] = Address
    addr = session.attributes["SAddress"]
    geolocator = Nominatim()
    location = geolocator.geocode('addr')
    latd = location.latitude
    lond = location.longitude
    twothirdr = radiuscalc(lato, lono, latd, lond)
    fset = nearbysearch(lato, lono, twothirdr)
    sset = nearbysearch(latd, lond, twothirdr)
    finaldest = fset.intersection(sset)
    dest_msg = "My recommended locations are {}".format(finaldest)
    return statement(dest_msg)



def radiuscalc(lao, loo, lad, lod):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={},{}&destinations={},{}&key=AIzaSyDjIdmWA4l-U9zAalsg9ySB3vy1qBxdJZs".format(lao, loo, lad, lod)

    response = urlopen(url).read().decode('utf8')
    obj = json.loads(response)
    radius = (obj['rows'][0]['elements'][0]['distance']['text'])
    fradius = radius * 2/3
    return fradius

def nearbysearch(lat, lon, rad):
    nearby = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius={}&type=restaurant&key=AIzaSyDjIdmWA4l-U9zAalsg9ySB3vy1qBxdJZs".format(lat,lon,rad)
    ur = urlopen(nearby)
    data = ur.read().decode('utf-8')
    result = json.loads(data)['results']
    total = len(result)
    places = set()
    for i in range(total):
        places.add(result[i]['name'])
    return places
