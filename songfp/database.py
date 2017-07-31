import pickle
import numpy as np
from collections import Counter

class Database:

    def __init__(self, file):
        """
        Initializes a new Database

        Parameters
        ----------
        file: String
            path to database file (.pkl)

        Returns
        -------
        Database?
        """

        self.file = file #database file
        try:
            self.music, self.songs = self.getDatabase()
            print("Loaded from database", flush = True)
        except EOFError:
            self.music = {}
            #self.counter = 0
            self.songs = {} 
        
    def __repr__(self):
        return "{}".format(self.music)

    #notes is a numpy array of numpy arrays which each contains the two notes with the delta t between them
    def addSong(self, fp, song_name):
        """
        Adds a song to the database

        Parameters
        ----------
        fp: Fingerprint
            Fingerprint of song to add
        song_name: String
            Name of song to add

        Returns
        -------
        None
        """

        count = len(self.songs)
        self.songs[count] = song_name
        keys = fp.fingerprint[:, 0]
        times = fp.fingerprint[:, 1]
        for i in range(len(keys)):
            if keys[i] in self.music:
                self.music[keys[i]].append((count, times[i]))
            else:
                self.music[keys[i]] = [(count, times[i])]

        self.updateDatabase()

    def updateDatabase(self):
        """
        Writes self.music and self.songs to database file

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # self.music = self.getDatabase()
        with open(self.file, "wb") as f:
            pickle.dump((self.music, self.songs), f)

    def getDatabase(self):
        """
        Retrieves music and songs from saved database file

        Parameters
        ----------
        None

        Returns
        -------
        Tuple of (music, songs), where music and songs are both dictionaries
        """
        with open(self.file, "rb") as f:
            music, songs = pickle.load(f)
        return (music, songs)

    def removeSong(self, fp):
        #self.music = getDatabase()
        """
        Removes a song from the database

        Parameters
        ----------
        fp: fingerprint
            Fingerprint of song to remove

        Returns
        -------
        None
        """
        keys = fp.fingerprint[:, 0]
        for i in keys:
            del self.music[i]
        self.updateDatabase()
    def clear(self):
        """
        Clears the database

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.music = {}
        self.songs = {}
        self.updateDatabase()
    def bestMatch(self, fp):
        """
        Finds the best match for an audio sample

        Parameters
        ----------
        fp:Fingerprint
            fingerprint of audio to match
        
        Returns
        -------
        String
            Song name
        """
        #self.music = self.getDatabase()
        counterlst = []
        for i in range(len(fp.fingerprint)):
            key = fp.fingerprint[i, 0]
            time1 = fp.fingerprint[i, 1]
            songs = self.music.get(key, None) #Array of None
            if(songs == None):
                continue

            for j in range(len(songs)):
                song, time2 = songs[j]
                counterlst.append((self.songs[song], np.abs(time2-time1)))

        b = Counter(counterlst)
        return b.most_common(1)