from os import path
from json import load, dumps
from math import ceil
from discord.ext import commands
from discord.utils import get
from discord.ext.tasks import loop
from discord.ext.commands import CommandNotFound
from asteval import Interpreter
from ISStreamer.Streamer import Streamer
from datetime import datetime

from _classes.BotData import BotData

from _cogs.InitiativeTracker import InitiativeCog
from _cogs.Help import Helper
from _cogs.SimpleDiceRoll import SimpleDiceRoller
from _cogs.CharacterSelection import CharacterSelector
from _cogs.Bank import Banker
from _cogs.DeckOfManyThings import DeckOfManyThings
from _cogs.DiceRolls import DiceRoller
from _cogs.CurrencyConversion import CurrencyConverter
from _cogs.Administrator import Administrator
from _cogs.ClassAbilities import ClassAbilityLookupCog
from _cogs.Feat import FeatLookupCog

import discord
import asyncio
import sys
import random
import os
import copy
import time
import textwrap

#region Helper Functions
async def get_pre(bot, message):
    if(message.guild == None):
        return '!'

    pre = data.prefixDict.get(str(message.guild.id), '!')
    return pre

async def createAndSendEmbeds(ctx, returnedArray):
    if(len(returnedArray[1]) < 2048):
        embed = discord.Embed(title = returnedArray[0], description = returnedArray[1])#, color=data.embedcolor)
        await ctx.send(embed = embed)

    #discord has a 2048 character limit so this is needed to split the message into chunks
    else:
        s = returnedArray[1]
        parts = [s[i:i+2048] for i in range(0, len(s), 2048)]
                    
        for i in range(0, len(parts)):
            if(i == 0):
                embed = discord.Embed(title = returnedArray[0], description = parts[i])#, color=data.embedcolor)
            else:
                embed = discord.Embed(title = returnedArray[0] + " *- Continued*", description = parts[i])#, color=data.embedcolor)
            await ctx.send(embed = embed)
    
async def codify(string, title = None):
    if title:
        s = f'''```md
# {title}

{string}```'''
    
    else:
        s = '```' + string + '```'
    return s
#endregion

#Initalize the bot:

data = BotData()
aeval = Interpreter()

bot = commands.Bot(command_prefix = get_pre)
bot.remove_command('help')

# Add Cogs
bot.add_cog(InitiativeCog(bot, data)) # Initiative
bot.add_cog(Helper(bot, data)) # Help
bot.add_cog(SimpleDiceRoller(bot, data)) # Simple Dice: dp, d20, d12, etc...
bot.add_cog(CharacterSelector(bot, data)) # Character Selection
bot.add_cog(Banker(bot, data)) # Bank
bot.add_cog(DeckOfManyThings(bot, data)) # Deck of Many Things
bot.add_cog(DiceRoller(bot, data)) # Dice Rolling
bot.add_cog(CurrencyConverter(bot, data)) # Currency Converstion
bot.add_cog(Administrator(bot, data)) # Adminstrator Commands
bot.add_cog(ClassAbilityLookupCog(bot, data)) # Ability Lookup
bot.add_cog(FeatLookupCog(bot, data))

#COMMANDS:

#region Hello
@bot.command()
async def hello(ctx):
    """
    Hi!
    """
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)

    #raise Exception

    data.statsDict['!hello'] += 1
    embed = discord.Embed()
    #https://cdn.discordapp.com/attachments/352281669992185866/500780935638155264/kOXnswR.gif
    embed.set_image(url='https://cdn.discordapp.com/attachments/401837411291627524/538476988357148675/hello.gif')
    await ctx.send(embed=embed)
#endregion

@bot.command()
async def ping(ctx):
    await ctx.send('`Pong! {0}ms`'.format(round(bot.latency, 3)))

#region Monster Manual
@bot.command()
async def mm(ctx, *, args = None):
    """
    Searches the Monster Manual for a monster
    """
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!mm'] += 1

    if not args:
        await ctx.send('''```Missing command arguments, see !help mm for more information.\nEx: !mm Tarrasque```''')
        return

    mmArr = await data.monsterManual.search(args)
    if (mmArr == False):
        await ctx.send("```I'm sorry. I wasn't able to find the monster you are looking for.```")
    else:
        await createAndSendEmbeds(ctx, mmArr)
     
