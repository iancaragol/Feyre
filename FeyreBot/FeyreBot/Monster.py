import os
import difflib
import random
import asyncio

class MonsterManual():
    """
    Class for searching and getting random monsters from the monster manual. All monsters are stored as
    markdown files in _data/_monsters
    """
    def __init__(self):
        self.monsterDictionary = {}
        self.mmList = []
        self.setup()
        

    def setup(self):
        """
        Constructs the monster dictionary by reading from all markdown files in _data/_monsters
        """
        pyDir = os.path.dirname(__file__)
        relPath = "_data//_monsters"
        absRelPath = os.path.join(pyDir, relPath)

        for file in os.listdir(absRelPath):
                self.monsterDictionary[file.replace(' ', '-').replace(".markdown", "")] = self.readForDict(file)
        self.mmList = list(self.monsterDictionary)

    async def search(self, message):
        """
        Searches for a monster that matches the message most closely and returns its description as a string.
        """
        #monster = message[4:] #remove !mm
        monster = message
        monster.replace(' ', '-')
        closeMatches = difflib.get_close_matches(monster, list(self.monsterDictionary.keys()))
        otherMatches = ""

        if(len(closeMatches) == 0):
            retArr = []
            retArr.append("An error occurred.")
            retArr.append("*I'm sorry, I was unable to find the monster you are looking for.*")
            return retArr

        elif(len(closeMatches) == 3):
            otherMatches = "\n *Did you mean these? " + closeMatches[1] + " or " + closeMatches[2] + "*"

        elif(len(closeMatches) == 2):
            otherMatches = "\n *Did you mean this? " + closeMatches[1] +"*"

        retArr = self.monsterDictionary[closeMatches[0]]
        retArr[1] += otherMatches

        return retArr

    async def randMonster(self): 
        """
        Returns a random monster description
        """
        roll = random.randint(0, len(self.mmList) - 1)
        monster = self.mmList[roll]

        return self.monsterDictionary[monster]

    def readForDict(self, filename):
         """
         Reads all markdown files in _data/_monster and adds them to the monster dictionary with the proper format
         """
         pyDir = os.path.dirname(__file__)
         relPath = "_data//_monsters"
         absRelPath = os.path.join(pyDir, relPath)

         file = open(os.path.join(absRelPath, filename), 'r', encoding = 'latin-1')

         retArr = []
         retStr = ""

         i = 0
         for line in file:
             if (i == 2):
                 retArr.append("***"+line.replace("title: ", '').replace('"', '')+"***")

             if (i > 7):
                retStr += line

             i+=1

         retArr.append(retStr)
         return retArr
 
    def fixFileNames(self):
            """
            Helper to rename all of the monster markdown files
            """
            pyDir = os.path.dirname(__file__)
            relPath = "_data//"
            absRelPath = os.path.join(pyDir, relPath)

            for filename in os.listdir(absRelPath):
                new_file_name = filename[11:]

                try:
                    os.rename(os.path.join(absRelPath, filename), os.path.join(absRelPath, new_file_name)) 
                except:
                    os.remove(os.path.join(absRelPath, new_file_name))
                    os.rename(os.path.join(absRelPath, filename), os.path.join(absRelPath, new_file_name)) 

