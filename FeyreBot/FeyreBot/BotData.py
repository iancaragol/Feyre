from os import path
from json import load, dumps

from BookOfTor import BookOfTor
from Monster import MonsterManual
from Feat import Feats
from Spellbook import Sb
from DiceRolls import Roller
from Init import Initiative
from datetime import datetime

import discord

class BotData():
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
            print("Stats loaded succesfully")

        except Exception as e:
            print(f"Error loading stats: {e}")
            self.statsDict = {'!tor horo':0, '!tor zodiac':0, '!hello':0, '!tor styles':0, '!tor randchar':0, '!roll':0,
                          '!help':0, '!mm':0, '!randmonster':0, '!feat':0, '!randfeat':0, '!init':0, '!spell':0}

        try:
            pyDir = path.dirname(__file__)
            relPath = "_data//prefixes.txt"
            absRelPath = path.join(pyDir, relPath)
            self.prefixDict = load(open(absRelPath))
            print("Prefixes loaded succesfully")

        except Exception as e:
            print(f"Error loading prefixes: {e}")

        try:
            pyDir = path.dirname(__file__)
            relPath = "_data//users.txt"
            absRelPath = path.join(pyDir, relPath)
            self.userSet = set(load(open(absRelPath)))
            print("Users loaded succesfully")

        except Exception as e:
            print(f"Error loading users: {e}")

        print("\nTime: " + str(datetime.now()))

    async def displayStats(self):
        retStr = f'''```asciidoc
= Lifetime Stats =
> !help: {self.statsDict['!help']}
> !hello: {self.statsDict['!hello']}
> !init: {self.statsDict['!init']}
> !roll: {self.statsDict['!roll']}

[D&D 5E]
> !feat: {self.statsDict['!feat']}
> !mm: {self.statsDict['!mm']}   
> !randfeat: {self.statsDict['!randfeat']}
> !randmonster: {self.statsDict['!randmonster']}
> !spell: {self.statsDict['!spell']}

[Book of Tor]
> !tor horo: {self.statsDict['!tor horo']}
> !tor randchar: {self.statsDict['!tor randchar']}
> !tor styles: {self.statsDict['!tor styles']}
> !tor zodiac: {self.statsDict['!tor zodiac']}

[Unique users: {len(self.userSet)}]```'''
        return retStr