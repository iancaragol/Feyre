from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

import motor.motor_asyncio

class StatsManager:
    def __init__(self, mongo_uri):
        self.sync_client = MongoClient(mongo_uri) #host uri
        self.sync_stats = self.sync_client["feyre-mongodb-id"]["stats"]
        self.client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
        self.db = self.client["feyre-mongodb-id"]    #Select the database
        self.stats = self.db["stats"]
        self.keys = [ # This is a list of all commands/keys for stats dictionary. When adding a new command just add it here
            "!ability",
            "!character",
            "chars_added",
            "rerolls",
            "!tor horo",
            "!tor zodiac",
            "!hello",
            "!tor styles",
            "!tor randchar", 
            "!roll",
            "!help",
            "!mm",
            "!randmonster",
            "!feat",
            "!randfeat",
            "!init",
            "!spell",
            "!weapon",
            "!item",
            "!gm", 
            "!new",
            "!admin",
            "!set_prefix",
            "!request",
            "!dom", 
            "!c", 
            "!currency",
            "!vote",
            "!condition",
            "!bank",
            "dirty_rolls"
        ]

    async def dump_stats_dict(self, stats_dict):
        # Add date time to stats dict
        date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        stats_dict['date'] = date_time

        await self.stats.insert_one(stats_dict)

    def validate_stats_sync(self, stats_dict):
        """
        This function adds any missing keys. As new commands are added the dictionary read from MongoDB may be out of date
        """
        for key in self.keys:
            if key not in stats_dict.keys():
                stats_dict[key] = 0
                print(f"Added {key} to stats dictionary.")

        del stats_dict['_id'] # Remove this because a new one will be generated when saving the stats dictionary

        print("Removed _id from stats dict")
        print("Stats validated succssfully.")
        return stats_dict

    async def validate_stats(self, stats_dict):
        """
        This function adds any missing keys. As new commands are added the dictionary read from MongoDB may be out of date
        """
       
        for key in self.keys:
            if key not in stats_dict.keys():
                stats_dict[key] = 0
                print(f"Added {key} to stats dictionary.")

        del stats_dict['_id'] # Remove this because a new one will be generated when saving the stats dictionary

        print("Removed _id from stats dict")
        print("Stats validated succssfully.")
        return stats_dict

    async def get_stats(self):
        stats_dict = await self.stats.find().sort('_id',-1).limit(1)[0]
        return await self.validate_stats(stats_dict)

    def get_stats_sync(self): # Used on startup
        stats_dict = self.sync_stats.find().sort('_id',-1).limit(1)[0]
        return self.validate_stats_sync(stats_dict)