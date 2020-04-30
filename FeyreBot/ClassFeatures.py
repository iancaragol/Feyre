import os
import difflib
import random
import asyncio

class ClassFeatures():
    def __init__(self):
        self.classDictionary = {}
        self.classList = []
        self.setup()
      
    def setup(self):
        pyDir = os.path.dirname(__file__)
        relPath = "_data/_classes"
        absRelPath = os.path.join(pyDir, relPath)

        for file in os.listdir(absRelPath):
                self.classDictionary[file.replace(' ', '-').replace(".txt", "").lower()] = self.readForDict(file)
        self.classList = list(self.classDictionary)

    async def search(self, message):
        """
        Searches the feat dictionary for the closest feat and returns a string with that feats description
        """
        class_info = message.lower()
        closeMatches = difflib.get_close_matches(class_info, list(self.classDictionary.keys()))

        if(len(closeMatches) == 0):
            return False

        return self.classDictionary[closeMatches[0]]

    def readForDict(self, filename):
         pyDir = os.path.dirname(__file__)
         relPath = "_data//_classes"
         absRelPath = os.path.join(pyDir, relPath)
         file = open(os.path.join(absRelPath, filename), 'r', encoding = 'utf-8')

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