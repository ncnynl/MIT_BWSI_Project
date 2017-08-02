from googleplaces import GooglePlaces, types, lang
from pygeocoder import Geocoder

API_Key = AIzaSyCnuCETkfIGLknIdLADpe5v2l62mogdHLE

google_places = GooglePlaces(API_Key)

#get address from alexa, geocode to coordinates
result = Geocoder.geocode("7250 South Tucson Boulevard, Tucson, AZ 85756")
if(result.valid_address == False):
    return "please enter a valid address"



#nearby search, get keyword?
query_result = google_places.nearby_search(
    location= result, keyword='Restaurants',
    radius=1000, types=[types.TYPE_RESTAURANT])

if query_result.has_attributions:
   print query_result.html_attributions


for place in query_result.places:
    print place.name
