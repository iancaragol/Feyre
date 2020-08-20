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
from _classes.Init import Initiative

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
bot = commands.Bot(command_prefix = get_pre)
bot.remove_command('help')
aeval = Interpreter()


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

#region Dice Rolls
@bot.command()
async def gm(ctx, *, args = None):
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!gm'] += 1

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

                gmUser = bot.get_user(data.gmDict[ctx.channel.id])
                gmResult = f'''```diff
Roll from [{ctx.author.name}]
{result} ```'''

                await gmUser.send(gmResult)

                userResult = f'''```diff
{result}```'''
                sendUser = bot.get_user(ctx.author.id)
                await sendUser.send(userResult)
            except:
                await ctx.send("```This channel does not have a dedicated GM. Type !gm to set yourself as GM.```")

@bot.command()
async def roll(ctx, *, args = None):
    """
    Rolls any number of dice in any format including skill checks
        Ex: !roll 1d20+5*6>100
    """
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!roll'] += 1

    if not args:
        await ctx.send('''```Missing command arguments, see !help roll for more information.\nEx: !roll 1d20+5```''')
        return

    roll_msg = await data.diceRoller.parse(args, gm = False)
    msg = await ctx.send(roll_msg)

    # Add emoji to roll
    arrows = '🔁'
    await msg.add_reaction(arrows)
    await reroll_helper(ctx, args, roll_msg, msg)
    

async def reroll_helper(ctx, args, roll_msg, msg):
    try:
        reaction, u = await bot.wait_for('reaction_add', check=lambda r, u:str(r.emoji) == '🔁' and u.id != bot.user.id and r.message.id == msg.id, timeout=21600) # Times out after 6 hours

        if reaction != None:
            print("Rerolling")
            roll_msg = await data.diceRoller.parse(args, gm = False)
            if ctx.channel.type is discord.ChannelType.private:
                await msg.delete()
                msg = await ctx.send(roll_msg)
                await msg.add_reaction('🔁')
            else:
                await msg.edit(content=roll_msg)
                await reaction.remove(u)
            await reroll_helper(ctx, args, roll_msg, msg)
    
    except asyncio.exceptions.TimeoutError as e:
        await msg.clear_reaction('🔁')
        

@bot.command()
async def r(ctx, *, args = None):
    """
    Rolls any number of dice in any format including skill checks
        Ex: !roll 1d20+5*6>100
    """

    await roll(ctx, args = args)
#endregion

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

#region Feats
@bot.command()
async def feat(ctx, *, args = None):
    """
    Searches the Player's Handbook for a feat
    """
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!feat'] += 1

    if not args:
        await ctx.send('''```Missing command arguments, see !help feat for more information.\nEx: !feat Lucky```''')
        return

    featArr = await data.feats.search(args)
    if (featArr == False):
        await ctx.send("```I'm sorry. I wasn't able to find the feat you are looking for.```")
    else:
        await createAndSendEmbeds(ctx, featArr)
            
@bot.command()
async def randfeat(ctx):
    """
    Gives a random feat from the Player's Handbook
    """
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!randfeat'] += 1

    featArr = await data.feats.randFeat()
    await createAndSendEmbeds(ctx, featArr)
#endregion

#region Shorthand dice rolls



@bot.command()
async def dp(ctx, *, args = None):
    data.statsDict['!roll'] += 1

    try:
        roll = str(random.randint(1, 100))
        if(args):
            total = aeval(roll + args.strip())
            msg = f'''```css\n{roll}{args.replace(' ', '')} = [{"%.2g" % total}%]```'''

        else:
            total = roll
            msg = f'''```asciidoc
[{total}%]```'''

    except:
        msg = f'''```I didn't understand something about your input. Try !roll for more complicated expressions.```'''

    await ctx.send(msg)

@bot.command()
async def d20(ctx, *, args = None):
    data.statsDict['!roll'] += 1

    try:
        roll = str(random.randint(1, 20))
        if(args):
            total = aeval(roll + args.strip())
            msg = f'''```css\n{roll}{args.replace(' ', '')} = [{"%.2g" % total}]```'''

        else:
            total = roll
            msg = f'''```asciidoc
[{total}]```'''

    except:
        msg = f'''```I didn't understand something about your input. Try !roll for more complicated expressions.```'''

    await ctx.send(msg)

