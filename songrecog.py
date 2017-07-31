from flask import Flask
from flask_ask import Ask, statement, question, session
import requests
import time
import unidecode
import json
from __future__ import unicode_literals
import youtube_dl
import urllib
import urllib2
import os
from bs4 import BeautifulSoup
from BWSI-Song-Recognition import Database
from BWSI-Song-Recognition import Audio
from BWSI-Song-Recognition import fingerprint


db = Database()

app = Flask(__name__)
ask = Ask(app, '/')

@app.route('/')
def homepage():
    return "Hello"

@ask.launch
def start_skill():
    msg = "Hello. What would you like to do?"
    return question(msg)



def youtubefile(keyword):
    textToSearch = 'keyword'
    query = urllib.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    vid = soup.findAll(attrs={'class':'yt-uix-tile-link'})[0]
        #print 'https://www.youtube.com' + vid['href']
    link = 'https://www.youtube.com' + vid['href']
    return link

@ask.intent("SongRecognitionIntent")
def actions(Action):
    if Action = "save":
        msg = "What song would you like to save"
        return question(msg)

    if Action = "recognize":
        fingerp = get_song()
        songmatch = fingerp.best_match(db)
        song_msg = "The title of this song is {}".format(songmatch)
        return statement(song_msg)


@ask.intent("FileSavingIntent")
def savefile(Song):
    session.attributes["Song"] = Song
    name = session.attributes["Song"]
    link = youtubefile(name)
    #webm = os.system("youtube-dl --title" +link)
    #conversion = ffmpeg -i webm -acodec libmp3lame -aq 4 output.mp3
    ydl = youtube_dl.YoutubeDL()
    options = {
    'format': 'bestaudio/best',
    'extractaudio' : True,  # only keep the audio
    'audioformat' : "mp3",  # convert to mp3
    'outtmpl': '%(id)s',    # name the file the ID of the video
    'noplaylist' : True,    # only download single song, not playlist
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        file = ydl.download(['link'])
    freqs, times, S = Audio.sample(file)
    fp = Fingerprints(S, freqs, times)
    r = none
    with ydl:
    r = ydl.extract_info(url, download=False)
    title = r['title']
    db.addsong(fp.fingerprint, title)




def get_song():
    freqs, times, S = Audio.mic()
    fp = Fingerprint(S, freqs, times)
    return fp

if __name__ == '__main__':
    app.run(debug=True)
