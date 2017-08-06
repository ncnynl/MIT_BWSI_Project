# Card Recognition
This Alexa skill can identify a standard playing card

#### Installation

As of now, this skill has no intents

#### Usage

This skill runs off of a Flask server, using ngrok to connect outside of localhost

Before running, make sure that the ```FLASK_APP``` environment variable is set to app.py

To start the server:
```
flask run -p [port]
```

To host on ngrok:
```
ngrok http [port]
```

Create a new skill in Alexa with:

##### Intent Schema (with placeholder intent) 
```
{
  "intents": [
    {
      "intent": "pokerIntent"
    }
  ]
}

```
##### Sample Utterances (with placeholder intent)
```
pokerIntent poker
```

Set your https node to the generated ngrok https url

#### Planned Features/ Future Steps

~~Suit recognition (DONE)~~
* Poker hand analysis
* AI to play card games based off video


Using flask, flask-ask

Built at Cogworks@Beaverworks Summer Institute 2017