@bot.command()
async def randmonster(ctx):
    """
    Gives a random monster from the Monster Manual
    """
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!randmonster'] += 1
    mmArr = await data.monsterManual.randMonster()
    await createAndSendEmbeds(ctx, mmArr)
#endregion

#region Items
@bot.command()
async def item(ctx, *, args = None):
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!item'] += 1

    if not args:
        await ctx.send('''```Missing the search argument! See !help item for more info.```''')
        return

    item = await data.item_lookup.search(args)

    if len(item) >= 1997 and len(item) < 3997:
        item1 = item[0:1990] + '```'
        item2 = '```diff\n' + item[1991:]
        await ctx.send(item1)
        await ctx.send(item2)

    elif len(item) >= 3997 and len(item) < 5980:
        item1 = item[0:1990] + '```'
        item2 = '```diff\n' + item[1990:3979] + '```'
        item3 = '```diff\n' + item[3979:]
        await ctx.send(item1)
        await ctx.send(item2)
        await ctx.send(item3)

    elif len(item) >= 5980:
        item1 = item[0:1990] + '```'
        item2 = '```diff\n' + item[1990:3979] + '```'
        item3 = '```diff\n' + item[3979:5979] + '```'
        item4 = '```diff\n' + item[5979:]
        await ctx.send(item1)
        await ctx.send(item2)
        await ctx.send(item3)
        await ctx.send(item4)
    
    else:
        await ctx.send(item)
#endregion

#region Conditions
@bot.command()
async def condition(ctx, *, args = None):
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!condition'] += 1

    if not args:
        await ctx.send('''```asciidoc
[Conditions]

- Blinded
- Charmed
- Deafened
- Fatigued
- Exhaustion
- Frightened
- Grappled
- Incapacitated
- Invisible
- Paralyzed
- Petrified
- Poisoned
- Prone
- Restrained
- Stunned 
- Unconscious

Try !condition [condition] for more info!
Ex: !condition Prone
```''')
        return


    condition = await data.condition_lookup.search(args)
    await ctx.send(condition)
#endregion

#region ClassFeatures
@bot.command()
async def c(ctx, *, args = None):
    """
    Searches the Player's Handbook for a spell
    """
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!c'] += 1

    if not args:
        await ctx.send('''```Missing command arguments, see !help class for more information.\nEx: !c Wizard```''')
        return

    classArr = await data.class_features.search(args)

    if (classArr == False):
        await ctx.send("```I'm sorry. I wasn't able to find the class you are looking for.```")
    else:
        await createAndSendEmbeds(ctx, classArr)
#endregion

#region Spell
@bot.command()
async def spell(ctx, *, args = None):
    """
    Searches the Player's Handbook for a spell
    """
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!spell'] += 1

    if not args:
        await ctx.send('''```Missing command arguments, see !help spell for more information.\nEx: !spell Wish```''')
        return

    spellArr = await data.spellBook.search(args)

    if (spellArr == False):
        await ctx.send("```I'm sorry. I wasn't able to find the spell you are looking for.```")
    else:
        await createAndSendEmbeds(ctx, spellArr)
#endregion

#region Voting
@bot.command()
async def vote(ctx,  *, args = None):
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!vote'] += 1

    embed = discord.Embed(description="If you have a moment, please [vote](https://top.gg/bot/500733845856059402) for Feyre on top.gg! This helps more people find the bot. Thanks :)")
    embed.set_image(url='https://media.giphy.com/media/zGnnFpOB1OjMQ/giphy.gif')
    await ctx.send(embed = embed)
#endregion

#region Weapon

async def weapon_helper(ctx, args):
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!weapon'] += 1

    if not args:
        await ctx.send('''```Missing command arguments, see !help weapon for more information.\nEx: !w Longsword```''')
        return

    wep = await data.weapons.search(args)
    if wep == False:
        await ctx.send("```Sorry, I couldn't find that weapon.```")
    else:
        await ctx.send(await wep.to_string())

