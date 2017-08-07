# Card Recognition
This Alexa skill can identify a standard playing card

#### Prerequisites
* NumPy
* Flask, Flask-Ask
* dlib
* OpenCV
* tensorflow
* [Cogworks 2017's camera module](https://github.com/LLCogWorks2017/Camera)


#### Usage
  
This skill runs off of a Flask server, using ngrok to connect outside of localhost

Before running, make sure that the ```FLASK_APP``` environment variable is set to ```app.py```

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
* Speed up suit recognition
* Poker hand analysis
* AI to play card games based off video


Using flask, flask-ask

Built at Cogworks@Beaverworks Summer Institute 2017
