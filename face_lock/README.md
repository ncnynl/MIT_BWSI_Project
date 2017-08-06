
<content> <
# Facial Lock
Our Facial Lock program is able to take in images of faces from either the built-in camera or a file and break it down. When launched, the program will ask if you want to store or retrieve a password.  If you want to store one, it will take a picture and compare the image with the ones stored in the database to see if you are in there.  If not, it will ask for your name and then proceed with the code.  The program afterwards will ask for the website you want to store the webiste to and then ask you in the command line to enter your password.  

If you want to retrieve a password, the built-in camera will take an image of you and determine who you are by comparing the image array with the ones in the database.  If the computer finds you in the database, it will print out the passwords.  The computer then runs through your passwords and determine if each is a weak or strong password using a built-in algorithm.  If a password is weak, then it will say the password out loud to force you to change it.  Also, if there are multiple people behind you while retrieving the passwords, the computer will throw an error so no passwords are printed for security.   
Open command line or git bash and run python app.py.  There will be questions from Alexa prompting you for actions to preform.  Follow Alexa to get desired output.  

The launch command: "password"

## Installation

Intent Schema
```
 {
  "intents": [
    {
      "intent": "StoreIntent"
    },
    {
      "slots": [
        {
          "name": "name",
          "type": "AMAZON.US_FIRST_NAME"
        }
      ],
      "intent": "AddNewProfileIntent"
    },
    {
      "slots": [
        {
          "name": "website",
          "type": "AMAZON.LITERAL"
        }
      ],
      "intent": "AppendPasswordsIntent"
    },
    {
      "intent": "RetrievePasswordIntent"
    },
    {
      "intent": "NoIntent"
    }
  ]
}
```

Utterances
```
StoreIntent store
StoreIntent store a password
AddNewProfileIntent {name}
AppendPasswordsIntent {google|website}
AppendPasswordsIntent {wikipedia|website}
AppendPasswordsIntent {Huffington Post|website}
AppendPasswordsIntent {Washington Post|website}
AppendPasswordsIntent {YouTube|website}
AppendPasswordsIntent {Comcast|website}
AppendPasswordsIntent {FaceBook|website}
AppendPasswordsIntent {Yahoo|website}
AppendPasswordsIntent {Twitter|website}
AppendPasswordsIntent {NFL|website}
AppendPasswordsIntent {CNN|website}
AppendPasswordsIntent {amazon|website}
AppendPasswordsIntent {BBC|website}
AppendPasswordsIntent {AoPS|website}
AppendPasswordsIntent {Instagram|website}
AppendPasswordsIntent {NY Times|website}
AppendPasswordsIntent {Steam|website}
AppendPasswordsIntent {Blizzard|website}
RetrievePasswordIntent retrieve
RetrievePasswordIntent retrieve passwords
NoIntent no
NoIntent nope
NoIntent no thanks
```

## History
This program was written over four days from August 2, 2017 to August 5, 2017
## Credits
Contributors: Sky Li, Brandon Zhang, Rishi Wadhwa, and Julie Lee (Our bosses are Ryan Soklaski and Melanie Chen and the crew of Beaverworks Summer Institute)
## License
This innovative technology has been patented and copyrighted already under the team name "Rice Kripsies" and any attempts to use this program for profitable uses must get permission.  
> 
</content>
 

