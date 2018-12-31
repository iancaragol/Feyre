from BookOfTor import BookOfTor
from Monster import MonsterManual
from Feat import Feats
from Spellbook import Sb
from DiceRolls import Roller
from Init import Initiative

from os import path
from json import load, dumps
from math import ceil
from discord.ext import commands
from datetime import datetime

import discord
import asyncio
import sys
import random


class Bot():
    """
    Main class for bot. Adds all commands to the bot and starts it with the start(token) function.

    Attributes:
        diceRoller: instance of the Roller() class
        spellBook: instance of the Sb() class
        monsterManual: instance of the MonsterManual class
        feats: instances of the Feats() class
        bookOfTor: instance of the BookOfTor() class

        initDict: dictionary mapping discord channel to Iniative()
        initEmbedDict: dictionary mapping discord channel to most recent message
        statsDict: iniatlized from text file, maps commands to ints

    TO DO:
        Bot should DM mm lookup/etc by default
        Bot should support DM's
        GM/Secret rolls
        Only admin's should be able to change the bot's prefix
        Inline dice rolls
        Fix dice roller (freezes on !roll 1000d20
    """
    def __init__(self):
        """
        Initalizes the Bot() class

        Raises:
            File read error
            JSON read error
        """
        #Main feature classes
        self.diceRoller = Roller()
        self.spellBook = Sb()
        self.monsterManual = MonsterManual()
        self.feats = Feats()
        self.bookOfTor = BookOfTor()

        #Initiative tracking dictionaries
        self.initDict = {}
        self.initEmbedDict = {}

        self.statsDict = {}
        self.prefixDict = {}

        self.embedcolor = discord.Color.from_rgb(165,87,249)

        self.userSet = set()

        try:
            pyDir = path.dirname(__file__)
            relPath = "_data//stats.txt"
            absRelPath = path.join(pyDir, relPath)
            self.statsDict = load(open(absRelPath))
            print("Stats loaded")

        except Exception:
            self.statsDict = {'!tor horo':0, '!tor zodiac':0, '!hello':0, '!tor styles':0, '!tor randchar':0, '!roll':0,
                          '!help':0, '!mm':0, '!randmonster':0, '!feat':0, '!randfeat':0, '!init':0, '!spell':0}

        try:
            pyDir = path.dirname(__file__)
            relPath = "_data//prefixes.txt"
            absRelPath = path.join(pyDir, relPath)
            self.prefixDict = load(open(absRelPath))
            print("Prefixes loaded")
            print(self.prefixDict)

        except Exception as e:
            print(f"Error loading prefixes: {e}")

        try:
            pyDir = path.dirname(__file__)
            relPath = "_data//users.txt"
            absRelPath = path.join(pyDir, relPath)
            self.userSet = set(load(open(absRelPath)))
            print("Users loaded")

        except Exception as e:
            print(f"Error loading users: {e}")

        print("\nTime: " + str(datetime.now()))

        return super().__init__()

    async def createAndSendEmbeds(self, ctx, returnedArray):
        if(len(returnedArray[1]) < 2048):
            embed = discord.Embed(title = returnedArray[0], description = returnedArray[1], color=self.embedcolor)
            await ctx.send(embed = embed)

        #discord has a 2048 character limit so this is needed to split the message into chunks
        else:
            s = returnedArray[1]
            mod = ceil(len(s) / 2048)
            parts = [s[i:i+2048] for i in range(0, len(s), 2048)]
                    
            for i in range(0, len(parts)):
                if(i == 0):
                    embed = discord.Embed(title = returnedArray[0], description = parts[i], color=self.embedcolor)
                else:
                    embed = discord.Embed(title = returnedArray[0] + " *- Continued*", description = parts[i], color=self.embedcolor)
                await ctx.send(embed = embed)
    
    async def displayStats(self):
        retStr = f'''**Lifetime Stats**
   > !help: {self.statsDict['!help']}
   > !hello: {self.statsDict['!hello']}
   > !init: {self.statsDict['!init']}
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

   **Unique users: {len(self.userSet)}**
   '''
        return retStr

    @commands.command()
    async def hello(self, ctx):
        """
        Hi!
        """
        if (ctx.author.id not in self.userSet):
            self.userSet.add(ctx.author.id)

        self.statsDict['!hello'] += 1
        embed = discord.Embed()
        embed.set_image(url='https://cdn.discordapp.com/attachments/352281669992185866/500780935638155264/kOXnswR.gif')
        await ctx.send(embed=embed)

    @commands.command()
    async def roll(self, ctx, *, args):
        """
        Rolls any number of dice in any format including skill checks
            Ex: !roll 1d20+5*6>100
        """
        if (ctx.author.id not in self.userSet):
            self.userSet.add(ctx.author.id)
        self.statsDict['!roll'] += 1
        await ctx.send(f"<@{ctx.author.id}>\n" + await self.diceRoller.parse(args))

    @commands.command()
    async def mm(self, ctx, *, args):
        """
        Searches the Monster Manual for a monster
        """
        if (ctx.author.id not in self.userSet):
            self.userSet.add(ctx.author.id)
        self.statsDict['!mm'] += 1
        mmArr = await self.monsterManual.search(args)
        await self.createAndSendEmbeds(ctx, mmArr)
     
    @commands.command()
    async def randmonster(self, ctx):
        """
        Gives a random monster from the Monster Manual
        """
        if (ctx.author.id not in self.userSet):
            self.userSet.add(ctx.author.id)
        self.statsDict['!randmonster'] += 1
        mmArr = await self.monsterManual.randMonster()
        await self.createAndSendEmbeds(ctx, mmArr)

    @commands.command()
    async def feat(self, ctx, *, args):
        """
        Searches the Player's Handbook for a feat
        """
        if (ctx.author.id not in self.userSet):
            self.userSet.add(ctx.author.id)
        self.statsDict['!feat'] += 1
        featArr = await self.feats.search(args)
        await self.createAndSendEmbeds(ctx, featArr)

    @commands.command()
    async def randfeat(self, ctx):
        """
        Gives a random feat from the Player's Handbook
        """
        if (ctx.author.id not in self.userSet):
            self.userSet.add(ctx.author.id)
        self.statsDict['!randfeat'] += 1
        featArr = await self.feats.randFeat()
        await self.createAndSendEmbeds(ctx, featArr)

    @commands.command()
    async def spell(self, ctx, *, args):
        """
        Searches the Player's Handbook for a spell
        """
        if (ctx.author.id not in self.userSet):
            self.userSet.add(ctx.author.id)
        self.statsDict['!spell'] += 1
        spellArr = await self.spellBook.search(args)
        await self.createAndSendEmbeds(ctx, spellArr)

    @commands.command()
    async def init(self, ctx, *, args = ""):
        """
        Starts or adds players to initiative
        """
        if (ctx.author.id not in self.userSet):
            self.userSet.add(ctx.author.id)
        #This command will be moved into its own class
        if (args == 'start'):
            self.statsDict['!init'] += 1
            key = ctx.guild.name + ":" + ctx.channel.name
            i = Initiative()
            self.initDict[key] = i
            embed = discord.Embed(title = "|-------- **Initiative** --------|", description = "", color=self.embedcolor)
            msg = await ctx.send(embed = embed)
            self.initEmbedDict[key] = msg
             
        else:
            argsStr = str(args)

            self.statsDict['!init'] += 1
            key = ctx.guild.name + ":" + ctx.channel.name

            if(key in self.initDict):
                split = argsStr.split(' ')
                name = ""
                init = ""

                #!init something
                if(len(split) == 1):
                    #!init
                    if(len(split[0]) == 0):
                        name = ctx.author.name
                        init = random.randint(1, 20)

                    #something = int so name = author
                    elif (split[0].lstrip('+-').isdigit()):
                        init = split[0]
                        name = ctx.author.name

                    #something = name so int = random
                    else:
                        name = split[0]
                        init = random.randint(1, 20)

                #!init name init OR init name
                if(len(split) == 2):
                    #!init Name Init
                    if (split[1].lstrip('+-').isdigit()):
                        init = split[1]
                        name = split[0]
                    #!init Init Name
                    else:
                        init = split[0]
                        name = split[1]

                    
                self.initDict[key].addPlayer(name, init)
                desc = self.initDict[key].displayInit()
                newEmbed = discord.Embed(title = "|------------- **Initiative** -------------|", description = self.initDict[key].displayInit(), color=self.embedcolor)

                #delete old message and send new one with updated values
                self.initEmbedDict[key] = await  self.initEmbedDict[key].delete()
                self.initEmbedDict[key] = await  ctx.send(embed = newEmbed)

            else:
                await ctx.send(f"<@{ctx.author.id}>" + "\n" + "Please start initiative with **!init start** before adding players")
    
    
    @commands.command()
    async def tor(self, ctx, *, args):
        if (ctx.author.id not in self.userSet):
            self.userSet.add(ctx.author.id)
        if (args == 'styles'):
            self.statsDict['!tor styles'] += 1
            await ctx.send(f"<@{ctx.author.id}>" + "\n" + await self.bookOfTor.styles())
        if (args == 'randchar'):
            self.statsDict['!tor randchar'] += 1
            await ctx.send(f"<@{ctx.author.id}>" + "\n" + await self.bookOfTor.randchar())
        if (args == 'horo'):
            self.statsDict['!tor horo'] += 1
            await ctx.send(f"<@{ctx.author.id}>" + "\n" + await self.bookOfTor.horo())
        if (args == 'zodiac'):
            self.statsDict['!tor zodiac'] += 1
            await ctx.send(f"<@{ctx.author.id}>" + "\n" + await self.bookOfTor.zodiac())

    @commands.command()
    async def stats(self, ctx):
        """
        Shows the lifetime stats of the bot

        """
        if (ctx.author.id not in self.userSet):
            self.userSet.add(ctx.author.id)
        embed = discord.Embed(description = await self.displayStats(), color=self.embedcolor)
        await ctx.send(embed = embed)
     
    @commands.command()
    async def help(self, ctx):
        if (ctx.author.id not in self.userSet):
            self.userSet.add(ctx.author.id)
        self.statsDict['!help'] += 1
        helpstr = '''Hello! My name is Feyre. You can use chat or DM's to summon me.

**Commands:**
   > **!help**: Displays all commands.
   > **!hello**: Hi!  
   > **!init start**: Starts initiative tracker in channel
   > **!init (name) (roll)**: Adds player to initiative tracker. If left blank uses discord username and rolls 1d20.
            Ex: !add init Feyre 20
   > **!roll (dice) (modifiers) (check)**: Rolls any number and types and dice. Supports complicated expressions and ability checks
            Ex: !roll 1d20 + (5 - 1)/2 + 1d6 < 25
   > **!stats**: Displays number of times each command has been used in the lifetime of the bot

   *D&D 5E Specific Commands:*
   > **!feat (name)**: Search D&D 5E offical books for a feat (currently only PH). 
            Ex: !feat Keen Mind
   > **!mm (name)**: Search the D&D 5E Monster Manual for a monster. 
            Ex: !mm Goblin
   > **!spell (name)**: Search D&D 5E SRD for a spell. 
            Ex: !spell fireball
   > **!randfeat**: Gives a random feat from offical 5E books.
   > **!randmonster**: Gives a random monster from the D&D 5e Monster Manual.

   *Book of Tor Specific Commands:*
   > **!tor horo**: Gives a Torian Horoscope.
   > **!tor randchar**: Gives a random race and class combination from the Book of Tor.
   > **!tor styles**: Lists all character styles from the Book of Tor.
   > **!tor zodiac**: Gives a Primidia's Zodiac animal from the Book of Tor.

   *Administrator Commands:*
   > **!set_prefix (prefix)**: Changes the command prefix for this server.

Please message @kittysaurus#9804 if you have any questions/issues.'''

        embed = discord.Embed(description = helpstr, color=self.embedcolor)
        await ctx.send(embed = embed)

    @commands.command()
    async def quit(self, ctx):
        """
        Cleanly shuts down the bot and re-writes the stats file
        """
        if(ctx.author.id == 112041042894655488):
                pyDir = path.dirname(__file__)
                relPath = "_data//stats.txt"
                absRelPath = path.join(pyDir, relPath)
                with open(absRelPath, 'w') as file:
                    file.write(dumps(self.statsDict))

                relPath = "_data//prefixes.txt"
                absRelPath = path.join(pyDir, relPath)
                with open(absRelPath, 'w') as file:
                    file.write(dumps(self.prefixDict))

                relPath = "_data//users.txt"
                absRelPath = path.join(pyDir, relPath)
                with open(absRelPath, 'w') as file:
                    file.write(dumps(list(self.userSet)))

                await ctx.send("<@112041042894655488> *Shutting down*")
                sys.exit()

    
    @commands.command()
    async def set_prefix(self, ctx, *, args = None):
        #TO DO:
        #Support pinging bot if you do not know the prefix
        #Removing bot from server should reset bot's prefix
        if args:
           args = args.strip()

           if(ctx.author.guild_permissions.administrator):
                possibleArgs = set(['!','~','`','#','$','%','^','&','*',',','.',';',':','>','<'])

                if(len(args) < 1):
                    await ctx.send(f"<@{ctx.author.id}>\n You must include arguments! Ex: !set_prefix &")
                    return

                elif (args not in possibleArgs):
                    await ctx.send(f"<@{ctx.author.id}>\n Prefix must be !, ~, `, #, $, %, ^, &, *, ,, ., ;, :, <, or >")
                    return

                self.prefixDict[str(ctx.message.guild.id)] = args   
                await ctx.send(f"<@{ctx.author.id}>\n Prefix for this server set to: {args.strip()}")
           else:
                 await ctx.send("Only server administrators have access to this command.")
        else:
            if(ctx.author.guild_permissions.administrator):
                await ctx.send(f"<@{ctx.author.id}>\n You must include arguments! Ex: !set_prefix &")
                return
            else:
                await ctx.send("Only server administrators have access to this command.")

    @commands.command()
    async def change_presence(self, ctx, *, args):
        if(ctx.author.id == 112041042894655488):
            await bot.change_presence(activity = discord.Game(name=args))

    async def get_pre(self, bot, message):
        pre = self.prefixDict.get(str(message.guild.id), '!')
        return pre

    def start(self, token):
        """
        Adds all of the commands and starts the bot with designated token.
        """
        #bot = commands.Bot(command_prefix = self.get_pre)
        global bot
        bot = commands.Bot(command_prefix = self.get_pre)


        bot.add_command(self.hello)
        bot.add_command(self.roll)
        bot.add_command(self.mm)
        bot.add_command(self.randmonster)
        bot.add_command(self.feat)
        bot.add_command(self.randfeat)
        bot.add_command(self.spell)
        bot.add_command(self.init)
        bot.add_command(self.tor)
        bot.add_command(self.stats)
        bot.add_command(self.quit)

        #the best way to override the default help command is to remove it
        bot.remove_command("help")
        bot.add_command(self.help)
        bot.add_command(self.change_presence)
        bot.add_command(self.set_prefix)

        #self.bot.run(token)
        bot.run(token)
        self.sBot = bot

def main():
    b = Bot()
    if(sys.argv[1] == 'test'):
        pyDir = path.dirname(__file__)
        file = open(path.join(pyDir, 'test_token.txt'), 'r')
        testToken = file.readline().strip()
        b.start(testToken)

       

    elif (sys.argv[1] == 'release'):
        pyDir = path.dirname(__file__)
        file = open(path.join(pyDir, 'release_token.txt'), 'r')
        releaseToken = file.readline().strip()
        b.start(releaseToken)
        


if __name__ == "__main__":
    main()

