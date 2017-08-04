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




app = Flask(__name__)
ask = Ask(app, '/')

API_Key = "AIzaSyDjIdmWA4l-U9zAalsg9ySB3vy1qBxdJZs"
gmaps = googlemaps.Client(key=API_Key)
first = set()
sec = set()

@app.route('/')
def homepage():
    return "Hello"

@ask.launch
def start_skill():
    msg = "Hello. What is the first address?"
    return question(msg)

@ask.intent("FirstAddressSavingIntent")
def saveFAddress(FAddress):
    session.attributes["FAddress"] = FAddress
    addr = session.attributes["FAddress"]
    print(addr, flush = True)
    geolocator = Nominatim()
    location = geolocator.geocode(addr)
    session.attributes["lato"] = location.latitude
    session.attributes["lono"] = location.longitude
    print(session.attributes["lato"], session.attributes["lono"])

    msg = "What is the second address?"
    return question(msg)


@ask.intent("SecondAddressSavingIntent")
def saveSAddress(SAddress):
    session.attributes["SAddress"] = SAddress
    addr = session.attributes["SAddress"]
    print(addr, flush = True)
    geolocator = Nominatim()
    location = geolocator.geocode(addr)
    session.attributes["latd"] = location.latitude
    session.attributes["lond"] = location.longitude
    print(session.attributes["lato"], session.attributes["lono"], session.attributes["latd"], session.attributes["lond"], flush = True)
    twothirdr = radiuscalc(session.attributes["lato"], session.attributes["lono"], session.attributes["latd"], session.attributes["lond"])
    fset = nearbysearch(session.attributes["lato"], session.attributes["lono"], twothirdr)
    sset = nearbysearch(session.attributes["latd"], session.attributes["lond"], twothirdr)
    finaldest = fset.intersection(sset)
    print(finaldest)
    dest_msg = "My recommended locations are {}".format(finaldest)
    return statement(dest_msg)



def radiuscalc(lao, loo, lad, lod):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={},{}&destinations={},{}&key=AIzaSyDjIdmWA4l-U9zAalsg9ySB3vy1qBxdJZs".format(lao, loo, lad, lod)

    response = urlopen(url).read().decode('utf8')
    obj = json.loads(response)
    print(obj)
    radius = float((obj['rows'][0]['elements'][0]['distance']['text']).split(" ")[0])
    print(radius)
    fradius = radius * 2/3 * 1000
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
    print(places)
    return places

if __name__ == '__main__':
    app.run(debug=True)
