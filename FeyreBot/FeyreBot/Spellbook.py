import os
import difflib
import random
import asyncio

#Bestow curse required some editing because of a hyperlink

class Sb():
    def __init__(self):
        self.spellDictionary = {}
        self.spellList = []
        self.setup()
      
    def setup(self):
        pyDir = os.path.dirname(__file__)
        relPath = "_data//_spells"
        absRelPath = os.path.join(pyDir, relPath)

        for file in os.listdir(absRelPath):
                self.spellDictionary[file.replace(' ', '-').replace(".txt", "")] = self.readForDict(file)
        self.spellList = list(self.spellDictionary)

    async def search(self, message):
        """
        Searches the feat dictionary for the closest feat and returns a string with that feats description
        """
        spell = message
        closeMatches = difflib.get_close_matches(spell, list(self.spellDictionary.keys()))

        if(len(closeMatches) == 0):
            retArr = []
            retArr.append("An error occurred.")
            retArr.append("*I'm sorry, I was unable to find the feat you are looking for.*")
            return retArr

        return self.spellDictionary[closeMatches[0]]

    def readForDict(self, filename):
         pyDir = os.path.dirname(__file__)
         relPath = "_data//_spells"
         absRelPath = os.path.join(pyDir, relPath)
         file = open(os.path.join(absRelPath, filename), 'r', encoding = 'ascii')

         retArr = []
         retStr = ""

         i = 0
         for line in file:
             if (i == 0):
                 retArr.append(line)
                 i = 1
             else:
                 retStr += line

         retArr.append(retStr)
         return retArr