@bot.command()
async def weapon(ctx, *, args = None):
    await weapon_helper(ctx, args)

@bot.command()
async def w(ctx, *, args = None):
    await weapon_helper(ctx, args)

#endregion

#region Tor    
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
#endregion

#region Stats
@bot.command()
async def stats(ctx, *, args = None):
    """
    Shows the lifetime stats of the bot

    """
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)

    if args != None:
        args = args.lower().strip()
    
    await ctx.send(await data.stats_handler.get_stats(args, data.statsDict, len(data.userSet), len(bot.guilds)))
#endregion

#region Developer
@bot.command()
async def request(ctx, *, args = None):
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!request'] += 1

    if (args == None):
        await ctx.send("```!request requires arguments! Try !request [feature]```")
        return
    else:
        User = bot.get_user(112041042894655488)

        requestStr = f"**Feature Request**\nFrom: {ctx.author}\n\n{args}"
        await User.send(requestStr)
        await ctx.send("```Thank you for submitting a request! Your request has been forwarded to the developer, kittysaurus.\n\nYou can also visit the support server and chat with the developer directly by using the !support command.```")

async def save_to_disk():
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




@bot.command()
async def quit(ctx):
    if(ctx.author.id == 112041042894655488):
        print("Saving to disk...")
        await save_to_disk()
        User = bot.get_user(112041042894655488)
        requestStr = "Shutting down..."
        await User.send(requestStr)
        sys.exit()

@bot.command()
async def change_presence(ctx, *, args):
    if(ctx.author.id == 112041042894655488):
        await ctx.send("Changing presence to: " + args)
        await bot.change_presence(activity = discord.Game(name=args))

#endregion

#region New
@bot.command()
async def new(ctx):
    """
    Whats new with the bot?

    """
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!new'] += 1

    updateString = '''```asciidoc
[Updates - see !help for more information]
= Rewrote Initiative tracking (!init) = 
    - Added emoji for adding a character to initiative
    - Added emoji for removing a character from initiative
    - Added support for characters with spaces in their names
    - Added support for more complicated dice expressions using the -i argument

= Added persistent character storage (!character)=
    - Users can now register up to 9 characters
    - When using the initiative tracker users can add their active character using emojis
    - Users can change their active character using emojis

    > This functionality will eventually be merged with the bank

= Added ability lookup (!ability)= 
    - Users can search for class abilities such as Rogue's Vanish

= Added dice reroll emoji (!roll)= 
    - Users can now reroll a dice using the reroll emoji. They no longer need to retype the command.

= Added a ping command (!ping) = 
    - !ping can be used to check bot latency

= Bank Command now shows abbreviated version of character accounts =

[Bugs]
> Fixed typos
> Fixed initiative tracker
> Moved most major functionality into cogs

Please report bugs using the !request command```'''
    await ctx.send(updateString)
#endregion
    
#region Usage Statistics
@bot.command()
async def start_stream(ctx):
    if(ctx.author.id == 112041042894655488):
        await ctx.send("`Starting stream to Initial State`")
        send_data.start()

@bot.command()
async def stop_stream(ctx):
    if(ctx.author.id == 112041042894655488):
        await ctx.send("`Stopping stream to Initial State`")
        send_data.stop()

@loop(seconds=300)
async def send_data():
    # print("Constructing stream data...")
    stream_data = copy.deepcopy(data.statsDict)
    stream_data['user_count'] = len(data.userSet)
    stream_data['server_count'] = len(bot.guilds)
    stream_data['total_command_count'] = sum(data.statsDict.values())

    # print("Streaming data to intial state...")
    streamer = Streamer(bucket_name="Feyre", bucket_key=bucket_key, access_key=access_key, buffer_size=200)
    streamer.log_object(stream_data)

    streamer.flush()
    streamer.close()
    # print("Done!")
#endregion

