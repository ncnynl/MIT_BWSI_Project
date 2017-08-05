#RiceKrispies: Julie Lee

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
first = set() #a set that contains all the locations a certain radius away from the first address
sec = set() #a set that contains all the locations a certain radius away from the second address

@app.route('/')
def homepage():
    return "Hello"

@ask.launch
def start_skill():
    msg = "Hello. What is the first address?"
    return question(msg)

@ask.intent("FirstAddressSavingIntent")
def saveFAddress(FAddress):
    """
    Takes in the user input of an address in the format of: street address, city, and state. By utilizing geopy,
    convert the input to latitude, longitude coordinates. Then, Alexa will prompt the user to enter the second
    address.
    """
    session.attributes["FAddress"] = FAddress
    addr = session.attributes["FAddress"]
    print(addr, flush = True)
    geolocator = Nominatim()
    location = geolocator.geocode(addr)
    session.attributes["lato"] = location.latitude
    session.attributes["lono"] = location.longitude
    print(session.attributes["lato"], session.attributes["lono"])

    msg = "Would you like to add another address?"
    return question(msg)

@ask.intent("YesIntent")
def yes_intent():
    msg = "What is the second address"
    return question(msg)

@ask.intent("NoIntent")
def no_intent():
    msg = "How far would you like to search in meters"
    return question(msg)

@ask.intent("DistanceSavingIntent")
def saveDistance(radius):
    session.attributes["radius"] = radius
    nearby = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius={}&type=restaurant&key=AIzaSyDjIdmWA4l-U9zAalsg9ySB3vy1qBxdJZs".format(session.attributes["lato"], session.attributes["lono"],session.attributes["radius"])
    ur = urlopen(nearby)
    data = ur.read().decode('utf-8')
    result = json.loads(data)['results']
    places = set()
    for i in range(len(result)):
        places.add(result[i]['name'])
    print(places)
    dest_msg = "My recommended locations are {}".format(places)
    return statement(dest_msg)



@ask.intent("SecondAddressSavingIntent")
def saveSAddress(SAddress):
    """
    Takes in the user input of the second address and converts it to coordinate points. Using radiuscalc, find the
    2/3 distance between the first and second address. Find all the pertaining locations within this radius for
    both addresses by calling nearbysearch. Return the intersection of these two sets.
    """
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
    """
    Utilizes the Google Maps distance matrix API, which takes in the coordinates of two locations and returns the
    distance in meters between the two. This method will return 2/3 of this distance.

    Parameters
    ----------
    lao: latitude of origin (first address)
    loo: longitude of origin (first address)
    lad: latitude of destination (second address)
    lod: longitude of destination (second address)

    Returns
    -------
    float
        2/3 of the distance between the two addresses
    """

    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={},{}&destinations={},{}&key=AIzaSyDjIdmWA4l-U9zAalsg9ySB3vy1qBxdJZs".format(lao, loo, lad, lod)
    response = urlopen(url).read().decode('utf8')
    obj = json.loads(response)
    print(obj)
    radius = float((obj['rows'][0]['elements'][0]['distance']['text']).split(" ")[0])
    print(radius)
    fradius = radius * 4/5 * 1000
    return fradius

def nearbysearch(lat, lon, rad):
    """
    Utilizes the Google Maps Places nearby search API, which takes in the coordinates of an address, radius, and type.
    The type is a keyword that indicates the kind of locations the user is searching for, such as a restaurant.
    The search will return all the pertaining locations within the specified radius from the original address.

    Parameters
    ----------
    lat: latitude coordinate of address
    lon: longitude coordinate of address
    rad: radius of search

    Returns
    -------
    set
        set of suggested locations
    """
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
