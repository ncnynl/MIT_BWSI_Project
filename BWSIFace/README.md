
<content> <
# Facial Recognition / symmetry test
Our Facial Recognition program is able to take in images of faces from either the built-in camera or a file and break it down. After it breaks down into arrays of numbers, it compares the image with the ones stored in the database to correctly label the face/person.  Also, if given a number of images, it is able to group the images based on the person.  Basically, it clusters the groups of photos by person and gives the labels to them if the information is provided in the database.   
## Usage
Open command line or git bash and run python main.py.  There will be questions prompting you for actions to preform.  Follow the text to get desired output.  

The commands: 
 - save: this command has two subcommands
 	- camera: this uses the built in camera on your device and takes a picture.  Then the command prompt will ask you to name the picture so it can save it to the database
 	- file: this asks for a file so it can import it and save it to the database, it will then ask who is in the photo so it can save the names

 - view: this command views who is in the database
 - clear: this command clears the database
 - loadimgs: this command loads the images
 - remove: this command will remove a specified image 
 - recognize: this is where the magic happens.  The computer, depending on which program you run (whispers or BWSIFace) will recognize images through either the camera or pre-existing jpegs.  If it requires a picture, it will use the built - in camera and then output the name of which image it thinks the picture is.  Using whispers causes the computer to cluster the images by person
 - sym: this does a symmetry test on your face. You can use the camera or a file saved in that directory to perform the test on.

## Prerequisites: dlib (comamnds to run) and opencv and imutils
- conda install -c conda-forge dlib
- python setup.py develop
- conda install -c conda-forge opencv # for windows users
- pip install imutils

## History
This program was written over two days on July 20, 2017 to July 21, 2017
## Credits
Contributors: Sky Li, Brandon Zhang, Rishi Wadhwa, and Julie Lee (Our bosses are Ryan Soklaski and Melanie Chen and the crew of Beaverworks Summer Institute)
## License
This innovative technology has been patented and copyrighted already under the team name "Rice Kripsies" and any attempts to use this program for profitable uses must get permission.  
> 
</content>
 

