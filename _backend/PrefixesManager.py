from pymongo import MongoClient
from bson.objectid import ObjectId

import motor.motor_asyncio
import pymongo

class PrefixManager:
    def __init__(self, mongo_uri, sync = False):
        self.sync_client = MongoClient(mongo_uri) #host uri
        self.sync_prefixes = self.sync_client["feyre-mongodb-id"]["prefix"]
        self.client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
        self.db = self.client["feyre-mongodb-id"]    #Select the database
        self.prefixes = self.db["prefix"]

    async def dump_prefix_dict(self, prefix_dict):
        await self.prefixes.insert_one(prefix_dict)

    async def get_prefix_dict(self):
        prefixes_dict = list(self.sync_prefixes.find().sort('_id', pymongo.DESCENDING).limit(1))[0]
        return prefixes_dict 

    def get_prefix_dict_sync(self): # Used on startup
        prefixes_dict = list(self.sync_prefixes.find().sort('_id', pymongo.DESCENDING).limit(1))[0]
        return prefixes_dict 
        