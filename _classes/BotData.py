import discord

from os import path
from json import load, dumps
from datetime import datetime

from _classes.BookOfTor import BookOfTor
from _classes.Monster import MonsterManual
from _classes.Feat import Feats
from _classes.Spellbook import Sb
from _classes.DiceRolls import Roller
# from _classes.Init import Initiative
from _classes.Weapons import Weapons
from _classes.Class_Abilities import Class_Abil
from _classes.Items import ItemLookup
from _classes.DeckOfMany import DeckOfMany
from _classes.ClassFeatures import ClassFeatures
from _classes.CurrencyConversion import CurrencyConverter
from _classes.Conditions import ConditionLookup
from _classes.Bank import Character, Bank

# from _classes.HelpHandler import HelpHandler
from _classes.StatsHandler import StatsHandler
from _classes.CharacterSelection import CharacterSelectionHandler

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
        self.weapons = Weapons()
        #self.class_abilities = Class_Abil() #deprecated
        self.item_lookup = ItemLookup()
        self.deck_of_many = DeckOfMany()
        self.class_features = ClassFeatures()
        self.currency_converter = CurrencyConverter()
        self.condition_lookup = ConditionLookup()

        self.bank = Bank()
        # self.help_handler = HelpHandler()
        self.stats_handler = StatsHandler()
        self.character_selection_handler = CharacterSelectionHandler()

        #Initiative tracking dictionaries
        # self.initDict = {}
        # self.initEmbedDict = {}

        self.roll_dict = {}

        self.gmDict = {}

        self.statsDict = {}
        self.prefixDict = {}

        self.embedcolor = discord.Color.from_rgb(165,87,249)

        self.userSet = set()

        try:
            pyDir = path.dirname(__file__)
            relPath = "..//_data//stats.txt"
            absRelPath = path.join(pyDir, relPath)
            self.statsDict = load(open(absRelPath))
            print("Stats loaded succesfully")

        except Exception as e:
            print(f"Error loading stats: {e}")
            self.statsDict = {'!tor horo':0, '!tor zodiac':0, '!hello':0, '!tor styles':0, '!tor randchar':0, '!roll':0,
                          '!help':0, '!mm':0, '!randmonster':0, '!feat':0, '!randfeat':0, '!init':0, '!spell':0, '!weapon':0}

        try:
            pyDir = path.dirname(__file__)
            relPath = "..//_data//gms.txt"
            absRelPath = path.join(pyDir, relPath)
            self.gmDict = load(open(absRelPath))
            print("GM's loaded succesfully")

        except Exception as e:
            print(f"Error loading GM's: {e}")
 
        try:
            pyDir = path.dirname(__file__)
            relPath = "..//_data//prefixes.txt"
            absRelPath = path.join(pyDir, relPath)
            self.prefixDict = load(open(absRelPath))
            print("Prefixes loaded succesfully")

        except Exception as e:
            print(f"Error loading prefixes: {e}")

        try:
            pyDir = path.dirname(__file__)
            relPath = "..//_data//users.txt"
            absRelPath = path.join(pyDir, relPath)
            self.userSet = set(load(open(absRelPath)))
            print("Users loaded succesfully")

        except Exception as e:
            print(f"Error loading users: {e}")

        print("\nTime: " + str(datetime.now()))

    