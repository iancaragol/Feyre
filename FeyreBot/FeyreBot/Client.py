#id 500733845856059402
#test id 505120997658329108

#permissions 67648
#test permissions 75776
#https://discordapp.com/oauth2/authorize?client_id=500733845856059402&scope=bot&permissions=67648
#https://discordapp.com/oauth2/authorize?client_id=505120997658329108&scope=bot&permissions=75776

from BookOfTor import BookOfTor
from Monster import MonsterManual
from Feat import Feats
from Spellbook import Sb
from DiceRolls import Roller
from Init import Initiative

import discord
import asyncio
import time
import math
import re
import random
import json
import os
import sys

from discord.voice_client import VoiceClient

class MyClient(discord.Client):
    def __init__(self):
        self.initDict = {}
        self.initEmbedDict = {}
        self.bt = BookOfTor()
        self.mm = MonsterManual()
        self.sb = Sb()
        self.f = Feats()
        self.dr = Roller()
        self.embedcolor = discord.Color.from_rgb(165,87,249)

        try:
            pyDir = os.path.dirname(__file__)
            relPath = "_data//stats.txt"
            absRelPath = os.path.join(pyDir, relPath)
            self.statsDict = json.load(open(absRelPath))

        except Exception:
            self.statsDict = {'!tor horo':0, '!tor zodiac':0, '!hello':0, '!tor styles':0, '!tor randchar':0, '!roll':0,
                          '!help':0, '!mm':0, '!randmonster':0, '!feat':0, '!randfeat':0, '!start init':0, '!add init':0, '!spell':0}

        self.userSet = set()

        return super().__init__()
            
    async def displayStats(self):
        retStr = f'''**Lifetime Stats**
   > !help: {self.statsDict['!help']}
   > !hello: {self.statsDict['!hello']}
   > !start init: {self.statsDict['!start init']}
   > !add init: {self.statsDict['!add init']}
   > !roll: {self.statsDict['!roll']}

   *D&D 5E Specific Commands:*
   > !feat: {self.statsDict['!feat']}
   > !mm: {self.statsDict['!mm']}   
   > !randfeat: {self.statsDict['!randfeat']}
   > !randmonster: {self.statsDict['!randmonster']}
   > !spell: {self.statsDict['!spell']}

   *Book of Tor Specific Commands:*
   > !tor horo: {self.statsDict['!tor horo']}
   > !tor randchar: {self.statsDict['!tor randchar']}
   > !tor styles: {self.statsDict['!tor styles']}
   > !tor zodiac: {self.statsDict['!tor zodiac']}
   '''
        return retStr

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
    
    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content.lower().startswith('!tor horo'):
            self.statsDict['!tor horo'] += 1
            await message.channel.send(f"<@{message.author.id}>" + "\n" + await self.bt.horo())

        if message.content.lower().startswith('!tor zodiac'):
            self.statsDict['!tor zodiac'] += 1
            await message.channel.send(f"<@{message.author.id}>" + "\n" + await self.bt.zodiac())

        if message.content.lower().startswith('!hello'):
            self.statsDict['!hello'] += 1
            embed = discord.Embed()
            embed.set_image(url='https://cdn.discordapp.com/attachments/352281669992185866/500780935638155264/kOXnswR.gif')

            await message.channel.send(embed=embed)

        if message.content.lower().startswith('!tor styles'):
            self.statsDict['!tor styles'] += 1
            await message.channel.send(f"<@{message.author.id}>" + "\n" + await self.bt.styles())

        if message.content.lower().startswith('!tor randchar'):    
            self.statsDict['!tor randchar'] += 1
            await message.channel.send(f"<@{message.author.id}>" + "\n" + await self.bt.ranchar())

        if message.content.lower().startswith('!roll'):
            self.statsDict['!roll'] += 1          
            await message.channel.send(f"<@{message.author.id}>" + "\n" + await self.dr.parse(message.content))

        if message.content.lower().startswith('!help'):
            self.statsDict['!help'] += 1
            await message.channel.send('''Hello! My name is Feyre.

**Commands:**
   > !help: Displays all commands.
   > !hello: Hi!  
   > !start init: Starts initiative tracker in channel
   > !add init (name) (roll): Adds player to initiative tracker. If left blank uses discord username and rolls 1d20.
        Ex: !add init Feyre 20
   > !roll #dSize: Rolls any number and types and dice. Supports complicated expressions
        Ex: !roll 1d20 + (5 - 1)/2 + 1d6
   > !spell name: Search D&D 5E SRD for a spell. Ex: !spell fireball
   > !stats: Displays number of times each command has been used in the lifetime of the bot

   *D&D 5E Specific Commands:*
   > !feat name: Search D&D 5E offical books for a feat (currently only PH). Ex: !feat Keen Mind
   > !mm name: Search the D&D 5E Monster Manual for a monster. Ex: !mm Goblin   
   > !randfeat: Gives a random feat from offical 5E books.
   > !randmonster: Gives a random monster from the D&D 5e Monster Manual.

   *Book of Tor Specific Commands:*
   > !tor horo: Gives a Torian Horoscope.
   > !tor randchar: Gives a random race and class combination from the Book of Tor.
   > !tor styles: Lists all character styles from the Book of Tor.
   > !tor zodiac: Gives a Primidia's Zodiac animal from the Book of Tor.

Please message <@112041042894655488> if you have any questions/issues.''')

        if message.content.lower().startswith('!mm'):
            self.statsDict['!mm'] += 1
            #search the monster manual
            retArr = await self.mm.search(message.content.lower())

            if(len(retArr[1]) < 2048):
                embed = discord.Embed(title = retArr[0], description = retArr[1], color=self.embedcolor)
                await message.channel.send(embed = embed)

            #discord has a 2048 character limit so this is needed to split the message into chunks
            else:
                s = retArr[1]
                mod = math.ceil(len(s) / 2048)
                parts = [s[i:i+2048] for i in range(0, len(s), 2048)]
                    
                for i in range(0, len(parts)):
                    if(i == 0):
                        embed = discord.Embed(title = retArr[0], description = parts[i], color=self.embedcolor)
                    else:
                        embed = discord.Embed(title = retArr[0] + " *- Continued*", description = parts[i], color=self.embedcolor)
                    await message.channel.send(embed = embed)    

        if message.content.lower().startswith('!randmonster'):
            self.statsDict['!randmonster'] += 1
            retArr = await self.mm.randMonster()
            if(len(retArr[1]) < 2048):
                embed = discord.Embed(title = retArr[0], description = retArr[1], color=self.embedcolor)
                await message.channel.send(embed = embed)

            #discord has a 2048 character limit so this is needed to split the message into chunks
            else:
                s = retArr[1]
                mod = math.ceil(len(s) / 2048)
                parts = [s[i:i+2048] for i in range(0, len(s), 2048)]
                    
                for i in range(0, len(parts)):
                    if(i == 0):
                        embed = discord.Embed(title = retArr[0], description = parts[i], color=self.embedcolor)
                    else:
                        embed = discord.Embed(title = retArr[0] + " *- Continued*", description = parts[i], color=self.embedcolor)
                    await message.channel.send(embed = embed)  

        if message.content.lower().startswith('!feat'):
            self.statsDict['!feat'] += 1
            retArr = await self.f.search(message.content.lower())
            if(len(retArr[1]) < 2048):
                embed = discord.Embed(title = retArr[0], description = retArr[1], color=self.embedcolor)
                await message.channel.send(embed = embed)

            #discord has a 2048 character limit so this is needed to split the message into chunks
            else:
                s = retArr[1]
                mod = math.ceil(len(s) / 2048)
                parts = [s[i:i+2048] for i in range(0, len(s), 2048)]
                    
                for i in range(0, len(parts)):
                    if(i == 0):
                        embed = discord.Embed(title = retArr[0], description = parts[i], color=discord.Color.from_rgb(87,228,249))
                    else:
                        embed = discord.Embed(title = retArr[0] + " *- Continued*", description = parts[i], color=discord.Color.from_rgb(87,228,249))
                    await message.channel.send(embed = embed)  

        if message.content.lower().startswith('!spell'):
            self.statsDict['!spell'] += 1
            retArr = await self.sb.search(message.content.lower())
            if(len(retArr[1]) < 2048):
                embed = discord.Embed(title = retArr[0], description = retArr[1], color=self.embedcolor)
                await message.channel.send(embed = embed)

            #discord has a 2048 character limit so this is needed to split the message into chunks
            else:
                s = retArr[1]
                mod = math.ceil(len(s) / 2048)
                parts = [s[i:i+2048] for i in range(0, len(s), 2048)]
                    
                for i in range(0, len(parts)):
                    if(i == 0):
                        embed = discord.Embed(title = retArr[0], description = parts[i], color=discord.Color.from_rgb(87,228,249))
                    else:
                        embed = discord.Embed(title = retArr[0] + " *- Continued*", description = parts[i], color=discord.Color.from_rgb(87,228,249))
                    await message.channel.send(embed = embed)    

        if message.content.lower().startswith('!randfeat'):
            self.statsDict['!randfeat'] += 1
            retArr = await self.f.randFeat()
            if(len(retArr[1]) < 2048):
                embed = discord.Embed(title = retArr[0], description = retArr[1], color=self.embedcolor)
                await message.channel.send(embed = embed)

            #discord has a 2048 character limit so this is needed to split the message into chunks
            else:
                s = retArr[1]
                mod = math.ceil(len(s) / 2048)
                parts = [s[i:i+2048] for i in range(0, len(s), 2048)]
                    
                for i in range(0, len(parts)):
                    if(i == 0):
                        embed = discord.Embed(title = retArr[0], description = parts[i], color=discord.Color.from_rgb(87,228,249))
                    else:
                        embed = discord.Embed(title = retArr[0] + " *- Continued*", description = parts[i], color=discord.Color.from_rgb(87,228,249))
                    await message.channel.send(embed = embed)  
            
        if message.content.lower().startswith('!start init'):
            self.statsDict['!start init'] += 1
            key = message.guild.name + ":" + message.channel.name
            i = Initiative()
            self.initDict[key] = i
            embed = discord.Embed(title = "|-------- **Initiative** --------|", description = "", color=self.embedcolor)
            msg = await message.channel.send(embed = embed)
            self.initEmbedDict[key] = msg

        if message.content.lower().startswith('!add init'):
            self.statsDict['!add init'] += 1
            key = message.guild.name + ":" + message.channel.name
            if(key in self.initDict):
                split = message.content.split(' ')
                name = ""
                init = ""

                #!add init
                if(len(split) == 2):
                    name = message.author.name
                    init = random.randint(1, 20)

                #!add init something
                if(len(split) == 3):
                    #something = int so name = author
                    if (split[2].lstrip('+-').isdigit()):
                        init = split[2]
                        name = message.author.name
                    #something = name so int = random
                    else:
                        name = split[2]
                        init = random.randint(1, 20)

                #!add init name init OR init name
                if(len(split) == 4):
                    #!add init Name Init
                    if (split[3].lstrip('+-').isdigit()):
                        init = split[3]
                        name = split[2]
                    #!add init Init Name
                    else:
                        init = split[2]
                        name = split[3]

                    
                self.initDict[key].addPlayer(name, init)
                desc = self.initDict[key].displayInit()
                newEmbed = discord.Embed(title = "|-------- **Initiative** --------|", description = self.initDict[key].displayInit(), color=self.embedcolor)

                #delete old message and send new one with updated values
                self.initEmbedDict[key] = await  self.initEmbedDict[key].delete()
                self.initEmbedDict[key] = await message.channel.send(embed = newEmbed)

            else:
                await message.channel.send(f"<@{message.author.id}>" + "\n" + "*Please start initiative with !start init before adding players*")

        if message.content.lower().startswith('!stats'):
            await message.channel.send(await self.displayStats())

        if message.content.lower().startswith('!quit'):
            if(message.author.id == 112041042894655488):
                pyDir = os.path.dirname(__file__)
                relPath = "_data//stats.txt"
                absRelPath = os.path.join(pyDir, relPath)
                with open(absRelPath, 'w') as file:
                    file.write(json.dumps(self.statsDict))


                await message.channel.send("<@112041042894655488> *Shutting down*")
                await self.close()
                sys.exit()


                
def main():
    client = MyClient()

    if(sys.argv[1] == 'test'):
        pyDir = os.path.dirname(__file__)
        file = open(os.path.join(pyDir, 'test_token.txt'), 'r')
        testToken = file.readline().strip()
        client.run(testToken)
        

    elif (sys.argv[1] == 'release'):
        pyDir = os.path.dirname(__file__)
        file = open(os.path.join(pyDir, 'release_token.txt'), 'r')
        releaseToken = file.readline().strip()
        client.run(releaseToken)


if __name__ == "__main__":
    main()