@bot.command()
async def d12(ctx, *, args = None):
    data.statsDict['!roll'] += 1

    try:
        roll = str(random.randint(1, 12))
        if(args):
            total = aeval(roll + args.strip())
            msg = f'''```css\n{roll}{args.replace(' ', '')} = [{"%.2g" % total}]```'''

        else:
            total = roll
            msg = f'''```asciidoc
[{total}]```'''

    except:
        msg = f'''```I didn't understand something about your input. Try !roll for more complicated expressions.```'''

    await ctx.send(msg)

@bot.command()
async def d10(ctx, *, args = None):
    data.statsDict['!roll'] += 1

    try:
        roll = str(random.randint(1, 10))
        if(args):
            total = aeval(roll + args.strip())
            msg = f'''```css\n{roll}{args.replace(' ', '')} = [{"%.2g" % total}]```'''

        else:
            total = roll
            msg = f'''```asciidoc
[{total}]```'''

    except:
        msg = f'''```I didn't understand something about your input. Try !roll for more complicated expressions.```'''

    await ctx.send(msg)

@bot.command()
async def d8(ctx, *, args = None):
    data.statsDict['!roll'] += 1

    try:
        roll = str(random.randint(1, 8))
        if(args):
            total = aeval(roll + args.strip())
            msg = f'''```css\n{roll}{args.replace(' ', '')} = [{"%.2g" % total}]```'''

        else:
            total = roll
            msg = f'''```asciidoc
[{total}]```'''

    except:
        msg = f'''```I didn't understand something about your input. Try !roll for more complicated expressions.```'''

    await ctx.send(msg)

@bot.command()
async def d6(ctx, *, args = None):
    data.statsDict['!roll'] += 1

    try:
        roll = str(random.randint(1, 6))
        if(args):
            total = aeval(roll + args.strip())
            msg = f'''```css\n{roll}{args.replace(' ', '')} = [{"%.2g" % total}]```'''

        else:
            total = roll
            msg = f'''```asciidoc
[{total}]```'''

    except:
        msg = f'''```I didn't understand something about your input. Try !roll for more complicated expressions.```'''

    await ctx.send(msg)

@bot.command()
async def d4(ctx, *, args = None):
    data.statsDict['!roll'] += 1

    try:
        roll = str(random.randint(1, 4))
        if(args):
            total = aeval(roll + args.strip())
            msg = f'''```css\n{roll}{args.replace(' ', '')} = [{"%.2g" % total}]```'''

        else:
            total = roll
            msg = f'''```asciidoc
[{total}]```'''

    except:
        msg = f'''```I didn't understand something about your input. Try !roll for more complicated expressions.```'''

    await ctx.send(msg)

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

#region Currency

async def currency_helper(ctx, args):
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!currency'] += 1

    if not args:
        await ctx.send('''```Missing command arguments, see !help currency for more information.\nEx: !currency 10gp 55ep 5sp```''')
        return
    await ctx.send(await data.currency_converter.parse_input(args))

@bot.command()
async def currency(ctx, *, args = None):
    await currency_helper(ctx, args)

@bot.command()
async def cur(ctx, *, args = None):
    await currency_helper(ctx, args)

@bot.command()
async def convert(ctx, *, args = None):
    await currency_helper(ctx, args)

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

#region DeckOfMany

async def deck_of_many_helper(ctx, args):
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!dom'] += 1

    if (args == None):
        card, effect = await data.deck_of_many.draw(data.deck_of_many.default_deck)
        await ctx.send(await data.deck_of_many.card_to_string(card, effect))

    if (len(ctx.args) == 1 and args == '-i'):
        card, effect = await data.deck_of_many.draw(data.deck_of_many.default_deck)
        embed = discord.Embed()
        embed.set_image(url=await data.deck_of_many.get_image(card))
        await ctx.send(embed=embed)
        await ctx.send(await data.deck_of_many.card_to_string(card, effect))


@bot.command()
async def dom(ctx, *, args = None):
    await deck_of_many_helper(ctx, args)

#endregion

#region Initiative

@bot.event
async def on_raw_reaction_add(payload):
    init_key = str(payload.guild_id) + ":" + str(payload.channel_id)
    if(init_key in data.initDict.keys()):
        channel = bot.get_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)

        init = data.initDict[init_key]

        reaction = get(msg.reactions, emoji=payload.emoji.name)
        if reaction and reaction.count > 1:
            #init.round_count += 1
            init.marker_count += 1
            await update_init(init_key)
    

