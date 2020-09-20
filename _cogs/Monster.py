import os
import difflib
import random
import asyncio

import discord
from discord.ext import commands

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
        relPath = "..//_data//_monsters"
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

        if(len(closeMatches) == 0):
            return False

        elif(len(closeMatches) == 3):
            otherMatches = "\n *Did you mean these? " + closeMatches[1] + " or " + closeMatches[2] + "*"

        elif(len(closeMatches) == 2):
            otherMatches = "\n *Did you mean this? " + closeMatches[1] +"*"

        retArr = self.monsterDictionary[closeMatches[0]]
        retArr[1] += "" #otherMatches, removed this at user request

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
         relPath = "..//_data//_monsters"
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


class MonsterManualCog(commands.Cog):
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
        self.monster_manual = MonsterManual()

    @commands.command(aliases=['monster', 'Monster', 'MM', 'Mm'])
    async def mm(self, ctx, *, args = None):
        """
        Searches the Player's Handbook for a spell
        """
        # if (ctx.author.id not in self.bot.data.userSet):
        self.data.userSet.add(ctx.author.id)
        self.data.statsDict['!mm'] += 1

        if not args:
            await ctx.send('''```Missing command arguments, see !help mm for more information.\nEx: !mm Tarrasque```''')
            return

        mmArr = await self.monster_manual.search(args)
        if (mmArr == False):
            await ctx.send("```I'm sorry. I wasn't able to find the monster you are looking for. I can only support monsters from the Standard Reference Document for copyright reasons.```")
        else:
            await self.send_monster(ctx, mmArr)
        
     
    @commands.command()
    async def randmonster(self, ctx, args = None):
        """
        Gives a random monster from the Monster Manual
        """
        self.data.userSet.add(ctx.author.id)
        self.data.statsDict['!randmonster'] += 1
        mmArr = await self.monster_manual.randMonster()
        await self.send_monster(ctx, mmArr)

    async def send_monster(self, ctx, monster_tup):
        if(len(monster_tup[1]) < 2048): # Discord Character Limit is 2048
            embed = discord.Embed(title = monster_tup[0], description = monster_tup[1])#, color=data.embedcolor)
            await ctx.send(embed = embed)

        #discord has a 2048 character limit so this is needed to split the message into chunks
        else:
            s = monster_tup[1]
            parts = await self.data.string_splitter(s, '\n', 10) # Helper function from BotData
                        
            for i in range(len(parts)):
                if(i == 0):
                    embed = discord.Embed(title = monster_tup[0], description = parts[i])#, color=data.embedcolor)
                else:
                    embed = discord.Embed(title = monster_tup[0].strip() + " *- Continued*", description = parts[i])#, color=data.embedcolor)
                await ctx.send(embed = embed)