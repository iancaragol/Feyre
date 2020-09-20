import os
import difflib
import random
import asyncio

import discord
from discord.ext import commands

class ClassFeatures():
    def __init__(self):
        self.classDictionary = {}
        self.classList = []
        self.setup()
      
    def setup(self):
        pyDir = os.path.dirname(__file__)
        relPath = "../_data/_character_classes"
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
         relPath = "..//_data//_character_classes"
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

class ClassFeaturesCog(commands.Cog):
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
        self.class_features = ClassFeatures()

    @commands.command(aliases=['class', 'C', 'Class'])
    async def c(self, ctx, *, args = None):
        """
        Searches the Player's Handbook for a spell
        """
        # if (ctx.author.id not in self.bot.data.userSet):
        self.data.userSet.add(ctx.author.id)
        self.data.statsDict['!c'] += 1

        if not args:
            await ctx.send('''```Missing command arguments, see !help class for more information.\nEx: !c Wizard```''')
            return

        classArr = await self.class_features.search(args)
        if (classArr == False):
            await ctx.send("```I'm sorry. I wasn't able to find the class you are looking for. I can only support classes from the Standard Reference Document for copyright reasons.```")
        else:
            await self.send_class(ctx, classArr)
        
     
    async def send_class(self, ctx, class_tup):
        if(len(class_tup[1]) < 2048): # Discord Character Limit is 2048
            embed = discord.Embed(title = class_tup[0], description = class_tup[1])#, color=data.embedcolor)
            await ctx.send(embed = embed)

        #discord has a 2048 character limit so this is needed to split the message into chunks
        else:
            s = class_tup[1]
            parts = await self.data.string_splitter(s, '\n', 10) # Helper function from BotData
                        
            for i in range(len(parts)):
                if(i == 0):
                    embed = discord.Embed(title = class_tup[0], description = parts[i])#, color=data.embedcolor)
                else:
                    embed = discord.Embed(title = class_tup[0] + " *- Continued*", description = parts[i])#, color=data.embedcolor)
                await ctx.send(embed = embed)