async def update_init(key):
    desc = data.initDict[key].displayInit()
    codeBlock = '''```asciidoc
= Initiative =
[Round: {}]'''.format(data.initDict[key].round_count) + desc + '```'

    #delete old message and send new one with updated values
    old_msg = data.initEmbedDict[key]
    data.initEmbedDict[key] = await  data.initEmbedDict[key].delete()
    data.initEmbedDict[key] = await  old_msg.channel.send(codeBlock)

    cross = '\N{CROSSED SWORDS}'
    await data.initEmbedDict[key].add_reaction(cross)

async def init_helper(ctx, args):
    """
    Starts or adds players to initiative
    """
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!init'] += 1

    if (not ctx.guild):
        await ctx.send("""```The initative tracker can only be used in a guild channel at this time. It is not supported when direct messaging Feyre. See !help init for more info.```""")
        return 

    #This command will be moved into its own class
    if (args == 'start'):
        key = str(ctx.guild.id) + ":" + str(ctx.channel.id)
        i = Initiative()
        data.initDict[key] = i
        codeBlock = '''```asciidoc
= Initiative = 
[Round: {}]```'''.format(i.round_count)
        msg = await ctx.send(codeBlock)
        cross = '\N{CROSSED SWORDS}'
        await msg.add_reaction(cross)
        data.initEmbedDict[key] = msg

    elif (args.strip().startswith('reset')):
        argsStr = str(args)
        key = str(ctx.guild.id) + ":" + str(ctx.channel.id)

        if(key in data.initDict):
            name = argsStr.strip()
            mark = data.initDict[key].changeMarker(0)
            ret = data.initDict[key].changeRound(0)

            if(ret):
                await update_init(key)

    elif (args.strip().startswith('round')):
        argsStr = str(args)
        argsStr = argsStr.replace('round', '').strip()
        key = str(ctx.guild.id) + ":" + str(ctx.channel.id)

        if(key in data.initDict):
            name = argsStr.strip()
            try:
                ret = data.initDict[key].changeRound(int(argsStr))
            except:
                 await ctx.send('''```Something went wrong! Make sure the new round is a number. See !help init for more info.```''')
            if(ret):
                await update_init(key)


    elif (args.strip().startswith('remove') or args.strip().startswith('-r')):
        argsStr = str(args)
        argsStr = argsStr.replace('remove', '').strip()
        argsStr = argsStr.replace('-r', '').strip()

        key = str(ctx.guild.id) + ":" + str(ctx.channel.id)

        if(key in data.initDict):
            name = argsStr.strip()
            ret = data.initDict[key].removePlayer(name)

            if(ret):
                await update_init(key)

            elif(not ret):
                await ctx.send('''```I couldnt find the player you were looking for.```''')

             
    else:
        argsStr = str(args)

        data.statsDict['!init'] += 1
        key = str(ctx.guild.id) + ":" + str(ctx.channel.id)

       
        if(key in data.initDict):
            split = argsStr.split(' ')
            name = ""
            init = ""
        #mod = ""        
            if len(split) == 2:
                try:
                    #name mod
                    name = split[0]
                    if split[1].startswith("+") or split[1].startswith("-") or split[1].startswith("/") or split[1].startswith("*"):
                        roll = random.randint(1, 20)
                        init = aeval(str(roll) + split[1])

                    #name roll
                    elif split[1][0].isdigit():
                        init = float(split[1])

                    else:
                        #mod name
                        name = split[1]
                        if split[0].startswith("+") or split[0].startswith("-") or split[0].startswith("/") or split[0].startswith("*"):
                            roll = random.randint(1, 20)
                            init = aeval(str(roll) + split[0])

                        #roll name
                        elif split[0][0].isdigit():
                            init = float(split[0])

                except Exception as e:
                    print(e)
                    await ctx.send('''```There was something I didnt understand about your input.
Ex: !init [name] [value OR modifier]

Currently I don't support inline dice rolls such as !init Gandalf +1d6```''')

            elif len(split) == 1 and split[0] != '':

                try:
                    if split[0][0].isdigit():
                        name = ctx.author.name
                        init = float(split[0])

                    elif split[0].startswith("+") or split[0].startswith("-") or split[0].startswith("/") or split[0].startswith("*"):
                        name = ctx.author.name
                        roll = random.randint(1, 20)
                        init = aeval(float(roll) + split[0])

                    else:
                        name = split[0]
                        init = random.randint(1, 20)

                except Exception as e:
                    print(e)
                    await ctx.send('''```There was something I didnt understand about your input.
Ex: !init [name] [value OR modifier]

Currently I don't support inline dice rolls such as !init Gandalf +1d6```''')
                    return
          
            elif len(split) == 1 and split[0] == '':
                name = ctx.author.name
                roll = random.randint(1, 20)
                init = float(roll)

            else:
                await ctx.send('''```There was something I didnt understand about your input.
Ex: !init [name] [value OR modifier]
Currently I don't support inline dice rolls such as !init Gandalf +1d6```''')

            try:
                init = float(init)
                name = str(name)

                data.initDict[key].addPlayer(name, init)
                await update_init(key)

            except Exception as e:
                print(e)
                await ctx.send('''```There was something I didnt understand about your input.
Ex: !init [name] [value OR modifier]

Currently I don't support inline dice rolls such as !init Gandalf +1d6```''')
                return

        else:
            await ctx.send('''```Please start initiative with !init start before adding players```''')


