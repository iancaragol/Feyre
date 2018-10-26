import os
import random
import difflib

class Feats():
    """
    Class for searching the PH for feats
    """
    def __init__(self):
        #skipped all non PH feats from Dwarven Fortitude down
        self.featDictionary = {} #maps feat names to descriptions
        self.featList = [] #list of all feats
        self.setup()

    def setup(self):
        """
        Reads all txt files in _data/_feats and stores them in featDictionary
        """
        pyDir = os.path.dirname(__file__)
        relPath = "_data//_feats"
        absRelPath = os.path.join(pyDir, relPath)

        for file in os.listdir(absRelPath):
                self.featDictionary[file.replace(".txt", "")] = self.readForDict(file)
        self.featList = list(self.featDictionary)

    async def search(self, message):
        """
        Searches the feat dictionary for the closest feat and returns a string with that feats description
        """
        feat = message[6:]
        closeMatches = difflib.get_close_matches(feat, list(self.featDictionary.keys()))

        if(len(closeMatches) == 0):
            retArr = []
            retArr.append("An error occurred.")
            retArr.append("*I'm sorry, I was unable to find the feat you are looking for.*")
            return retArr

        return self.featDictionary[closeMatches[0]]
    
    async def randFeat(self):     
        """
        Returns a string with a description of a random feat
        """
        roll = random.randint(0, len(self.featList) - 1)
        feat = self.featList[roll]

        return self.featDictionary[feat]

    def readForDict(self, filename):
         """
         Used for setup, reads all text files and adds them to feat dictionary
         """
         pyDir = os.path.dirname(__file__)
         relPath = "_data//_feats"
         absRelPath = os.path.join(pyDir, relPath)
         file = open(os.path.join(absRelPath, filename), 'r', encoding = 'latin-1')

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



    def readAndFormat(self, matches):
         """
         Legacy code, replaced by readForDict()
         """
         pyDir = os.path.dirname(__file__)
         relPath = "_data//_feats"
         absRelPath = os.path.join(pyDir, relPath)

         filename = self.featDictionary[matches[0]]
         file = open(os.path.join(absRelPath, filename), 'r', encoding = 'latin-1')

         retArr = []
         retStr = ""

         i = 0
         for line in file:
             if (i == 0):
                 retArr.append(line)
                 i = 1
             else:
                 retStr += line

         #print(retStr)
         retArr.append(retStr)
         return retArr