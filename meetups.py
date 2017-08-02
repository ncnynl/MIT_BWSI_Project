from googleplaces import GooglePlaces, types, lang
from pygeocoder import Geocoder

API_Key = AIzaSyCnuCETkfIGLknIdLADpe5v2l62mogdHLE

google_places = GooglePlaces(API_Key)



#
query_result = google_places.nearby_search(
    location='Mumbai', keyword='Restaurants',
    radius=1000, types=[types.TYPE_RESTAURANT])

geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

result = Geocoder.geocode("7250 South Tucson Boulevard, Tucson, AZ 85756")
