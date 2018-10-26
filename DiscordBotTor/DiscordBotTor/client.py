#id 500733845856059402
#test id 505120997658329108
#token NTAwNzMzODQ1ODU2MDU5NDAy.DqPI-g.BBe4LLMfN3QFmrZXOK3mTNwSpws
#test token NTA1MTIwOTk3NjU4MzI5MTA4.DrO-Lg.jiyCbUD07MoplIKMq01kBSRbaPs
#permissions 67648
#test permissions 75776
#https://discordapp.com/oauth2/authorize?client_id=500733845856059402&scope=bot&permissions=67648
#https://discordapp.com/oauth2/authorize?client_id=505120997658329108&scope=bot&permissions=75776


import BookOfTor
import DiceRolls
import MonsterManual
import Feats
import Initiative

import discord
import asyncio
import time
import math
import re
import random

from discord.voice_client import VoiceClient

class MyClient(discord.Client):
    def __init__(self):
        self.initDict = {}
        self.initEmbedDict = {}
        return super().__init__()
              
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
    
    async def on_message(self, message):
        #ts = time.gmtime()
        #t = time.strftime("%Y-%m-%d %H:%M:%S", ts)
        #print(f"Received command: {message.content.lower()} from {message.author} at {t}")   

        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content.lower().startswith('!tor horo'):
            await message.channel.send(f"<@{message.author.id}>" + "\n" + await bt.horo())

        if message.content.lower().startswith('!tor zodiac'):
            await message.channel.send(f"<@{message.author.id}>" + "\n" + await bt.zodiac())

        if message.content.lower().startswith('!hello'):
            embed = discord.Embed()
            embed.set_image(url='https://cdn.discordapp.com/attachments/352281669992185866/500780935638155264/kOXnswR.gif')

            await message.channel.send(embed=embed)

        if message.content.lower().startswith('!tor styles'):
            await message.channel.send(f"<@{message.author.id}>" + "\n" + await bt.styles())

        if message.content.lower().startswith('!tor randchar'):         
            await message.channel.send(f"<@{message.author.id}>" + "\n" + await bt.ranchar())

        if message.content.lower().startswith('!roll'):         
            await message.channel.send(f"<@{message.author.id}>" + "\n" + await dr.parse(message.content))

        if message.content.lower().startswith('!uok'):
            await message.channel.send(f"<@{244286371181625344}>" + "\n" + "You okay?")

        if message.content.lower().startswith('!help'):
            await message.channel.send('''Hello! My name is Feyre.

**Commands:**
   > !help: Displays all commands.
   > !hello: Hi!  
   > !start init: Starts initiative tracker in channel
   > !add init (name) (roll): Adds player to initiative tracker. If left blank uses discord username and rolls 1d20.
        Ex: !add init Feyre 20
   > !roll #dSize: Rolls any number and types and dice. Supports complicated expressions
        Ex: !roll 1d20 + (5 - 1)/2 + 1d6


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
            #search the monster manual
            retArr = await mm.search(message.content.lower())

            if(len(retArr[1]) < 2048):
                embed = discord.Embed(title = retArr[0], description = retArr[1], color=embedcolor)
                await message.channel.send(embed = embed)

            #discord has a 2048 character limit so this is needed to split the message into chunks
            else:
                s = retArr[1]
                mod = math.ceil(len(s) / 2048)
                parts = [s[i:i+2048] for i in range(0, len(s), 2048)]
                    
                for i in range(0, len(parts)):
                    if(i == 0):
                        embed = discord.Embed(title = retArr[0], description = parts[i], color=embedcolor)
                    else:
                        embed = discord.Embed(title = retArr[0] + " *- Continued*", description = parts[i], color=embedcolor)
                    await message.channel.send(embed = embed)    

        if message.content.lower().startswith('!randmonster'):
            retArr = await mm.randMonster()
            if(len(retArr[1]) < 2048):
                embed = discord.Embed(title = retArr[0], description = retArr[1], color=embedcolor)
                await message.channel.send(embed = embed)

            #discord has a 2048 character limit so this is needed to split the message into chunks
            else:
                s = retArr[1]
                mod = math.ceil(len(s) / 2048)
                parts = [s[i:i+2048] for i in range(0, len(s), 2048)]
                    
                for i in range(0, len(parts)):
                    if(i == 0):
                        embed = discord.Embed(title = retArr[0], description = parts[i], color=embedcolor)
                    else:
                        embed = discord.Embed(title = retArr[0] + " *- Continued*", description = parts[i], color=embedcolor)
                    await message.channel.send(embed = embed)  

        if message.content.lower().startswith('!feat'):
            retArr = await f.search(message.content.lower())
            if(len(retArr[1]) < 2048):
                embed = discord.Embed(title = retArr[0], description = retArr[1], color=embedcolor)
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
            retArr = await f.randFeat()
            if(len(retArr[1]) < 2048):
                embed = discord.Embed(title = retArr[0], description = retArr[1], color=embedcolor)
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
            key = message.guild.name + ":" + message.channel.name
            i = Initiative.Initiative()
            self.initDict[key] = i
            embed = discord.Embed(title = "**--------Initiative--------**", description = "", color=embedcolor)
            msg = await message.channel.send(embed = embed)
            self.initEmbedDict[key] = msg

        if message.content.lower().startswith('!add init'):
            key = message.guild.name + ":" + message.channel.name
            if(key in self.initDict):
                split = message.content.split(' ')
                name = ""
                init = ""

                if(len(split) == 2):
                    name = message.author.name
                    init = random.randint(1, 20)

                if(len(split) == 3):
                    if (split[2].lstrip('+-').isdigit()):
                        init = split[2]
                        name = message.author.name
                    else:
                        name = split[2]
                        init = random.randint(1, 20)

                if(len(split) == 4):
                    if (split[3].lstrip('+-').isdigit()):
                        init = split[3]
                        name = split[2]
                    else:
                        init = split[2]
                        name = split[3]

                    
                self.initDict[key].addPlayer(name, init)
                desc = self.initDict[key].displayInit()
                newEmbed = discord.Embed(title = "**--------Initiative--------**", description = self.initDict[key].displayInit(), color=embedcolor)

                self.initEmbedDict[key] = await  self.initEmbedDict[key].delete()
                self.initEmbedDict[key] = await message.channel.send(embed = newEmbed)

            else:
                await message.channel.send(f"<@{message.author.id}>" + "\n" + "*Please start initiative with !start init before adding players*")

        if message.content.lower().startswith('!quit'):
            if(message.author.id == 112041042894655488):
                await message.channel.send("<@112041042894655488> *Shutting down*")
                await client.close()
                sys.exit()

global bt 
bt = BookOfTor.BookOfTor()

global dr
dr = DiceRolls.Roller()

global mm
mm = MonsterManual.MonsterManual()

global f
f = Feats.Feats()

embedcolor = discord.Color.from_rgb(165,87,249)
client = MyClient()
client.run("NTA1MTIwOTk3NjU4MzI5MTA4.DrO-Lg.jiyCbUD07MoplIKMq01kBSRbaPs")