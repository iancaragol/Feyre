import os
import difflib
import random
import asyncio

class Spelbook():
    def __init__(self):
        self.spellDictionary = {}
        self.spellList = []
        self.setup()

    def setup(self):
        pyDir = os.path.dirname(__file__)
        relPath = "_data//_spells"
        absRelPath = os.path.join(pyDir, relPath)

        for file in os.listdir(absRelPath):
                self.spellDictionaryDictionary[file.replace(' ', '-').replace(".txt", "")] = self.readForDict(file)
        self.spellList = list(self.monsterDictionary)


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