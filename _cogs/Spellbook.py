import os
import difflib
import random
import asyncio
import numpy
import discord
from discord.ext import commands

#Bestow curse required some editing because of a hyperlink

class Spellbook():
    def __init__(self):
        self.spellDictionary = {}
        self.spellList = []
        self.setup()
      
    def setup(self):
        pyDir = os.path.dirname(__file__)
        relPath = "..//_data//_spells"
        absRelPath = os.path.join(pyDir, relPath)

        for file in os.listdir(absRelPath):
                self.spellDictionary[file.replace(' ', '-').replace(".txt", "").lower()] = self.readForDict(file)
        self.spellList = list(self.spellDictionary)

    async def search(self, message):
        """
        Searches the feat dictionary for the closest feat and returns a string with that feats description
        """
        spell = message.lower()
        closeMatches = difflib.get_close_matches(spell, list(self.spellDictionary.keys()))

        if(len(closeMatches) == 0):
            return False

        return self.spellDictionary[closeMatches[0]]

    def readForDict(self, filename):
         pyDir = os.path.dirname(__file__)
         relPath = "..//_data//_spells"
         absRelPath = os.path.join(pyDir, relPath)
         file = open(os.path.join(absRelPath, filename), 'r', encoding = 'ascii')

         spell_title = ""
         spell_description = ""

         i = 0
         for line in file:
             if (i == 0):
                 spell_title = line
                 i = 1
             else:
                 spell_description += line

         return (spell_title, spell_description)

class SpellbookCog(commands.Cog):
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
        self.spellbook = Spellbook()

    @commands.command(aliases=['Spell', 's', 'S'])
    async def spell(self, ctx, *, args = None):
        """
        Searches the Player's Handbook for a spell
        """
        # if (ctx.author.id not in self.bot.data.userSet):
        self.data.userSet.add(ctx.author.id)
        self.data.statsDict['!spell'] += 1

        if not args:
            await ctx.send('''```Missing command arguments, see !help spell for more information.\nEx: !spell Wish```''')
            return

        spell_tup = await self.spellbook.search(args) #(Title, Description)

        if (spell_tup == False): # Returns false if nothing was found
            await ctx.send("```I'm sorry. I wasn't able to find the spell you are looking for. I can only support spells from the Standard Reference Document for copyright reasons.```")
        else:
            await self.send_spell(ctx, spell_tup)

    async def send_spell(self, ctx, spell_tup):
        if(len(spell_tup[1]) < 2048): # Discord Character Limit is 2048
            embed = discord.Embed(title = spell_tup[0], description = spell_tup[1])#, color=data.embedcolor)
            await ctx.send(embed = embed)

        #discord has a 2048 character limit so this is needed to split the message into chunks
        else:
            s = spell_tup[1]
            parts = await self.data.string_splitter(s, '\n', 5) # Helper function from BotData
                        
            for i in range(len(parts)):
                if(i == 0):
                    embed = discord.Embed(title = spell_tup[0], description = parts[i])#, color=data.embedcolor)
                else:
                    embed = discord.Embed(title = spell_tup[0] + " *- Continued*", description = parts[i])#, color=data.embedcolor)
                await ctx.send(embed = embed)