@loop(hours=12)
async def save_data():
    print("Saving data to disk...")
    await save_to_disk()


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        result = None
        try:
            if((ctx.invoked_with[0] == 'r' and 'd' in ctx.invoked_with)): # Treat this as some attempted dice input
                result = await bot.get_cog('DiceRoller').dice_roll.parse(ctx.invoked_with[0:], gm = False)
            elif((ctx.invoked_with[0] == 'd' or ctx.invoked_with[1] == 'd' or ctx.invoked_with[2] == 'd')): # Treat this as some attempted dice input
                result = await bot.get_cog('DiceRoller').dice_roll.parse(ctx.invoked_with[0:], gm = False)
            if(result and not result.startswith("```I'm sorry")): # this is bad but ill accept it for now
                await bot.get_cog('DiceRoller').roll(ctx, args = ctx.invoked_with[0:])
                data.statsDict['dirty_rolls'] += 1
                return
        except Exception as e:
            print("Attempted dice roll: " + ctx.invoked_with)
            print(e)
            return
    raise error

@bot.event
async def on_ready():
    print()
    print ("Starting up...")
    print ("I am running as: " + bot.user.name)
    print ("With the ID: " + str(bot.user.id))

    await bot.change_presence(activity = discord.Game(name="!help (chat or DM)"))
    if(sys.argv[2] == 'true'):
        print("Starting stream to initial state...")
        send_data.start()
    elif (sys.argv[2] == 'false'):
        print("Stream argument is set to false. Skipping stream.")
    save_data.start()
#Start the bot


#region upper/lowercase
@bot.command()
async def Hello(ctx, *, args = None):
    await hello(ctx)


@bot.command()
async def Mm(ctx, *, args = None):
    await mm(ctx, args = args)

@bot.command()
async def Randmonster(ctx, *, args = None):
    await randmonster(ctx)

@bot.command()
async def Item(ctx, *, args = None):
    await item(ctx, args = args)

@bot.command()
async def Condition(ctx, *, args = None):
    await condition(ctx, args = args)

@bot.command()
async def C(ctx, *, args = None):
    await c(ctx, args = args)

@bot.command()
async def Spell(ctx, *, args = None):
    await spell(ctx, args = args)

@bot.command()
async def Vote(ctx, *, args = None):
    await vote(ctx, args = args)

@bot.command()
async def Weapon(ctx, *, args = None):
    await weapon(ctx, args = args)

@bot.command()
async def W(ctx, *, args = None):
    await w(ctx, args = args)

@bot.command()
async def Tor(ctx, *, args = None):
    await tor(ctx, args = args)

@bot.command()
async def Stats(ctx, *, args = None):
    await stats(ctx, args = args)


@bot.command()
async def Request(ctx, *, args = None):
    await request(ctx, args = args)

@bot.command()
async def Quit(ctx, *, args = None):
    await quit(ctx)

@bot.command()
async def Change_presence(ctx, *, args = None):
    await change_presence(ctx, args = args)

@bot.command()
async def New(ctx, *, args = None):
    await new(ctx)
#endregion


global bucket_key
global access_key

if(sys.argv[1] == 'test'):
    pyDir = path.dirname(__file__)
    testToken = ""
    with open(path.join(pyDir, 'test_token.txt'), 'r') as file:
        testToken = file.readline().strip()
    with open(path.join(pyDir, 'bucket_key.txt'), 'r') as file:
        bucket_key = file.readline().strip()
    with open(path.join(pyDir, 'access_key.txt'), 'r') as file:
        access_key = file.readline().strip()
    bot.run(testToken)
    
elif (sys.argv[1] == 'release'):
    pyDir = path.dirname(__file__)
    releaseToken = ""
    with open(path.join(pyDir, 'release_token.txt'), 'r') as file:
        releaseToken = file.readline().strip()
    with open(path.join(pyDir, 'bucket_key.txt'), 'r') as file:
        bucket_key = file.readline().strip()
    with open(path.join(pyDir, 'access_key.txt'), 'r') as file:
        access_key = file.readline().strip()
    bot.run(releaseToken)