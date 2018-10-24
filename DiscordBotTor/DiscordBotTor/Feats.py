import os
import random
import difflib

class Feats():
    def __init__(self):
        #maps feat names to file names
        #skipped all non PH feats from Dwarven Fortitude down
        self.featDictionary = {}
        self.featList = []
        self.setup()

    def setup(self):
        pyDir = os.path.dirname(__file__)
        relPath = "_data//_feats"
        absRelPath = os.path.join(pyDir, relPath)

        for file in os.listdir(absRelPath):
                self.featDictionary[file.replace(".txt", "")] = self.readForDict(file)
        self.featList = list(self.featDictionary)

    async def search(self, message):
        #!feat Name
        feat = message[6:]
        closeMatches = difflib.get_close_matches(feat, list(self.featDictionary.keys()))

        if(len(closeMatches) == 0):
            retArr = []
            retArr.append("An error occurred.")
            retArr.append("*I'm sorry, I was unable to find the feat you are looking for.*")
            return retArr

        return self.featDictionary[closeMatches[0]]
        #return self.readAndFormat(closeMatches)
    
    async def randFeat(self):     
        roll = random.randint(0, len(self.featList) - 1)
        feat = self.featList[roll]

        return self.featDictionary[feat]

    def readForDict(self, filename):
         pyDir = os.path.dirname(__file__)
         relPath = "_data//_feats"
         absRelPath = os.path.join(pyDir, relPath)
         file = open(os.path.join(absRelPath, filename), 'r')

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



    def readAndFormat(self, matches):
         pyDir = os.path.dirname(__file__)
         relPath = "_data//_feats"
         absRelPath = os.path.join(pyDir, relPath)

         filename = self.featDictionary[matches[0]]
         file = open(os.path.join(absRelPath, filename), 'r')

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