
# Math
Our math program is able to take in math problems from people and through Wolfram Alpha's API, obtain an answer. The answer is then processed through formatting to ensure that Alexa can read it correctly.  Despite the fact that this program is simple because it uses Wolfram Alpha directly, we thought it would be good if Wolfram Alpha's technology was applied to a cognitive assitant to ensure easy access for users.  This allows many users to multi-task or calculate on the fly to ensure maximum efficiency.  

## Usage

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

##### Intent Schema
```
{
  "intents": [
    {
      "slots": [
        {
          "name": "equation",
          "type": "AMAZON.LITERAL"
        }
      ],
      "intent": "mathIntent"
    },
    {
      "intent": "NoIntent"
    }
  ]
}
```
##### Sample Utterances
```
mathIntent {x squared plus three x minus two equals zero solve for x|equation}
mathIntent {integrate x plus three|equation}
mathIntent {derivative of x cubed minus five|equation}
mathIntent {compute the integral of x divided by five|equation}
NoIntent nothing
NoIntent cancel
NoIntent bye
```

## History
This program was written over 5 days from August 2, 2017 to August 5, 2017

## Credits
Contributors: Sky Li, Brandon Zhang, Rishi Wadhwa, and Julie Lee (Our bosses are Ryan Soklaski and Melanie Chen and the crew of Beaverworks Summer Institute)
 
