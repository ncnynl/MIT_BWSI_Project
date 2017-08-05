from flask import Flask
from flask_ask import Ask, statement, question, session
import requests
import time
import unidecode
import json
import youtube_dl
import urllib
from urllib.request import urlopen
import urllib.parse
import os
from bs4 import BeautifulSoup
from songfp.database import Database
from songfp.audio import *
from songfp.fingerprint import Fingerprint



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
    textToSearch = keyword
    query = urllib.parse.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.find(id = "content").prettify())
    vid = soup.find_all(class_= 'yt-uix-tile-link')[0]
        #print 'https://www.youtube.com' + vid['href']
    link = 'https://www.youtube.com' + vid['href']
    print(link)
    return link

@ask.intent("SongRecognitionIntent")
def actions(Action):
    if Action == "save":
        msg = "What song would you like to save"
        return question(msg)

    if Action == "recognize":
        fingerp = get_song()
        db = Database("songfp/music.pkl")
        songmatch = fingerp.best_match(db)
        print(songmatch)
        song_msg = "The title of this song is {}".format(songmatch)
        return statement(song_msg)


@ask.intent("FileSavingIntent")
def savefile(Song):
    print(Song, flush = True)
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

    savepath = make_savepath(Song)
    print(savepath)
    with youtube_dl.YoutubeDL(options) as ydl:
        result = ydl.extract_info(link, download=True)
        os.rename(result['id'], savepath)
        # title = result['id']
    # print(title)
    # print(file)
    freqs, times, S = sample("songs/{}.mp3".format(Song))
    fp = Fingerprint(S, freqs, times)
    db = Database("songfp/database.pkl")

    print(type(fp))
    db.addSong(fp, Song)

def make_savepath(title):
    savedir = "songs"
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    return os.path.join(savedir, "%s.mp3" % (title))



def get_song():

    freqs, times, S = mic(3)
    fp = Fingerprint(S, freqs, times)
    return fp

if __name__ == '__main__':
    app.run(debug=True)
