import os
import difflib
import random

#Gets a monster from the D&D monster manual
class MonsterManual():
    def __init__(self):
        #maps monster names to file names
        self.monsterDictionary = {}
        self.setup()

    def setup(self):
        pyDir = os.path.dirname(__file__)
        relPath = "_data\\_monsters"
        absRelPath = os.path.join(pyDir, relPath)

        for file in os.listdir(absRelPath):
                self.monsterDictionary[file.replace(' ', '-').replace(".markdown", "")] = file

    def search(self, message):
        monster = message[4:]
        monster.replace(' ', '-')
        closeMatches = difflib.get_close_matches(monster, list(self.monsterDictionary.keys()))

        if(len(closeMatches) == 0):
            retArr = []
            retArr.append("An error occurred.")
            retArr.append("*I'm sorry, I was unable to find the monster you are looking for.*")
            return retArr

        return self.readAndFormat(closeMatches)

    def readAndFormat(self, matches):
         pyDir = os.path.dirname(__file__)
         relPath = "_data\\_monsters"
         absRelPath = os.path.join(pyDir, relPath)


         filename = self.monsterDictionary[matches[0]]
         file = open(os.path.join(absRelPath, filename), 'r')

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

    def randMonster(self):
        mmList = list(self.monsterDictionary)
        roll = random.randint(0, len(mmList) - 1)

        mHelp = []
        monster = mmList[roll]
        mHelp.append(monster)

        return self.readAndFormat(mHelp)

    def fixFileNames(self):
            pyDir = os.path.dirname(__file__)
            relPath = "_data\\"
            absRelPath = os.path.join(pyDir, relPath)

            for filename in os.listdir(absRelPath):
                new_file_name = filename[11:]

                try:
                    os.rename(os.path.join(absRelPath, filename), os.path.join(absRelPath, new_file_name)) 
                except:
                    os.remove(os.path.join(absRelPath, new_file_name))
                    os.rename(os.path.join(absRelPath, filename), os.path.join(absRelPath, new_file_name)) 