@bot.command()
async def init(ctx, *, args = ""):
    await init_helper(ctx, args)

@bot.command()
async def i(ctx, *, args = ""):
    await init_helper(ctx, args)

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

#region Help
@bot.command()
async def p(ctx, *, args = None):
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!help'] += 1

    if args != None:
        args = args.strip().lower()

    help_str = await data.help_handler.help(args)

    await ctx.send(help_str)
#endregion

#region Admin
@bot.command()
async def admin(ctx):
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!admin'] += 1

    retstr = '''```!admin is for server administrators. Currently the only command available to adminstrators is !set_prefix.

Commands:
!set_prefix [prefix]
    > Sets the server wide prefix to [prefix]. 
    Prefix must be /, !, ~, `, #, $, %, ^, &, *, ,, ., ;, :, <, or >
Note: If you forget the bot's prefix you will no longer be able to summon it and reset it's prefix.
For this reason, the prefix will be pinned in the channel from which it is changed.```'''

    await ctx.send(retstr)

@bot.command()
async def set_prefix(ctx, *, args = None):
    #TO DO:
    #Support pinging bot if you do not know the prefix
    #Removing bot from server should reset bot's prefix
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!set_prefix'] += 1

    if(not hasattr(ctx.author, 'ctx.author.guild_permissions')):
        await ctx.send(f"This command is for server use only.")

    if args:
        args = args.strip()

        if(ctx.author.guild_permissions.administrator):
            possibleArgs = set(['/','!','~','`','#','$','%','^','&','*',',','.',';',':','>','<'])

            if(len(args) < 1):
                await ctx.send(f"<@{ctx.author.id}>\n You must include arguments! Ex: !set_prefix &")
                return

            elif (args not in possibleArgs):
                await ctx.send(f"<@{ctx.author.id}>\n Prefix must be /, !, ~, `, #, $, %, ^, &, *, ,, ., ;, :, <, or >")
                return

            data.prefixDict[str(ctx.message.guild.id)] = args   
           
            msg = await ctx.send(f"<@{ctx.author.id}>\n Prefix for this server set to: {args.strip()}")
            await msg.pin()

        else:
                await ctx.send("Only server administrators have access to this command.")
    else:
        if(ctx.author.guild_permissions.administrator):
            await ctx.send(f"<@{ctx.author.id}>\n You must include arguments! Ex: !set_prefix &")
            return
        else:
            await ctx.send("Only server administrators have access to this command.")
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
        await ctx.send("```Thank you for submitting a request! Your request has been forwarded to the developer, kittysaurus.```")

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

#region Bank
@bot.command()
async def bank(ctx, *, args = None):
    """
    Rolls any number of dice in any format including skill checks
        Ex: !roll 1d20+5*6>100
    """
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!bank'] += 1

    if not args:
        await ctx.send(await data.bank.get_characters_formatted(ctx.author.id))

    if args:
        await ctx.send(await data.bank.parse_args(ctx.author.id, args))

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
[Updates]
> Added Feyre Bank. Use !bank to access and manage your character's purse strings!

[Bugs]
> Fixed a few typos.

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
                result = await data.diceRoller.parse(ctx.invoked_with[0:], gm = False)
            elif((ctx.invoked_with[0] == 'd' or ctx.invoked_with[1] == 'd' or ctx.invoked_with[2] == 'd')): # Treat this as some attempted dice input
                result = await data.diceRoller.parse(ctx.invoked_with[0:], gm = False)
            if(result and not result.startswith("```I'm sorry")): # this is bad but ill accept it for now
                await roll(ctx, args = ctx.invoked_with[0:])
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

