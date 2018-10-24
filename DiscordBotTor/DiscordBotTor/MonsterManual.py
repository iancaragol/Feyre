import os
import difflib
import random
import asyncio

#Gets a monster from the D&D monster manual
class MonsterManual():
    def __init__(self):
        #maps monster names to monster manual arrays
        self.monsterDictionary = {}
        self.mmList = []
        self.setup()
        

    def setup(self):
        pyDir = os.path.dirname(__file__)
        relPath = "_data//_monsters"
        absRelPath = os.path.join(pyDir, relPath)

        for file in os.listdir(absRelPath):
                self.monsterDictionary[file.replace(' ', '-').replace(".markdown", "")] = self.readForDict(file)
        self.mmList = list(self.monsterDictionary)

    #searches for the monster that matches the search message most closely
    async def search(self, message):
        monster = message[4:]
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

    #gives a random monster
    async def randMonster(self):      
        roll = random.randint(0, len(self.mmList) - 1)
        monster = self.mmList[roll]

        return self.monsterDictionary[monster]

    #helper for setup
    def readForDict(self, filename):
         pyDir = os.path.dirname(__file__)
         relPath = "_data//_monsters"
         absRelPath = os.path.join(pyDir, relPath)

         file = open(os.path.join(absRelPath, filename), 'r', encoding='utf-8')

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
 
    #helper to fix markdown files
    def fixFileNames(self):
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

