from BotData import BotData

from os import path
from json import load, dumps
from math import ceil
from discord.ext import commands
from Init import Initiative


import discord
import asyncio
import sys
import random


#Helper functions:
async def get_pre(bot, message):
    if(message.guild == None):
        return '!'

    pre = data.prefixDict.get(str(message.guild.id), '!')
    return pre

async def createAndSendEmbeds(ctx, returnedArray):
    if(len(returnedArray[1]) < 2048):
        embed = discord.Embed(title = returnedArray[0], description = returnedArray[1], color=data.embedcolor)
        await ctx.send(embed = embed)

    #discord has a 2048 character limit so this is needed to split the message into chunks
    else:
        s = returnedArray[1]
        mod = ceil(len(s) / 2048)
        parts = [s[i:i+2048] for i in range(0, len(s), 2048)]
                    
        for i in range(0, len(parts)):
            if(i == 0):
                embed = discord.Embed(title = returnedArray[0], description = parts[i], color=data.embedcolor)
            else:
                embed = discord.Embed(title = returnedArray[0] + " *- Continued*", description = parts[i], color=data.embedcolor)
            await ctx.send(embed = embed)
    


#Initalize the bot:

data = BotData()
bot = commands.Bot(command_prefix = get_pre)
bot.remove_command('help')

#COMMANDS:

@bot.command()
async def hello(ctx):
    """
    Hi!
    """
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)

    data.statsDict['!hello'] += 1
    embed = discord.Embed()
    embed.set_image(url='https://cdn.discordapp.com/attachments/352281669992185866/500780935638155264/kOXnswR.gif')
    await ctx.send(embed=embed)

@bot.command()
async def roll(ctx, *, args):
    """
    Rolls any number of dice in any format including skill checks
        Ex: !roll 1d20+5*6>100
    """
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!roll'] += 1
    await ctx.send(await data.diceRoller.parse(args, gm = False))

@bot.command()
async def mm(dctx, *, args):
    """
    Searches the Monster Manual for a monster
    """
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!mm'] += 1
    mmArr = await data.monsterManual.search(args)
    if (mmArr == False):
        await ctx.send("```I'm sorry. I wasn't able to find the monster you are looking for.```")
    else:
        await data.createAndSendEmbeds(ctx, mmArr)
     
@bot.command()
async def randmonster(ctx):
    """
    Gives a random monster from the Monster Manual
    """
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!randmonster'] += 1
    mmArr = await data.monsterManual.randMonster()
    await data.createAndSendEmbeds(ctx, mmArr)

@bot.command()
async def feat(ctx, *, args):
    """
    Searches the Player's Handbook for a feat
    """
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!feat'] += 1
    featArr = await data.feats.search(args)
    if (featArr == False):
        await ctx.send("```I'm sorry. I wasn't able to find the feat you are looking for.```")
    else:
        await data.createAndSendEmbeds(ctx, featArr)
            
@bot.command()
async def randfeat(bot, ctx):
    """
    Gives a random feat from the Player's Handbook
    """
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!randfeat'] += 1

    featArr = await data.feats.randFeat()
    await data.createAndSendEmbeds(ctx, featArr)

@bot.command()
async def spell(ctx, *, args):
    """
    Searches the Player's Handbook for a spell
    """
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!spell'] += 1

    spellArr = await data.spellBook.search(args)

    if (spellArr == False):
        await ctx.send("```I'm sorry. I wasn't able to find the spell you are looking for.```")
    else:
        await data.createAndSendEmbeds(ctx, spellArr)

@bot.command()
async def init(ctx, *, args = ""):
    """
    Starts or adds players to initiative
    """
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!init'] += 1

    #This command will be moved into its own class
    if (args == 'start'):
        key = ctx.guild.name + ":" + ctx.channel.name
        i = Initiative()
        data.initDict[key] = i
        codeBlock = '''```diff
- Initiative -```'''
        msg = await ctx.send(codeBlock)
        data.initEmbedDict[key] = msg
             
    else:
        argsStr = str(args)

        data.statsDict['!init'] += 1
        key = ctx.guild.name + ":" + ctx.channel.name

        if(key in data.initDict):
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

                    
            data.initDict[key].addPlayer(name, init)
            desc = data.initDict[key].displayInit()
            #newEmbed = discord.Embed(title = "|------------- **Initiative** -------------|", description = data.initDict[key].displayInit(), color=data.embedcolor)

            codeBlock = '''```diff
- Initiative -''' + desc + '```'

            #delete old message and send new one with updated values
            data.initEmbedDict[key] = await  data.initEmbedDict[key].delete()
            data.initEmbedDict[key] = await  ctx.send(codeBlock)

        else:
            await ctx.send('''```Please start initiative with !init start before adding players```''')
    
