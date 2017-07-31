import pickle
import numpy as np
from collections import Counter
from SearchEngine import SearchEngine

class Database:
    def __init__(self, file = "database.pkl"):
        """
        Initializes a new Database

        Parameters
        ----------
        file: String
            path to database file (.pkl)

        Returns
        -------
        None
        """
        self.file = file #database file
        try:
            self.engine, self.entities = self.getDatabase()
            print("Loaded from database", flush = True)
        except EOFError:
            self.engine = SearchEngine()
            self.entities = {}
        
    def __repr__(self):
        return "{}".format(self.engine.raw_text.keys())

    def addDocument(self, text_id, text):
        """
        Adds a document to the database

        Parameters
        ----------
        id: id of document to add
        text: rawtext

        Returns
        -------
        None
        """
        #TODO: Finish
        self.engine.add(text_id, text)
        entities_list = self.engine.getEntities(text)
        self.entities[text_id]= entities_list
        for entity in entities_list:
            self.engine.inverted_index[entity].add(text_id)
        self.updateDatabase()

    def updateDatabase(self):
        """
        Writes self.engine and self.entities to database file

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        with open(self.file, "wb") as f:
            pickle.dump((self.engine, self.entities), f)

    def getDatabase(self):
        """
        Retrieves engine and entities from saved database file

        Parameters
        ----------
        None

        Returns
        -------
        Tuple of (engine, entities), where music and songs are both dictionaries
        """
        with open(self.file, "rb") as f:
            engine, entities = pickle.load(f)
        return (engine, entities)

    def removeDocument(self, text_id):
        """
        Removes a document from the database

        Parameters
        ----------
        text_id: string
            text_id of document to remove

        Returns
        -------
        None
        """
        self.engine.remove(text_id)
        for entity in self.entities[text_id]:
            if text_id in self.engine.inverted_index[entity]:
                self.engine.inverted_index[entity].remove(text_id)

        del self.entities[text_id]
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
        self.engine = SearchEngine()
        self.entities = {}
        self.updateDatabase()