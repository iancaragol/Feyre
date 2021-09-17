import discord
import numpy

from os import access, path
from json import load, dumps
from datetime import datetime

from _classes.BookOfTor import BookOfTor

from _backend.GmManager import GmManager
from _backend.StatsManager import StatsManager
from _backend.UserManager import UserManager
from _backend.PrefixesManager import PrefixManager

class CommonInfra():
    """
    Class containing common resources used across different cogs
    """
    def __init__(self, mongo_uri, botid, env, bucket_key, access_key):
        """
        Initializes the CommonInfra() class

        Raises:
            File read error
            JSON read error
        """
        self.bookOfTor = BookOfTor()

        self.roll_dict = {}

        self.gmDict = {}

        self.statsDict = {}
        self.prefixDict = {}

        self.embedcolor = discord.Color.from_rgb(165,87,249)

        self.userSet = set()

        self.mongo_uri = mongo_uri
        self.botid = botid
        self.env = env
        self.bucket_key = bucket_key
        self.access_key = access_key

        # These values are set after the bot has been initialized
        # DataManager holds all of the streaming and Feyre data
        self.dataManager = None # DataManager must be set after the bot has been initialized
        self.dev_user = None # Work around to allow Social request command to DM 

        try:
            print("Loading stats from mongo db...")
            sm = StatsManager(self.mongo_uri)
            self.statsDict = sm.get_stats_sync()
            print("Stats loaded successfully")

        except Exception as e:
            try:
                print(f"Error loading stats: {e}")
                print("Loading stats from disk...")
                pyDir = path.dirname(__file__)
                relPath = "..//_data//stats.txt"
                absRelPath = path.join(pyDir, relPath)
                self.statsDict = load(open(absRelPath))
                print("Stats loaded successfully")

            except Exception as e:
                print("Error loading stats: {}".format(e))

        try:
            print("Loading users from mongo db...")
            um = UserManager(self.mongo_uri)
            self.userSet = um.get_user_set_sync()
            print("Users loaded successfully")

        except Exception as e:
            try:
                print(f"Error loading users: {e}")
                print("Loading users from disk...")
                pyDir = path.dirname(__file__)
                relPath = "..//_data//users.txt"
                absRelPath = path.join(pyDir, relPath)
                self.userSet = set(load(open(absRelPath)))
                print("Users loaded successfully")

            except Exception as e:
                print(f"Error loading GM's: {e}")

        try:
            print("Loading gms from mongo db...")
            gm = GmManager(self.mongo_uri, sync=True)
            self.gmDict = gm.get_gm_dict_sync()
            print("Gms loaded successfully")
        
        except Exception as e:
            try:
                print(f"Error loading GM's: {e}")
                print("Loading gms from disk...")
                pyDir = path.dirname(__file__)
                relPath = "..//_data//gms.txt"
                absRelPath = path.join(pyDir, relPath)
                self.gmDict = load(open(absRelPath))
                print("GM's loaded successfully")

            except Exception as e:
                print(f"Error loading GM's: {e}")
 
        try:
            print("Loading prefixes from mongo db...")
            pm = PrefixManager(self.mongo_uri, sync=True)
            self.prefixDict = pm.get_prefix_dict_sync()
            print("Prefixes loaded successfully")
        
        except Exception as e:
            try:
                print(f"Error loading prefixes: {e}")
                print("Loading prefixes from disk...")
                pyDir = path.dirname(__file__)
                relPath = "..//_data//prefixes.txt"
                absRelPath = path.join(pyDir, relPath)
                self.prefixDict = load(open(absRelPath))
                print("Prefixes loaded successfully")

            except Exception as e:
                print(f"Error loading prefixes: {e}")

        print("\nTime: " + str(datetime.now()))

    async def string_splitter(self, string, char, max_splits):
        idxs = numpy.array([pos for pos, c in enumerate(string) if char == c])

        split_arr = []
        char_constant = 1800 # Maximum number of chars we will send
        prev_lower = 0

        for i in range(max_splits):
            leq = char_constant * (i+1)
            lower = idxs[idxs < leq].max()
            
            split_arr.append(string[prev_lower:lower])
            prev_lower = lower

            if leq > len(string):
                break

        return split_arr


    async def createAndSendEmbeds(self, ctx, returnedArray):
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
    
    async def codify(self, string, title = None):
        if title:
            s = f'''```md
    # {title}

    {string}```'''
        
        else:
            s = '```' + string + '```'
        return s    