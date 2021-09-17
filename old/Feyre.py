import discord
import sys
import os
import uuid

from discord.ext import commands
from pymongo import SLOW_ONLY

from _backend.CommonInfra import CommonInfra
from _backend.DataManager import DataManager

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
from _cogs.Spellbook import SpellbookCog
from _cogs.Monster import MonsterManualCog
from _cogs.Weapons import WeaponLookupCog
from _cogs.Items import ItemLookupCog
from _cogs.ClassFeatures import ClassFeaturesCog
from _cogs.Conditions import ConditionLookupCog
from _cogs.Stats import StatsCog
from _cogs.Developer import DeveloperCog
from _cogs.Social import SocialCog
from _cogs.TestDieRolls import TESTDiceRoller

# Populate ENV Variables
global bucket_key
global access_key
global env

try:
    env = os.environ['ENV'].upper()

    botid = uuid.uuid4()
    print(f'[#] BotID: {botid}\n[#] ENV: {env}')
    sys.stdout.flush()

    if env == "DEVELOPMENT":
        token = os.environ['FEYRE_TOKEN_DEV']
        mongo_uri = os.environ['MONGO_URI_DEV']
    elif (env == "PRODUCTION"):
        token = os.environ['FEYRE_TOKEN_PROD']
        mongo_uri = os.environ['MONGO_URI_PROD']

    bucket_key = os.environ['BUCKET_KEY']
    access_key = os.environ['ACCESS_KEY']

except KeyError:
    raise Exception("Unable to read Environment Variables.")

# CommonInfra is a class that holds a lot of the common resources
data = CommonInfra(mongo_uri = mongo_uri, botid = botid, env = env, bucket_key = bucket_key, access_key = access_key)

# Although I would like to define it in Common Infra, this function needs to be here.
async def get_pre(bot, message):
    if(message.guild == None):
        return '!'

    pre = data.prefixDict.get(str(message.guild.id), '!')
    return pre

# Feyre needs to be auto sharded to meet discord API rate limiting requirements
bot = commands.AutoShardedBot(command_prefix = get_pre)

# We implement our own help function, so the default must be removed
bot.remove_command('help')

# Add Cogs
# https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html
bot.add_cog(InitiativeCog(bot, data)) # Initiative
bot.add_cog(Helper(bot, data)) # Help
bot.add_cog(SimpleDiceRoller(bot, data)) # Simple Dice: dp, d20, d12, etc...
bot.add_cog(CharacterSelector(bot, data)) # Character Selection
bot.add_cog(Banker(bot, data)) # Bank
bot.add_cog(DeckOfManyThings(bot, data)) # Deck of Many Things
bot.add_cog(DiceRoller(bot, data)) # Dice Rolling
bot.add_cog(CurrencyConverter(bot, data)) # Currency Conversion
bot.add_cog(Administrator(bot, data)) # Administrator Commands
bot.add_cog(ClassAbilityLookupCog(bot, data)) # Ability Lookup
bot.add_cog(FeatLookupCog(bot, data)) # Feat
bot.add_cog(SpellbookCog(bot, data)) # Spellbook
bot.add_cog(WeaponLookupCog(bot, data)) # Weapons
bot.add_cog(ItemLookupCog(bot, data)) # Items
bot.add_cog(MonsterManualCog(bot, data)) # Monsters
bot.add_cog(ClassFeaturesCog(bot, data)) # Class Lookup
bot.add_cog(ConditionLookupCog(bot, data)) # Conditions
bot.add_cog(StatsCog(bot, data)) # Conditions
bot.add_cog(DeveloperCog(bot, data, StatsCog))
bot.add_cog(SocialCog(bot, data))
bot.add_cog(TESTDiceRoller(bot, data))

# Populate DataManager
data.dataManager = DataManager(bot, data, "_//data")

# This only works when it is here, I have no idea why!
# I tried moving this command to Social.py but the get_user would always return None
@bot.command()
async def request(ctx, *, args = None):
    data.userSet.add(ctx.author.id)
    data.statsDict['!request'] += 1

    if (args == None):
        await ctx.send("```!request requires arguments! Try !request [feature]```")
    else:
        user = await bot.fetch_user(112041042894655488)

        requestStr = f"**Feature Request**\nFrom: {ctx.author}\n\n{args}"
        await user.send(requestStr)
        await ctx.send("```Thank you for submitting a request! Your request has been forwarded to the developer, kittysaurus.\n\nYou can also visit the support server and chat with the developer directly by using the !support command.```")

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

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
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
    else:
        raise error
    # CommandNotFound errors are suppressed
    #print(error.args[0])

# Bot has started, is ready to receive messages
@bot.event
async def on_ready():
    print()
    print ("[#] Starting up...")
    print ("[#] I am running as: " + bot.user.name)
    print ("[#] With the ID: " + str(bot.user.id))
    print (f"[#] In a {env} environment")

    await bot.change_presence(activity = discord.Game(name="feyre.io | !help"))

    if (env == "PRODUCTION"):
        if (os.environ['ISS'].upper() == 'TRUE'):
            print("[#] Starting stream to initial state...")
            data.dataManager.send_data.start()
        else:
            print("[#] Stream environment variable not set. Skipping stream.")

        data.dataManager.save_data.start()
        print("[#] Started auto backup of data.")

    elif (env == "DEVELOPMENT"):
        print("[#] Feyre is running in a development environment. Data will not be saved or streamed.")

    sys.stdout.flush()

# Start the Bot
bot.run(token)