@bot.command()
async def tor(ctx, *, args):
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    if (args == 'styles'):
        data.statsDict['!tor styles'] += 1
        newEmbed = discord.Embed(description = await data.bookOfTor.styles(), color=data.embedcolor)

    if (args == 'randchar'):
        data.statsDict['!tor randchar'] += 1
        newEmbed = discord.Embed(description = await data.bookOfTor.randchar(), color=data.embedcolor)

    if (args == 'horo'):
        data.statsDict['!tor horo'] += 1
        newEmbed = discord.Embed(description = await data.bookOfTor.horo(), color=data.embedcolor)

    if (args == 'zodiac'):
        data.statsDict['!tor zodiac'] += 1
        newEmbed = discord.Embed(description = await data.bookOfTor.zodiac(), color=data.embedcolor)

    await ctx.send(embed=newEmbed)

@bot.command()
async def stats(ctx):
    """
    Shows the lifetime stats of the bot

    """
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    #embed = discord.Embed(description = await data.displayStats(), color=data.embedcolor)
    await ctx.send(await data.displayStats())
     
@bot.command()
async def help(ctx, *, args = None):
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!help'] += 1
    helpstr = ""

    if (args != None):
        args = args.lower().strip()

    if (args == None):
        helpstr = '''```Hello! My name is Feyre. You can use chat or DM's to summon me. 

The default prefix is !. To learn more about a command type !help [command].
Like this: !help roll

Commands:
> hello - Hi!
> init - Initiative tracking
> roll - Dice rolling
> gm - GM only dice rolling
> stats - Bot usage statistics
> feat - Feat lookup
> mm - Monster Manual lookup
> spell - Spell lookup
> tor - Book of Tor
> request - Request new features!
> admin - Change defualt command prefix

Feyre always responds in the channel or direct message from which it was summoned.
Use this link to add Feyre to your channel: [https://discordbots.org/bot/500733845856059402]```''' 

    elif (args == "init"):
        helpstr = '''```!init is a per channel based initiative tracker. 

Commands:
!init start
    > Starts a new initiative tracker in the same channel
!init
    > Adds the player to initiative with their discord username and rolls 1d20 for them
!init [player name]
    > Adds a player with [player name] to initiative and rolls 1d20 for them
!init [player name] [initiative]
    > Adds a player with [player name] and [initiative] to iniative.

Ex:
!init start
!init Legolas
!init Gandalf 1```'''
    elif (args == "roll"):
        helpstr = '''```!roll can be used to roll dice of any size with complicated expressions and built in skill checks.

Dice are represented with the standard [# of dice]d[size of dice] format.
Ex: !roll 4d6
!roll 1d6*2
!roll 1d20 + 5
!roll 1d1000 + 2d2000 * 3 / 3 - 1

Skill checks can be built into the dice expression using the < and > symbols.
Ex: !roll 1d20 > 15

You can roll with advantage or disadvantage using the -a and -d flags before the dice expression.
Ex: !roll -a 1d20
    !roll -d 1d20+5
```'''
    elif (args == "stats"):
        helpstr = '''```Feyre keeps track of the number of times each command has been used and the total user count.
```'''
    elif (args == "feat"):
        helpstr = '''```!feat can be used to lookup feats from the Player's Handbook. 

Commands:
!feat [feat name] 
    > Searches for a feat
!randfeat
    > Gives a random feat
Ex:
!feat Keen Mind```'''
    elif (args == "mm"):
        helpstr = '''```!mm can be used to lookup monsters from the Monster Manual.

Commands:
!mm [monster name]
    > Searches for a monster
!randmonster
    > Gives a random monster
Ex:
!mm Young Black Dragon
!mm Tarrasque```'''
    elif (args == "spell"):
                helpstr = '''```!spell can be used to lookup spells from the Player's Handbook.

!spell [spell name]

Ex: 
!spell Wish
!spell Cure Wounds```'''

    elif (args == "tor"):
                helpstr = '''```!tor can be used to find character styles, horoscope, race/class combinations, and zodiac from the Book of Tor.

Commands:
!tor styles
    > Displays character styles
!tor horo
    > Gives a Torian horoscope
!tor zodiac
    > Gives a Torian zodiac
!tor randchar
    > Gives a random Torian race/class combination.```'''

    elif (args == "admin"):
                helpstr = '''```!admin is for server administrators. Currently the only command available to adminstrators is !set_prefix.

Commands:
!set_prefix [prefix]
    > Sets the server wide prefix to [prefix]. Prefix must be !, ~, `, #, $, %, ^, &, *, ,, ., ;, :, <, or >
Note: If you forget the bot's prefix you will no longer be able to summon it and reset it's prefix (as of now).```'''

    elif (args == "request"):
        helpstr = '''```Please help improve the bot by requesting features you would like to see!

!request [feature]```'''

    elif (args == "hello"):
                helpstr = '''```Hi?```'''

    elif (args == "gm"):
                helpstr = '''```!gm can be used to send dice rolls to the GM without other players being able to see the result.
GM's are set on a per channel basis.
                
Commands:
!gm
    > Sets the channels GM to the user
!gm roll [expression]
    > Rolls dice and sends the result to the user and the GM

Ex:
!gm
!gm roll 1d20```'''

    else:
        helpstr = '''```I could not find that command. Try !help for a list of commands.```'''

    await ctx.send(helpstr)

