Meetups ReadMe


This meetup program is designed to return the names of recommended restaurants nearby an address or
2 addresses. Through the Flask App, Alexa will prompt the user for the first address, which will be in the form of:
street address, city, and state.

If the user wishes to search with only one address, they respond "no" when Alexa
inquires about the second address. Then, they provide Alexa with the desired search radius, which is in meters.
Alexa will then respond with suggested restaurants within this range.

If the user chooses to respond with a second address, the distance between the two locations is calculated.
Then a set of restaurants within 2/3 of the calculated distance for each of the two addresses is respectively
generated. Alexa will return the intersection of these two sets.

Geopy is used to convert spoken addresses to latitude and longitude coordinates. The Google Maps distance matrix API was
utilized to find the distance between 2 sets of coordinates, while the Google Maps Places nearbysearch API helped find the optimal meeting places, which in this case, are restaurants. The default was set to "rank by prominence," which helps Alexa only return restaurants with positive ratings, usually 3.5/5 or higher.

#Usage
-Download Geopy and GoogleMaps using pip install
-In the Alexa Developer's Console, under interaction model, copy and paste the following.

(For Intent Schema)-

{
  "intents": [
    {
      "slots": [
        {
          "name": "FAddress",
          "type": "AMAZON.PostalAddress"
        }
      ],
      "intent": "FirstAddressSavingIntent"
    },
    {
      "slots": [
        {
          "name": "SAddress",
          "type": "AMAZON.PostalAddress"
        }
      ],
      "intent": "SecondAddressSavingIntent"
    },
    {
      "slots": [
        {
          "name": "radius",
          "type": "AMAZON.NUMBER"
        }
      ],
      "intent": "DistanceSavingIntent"
    },
    {
      "intent": "YesIntent"
    },
    {
      "intent": "NoIntent"
    }
  ]
}

(For Sample Utterances):
FirstAddressSavingIntent first is {FAddress}
SecondAddressSavingIntent second is {SAddress}
DistanceSavingIntent radius is {radius}
YesIntent yes
YesIntent ok
NoIntent no

In your terminal, run python meetups.py as well as the ngrok server.