@bot.command()
async def request(ctx, *, args = None):
    #TODO: Finish implementing the request command
    if (args == None):
        await ctx.send("```!request requires arguments! Try !request [feature]```")
    else:
        User = bot.get_user(112041042894655488)

        requestStr = f"**Feature Request**\nFrom: {ctx.author}\n\n{args}"
        await User.send(requestStr)

@bot.command()
async def admin(ctx):
    retstr = '''```!admin is for server administrators. Currently the only command available to adminstrators is !set_prefix.

Commands:
!set_prefix [prefix]
    > Sets the server wide prefix to [prefix]. Prefix must be !, ~, `, #, $, %, ^, &, *, ,, ., ;, :, <, or >
Note: If you forget the bot's prefix you will no longer be able to summon it and reset it's prefix (as of now).```'''

    await ctx.send(retstr)

@bot.command()
async def quit(ctx):
    if(ctx.author.id == 112041042894655488):
        pyDir = path.dirname(__file__)
        relPath = "_data//stats.txt"
        absRelPath = path.join(pyDir, relPath)
        with open(absRelPath, 'w') as file:
            file.write(dumps(data.statsDict))

        relPath = "_data//prefixes.txt"
        absRelPath = path.join(pyDir, relPath)
        with open(absRelPath, 'w') as file:
            file.write(dumps(data.prefixDict))

        relPath = "_data//users.txt"
        absRelPath = path.join(pyDir, relPath)
        with open(absRelPath, 'w') as file:
            file.write(dumps(list(data.userSet)))

        pyDir = path.dirname(__file__)
        relPath = "_data//gms.txt"
        absRelPath = path.join(pyDir, relPath)
        with open(absRelPath, 'w') as file:
            file.write(dumps(data.gmDict))

        User = bot.get_user(112041042894655488)

        requestStr = "Shutting down..."
        await User.send(requestStr)
        sys.exit()

@bot.command()
async def set_prefix(ctx, *, args = None):
    #TO DO:
    #Support pinging bot if you do not know the prefix
    #Removing bot from server should reset bot's prefix
    if(not hasattr(ctx.author, 'ctx.author.guild_permissions')):
        await ctx.send(f"This command is for server use only.")

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

            data.prefixDict[str(ctx.message.guild.id)] = args   
            await ctx.send(f"<@{ctx.author.id}>\n Prefix for this server set to: {args.strip()}")
        else:
                await ctx.send("Only server administrators have access to this command.")
    else:
        if(ctx.author.guild_permissions.administrator):
            await ctx.send(f"<@{ctx.author.id}>\n You must include arguments! Ex: !set_prefix &")
            return
        else:
            await ctx.send("Only server administrators have access to this command.")

@bot.command()
async def change_presence(ctx, *, args):
    if(ctx.author.id == 112041042894655488):
        await bot.change_presence(activity = discord.Game(name=args))

@bot.command()
async def gm(ctx, *, args = None):
    #TODO: Fix this command, codeblocks do not disply color correctly.
    if (ctx.guild == None):
        await ctx.send("```GM rolls must be done in a channel with a dedicated gm.```")
        return

    elif (args == None):
        data.gmDict[ctx.channel.id] = ctx.author.id
        await ctx.send(f"```{ctx.author} was made GM of this channel.```")

    elif (args != None):
        args = args.strip()
        if (args.startswith('roll')):
            try:
                expression = args.replace('roll', '').strip()
                result = await data.diceRoller.parse(expression, gm = True)
                #TODO: Fix this spaget
                result = result.replace('```', '')
                result = result.replace('diff', '')

                gmUser = bot.get_user(data.gmDict[ctx.channel.id])
                gmResult = f'''```asciidoc
Roll from = {ctx.author.name} =
{result} ```'''

                await gmUser.send(gmResult)

                userResult = f'''```asciidoc
Roll to = {ctx.author.name} =
{result} ```'''
                sendUser = bot.get_user(ctx.author.id)
                await sendUser.send(userResult)
            except:
                await ctx.send("```This channel does not have a dedicated GM. Type !gm to set yourself as GM.```")

#EVENTS:


@bot.event
async def on_ready():
    print()
    print ("Starting up...")
    print ("I am running as: " + bot.user.name)
    print ("With the ID: " + str(bot.user.id))

    await bot.change_presence(activity = discord.Game(name="!help (chat or DM)"))
#Start the bot
if(sys.argv[1] == 'test'):
    pyDir = path.dirname(__file__)
    file = open(path.join(pyDir, 'test_token.txt'), 'r')
    testToken = file.readline().strip()
    bot.run(testToken)
    
elif (sys.argv[1] == 'release'):
    pyDir = path.dirname(__file__)
    file = open(path.join(pyDir, 'release_token.txt'), 'r')
    releaseToken = file.readline().strip()
    bot.run(releaseToken)


