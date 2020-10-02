from pymongo import MongoClient
from bson.objectid import ObjectId

import motor.motor_asyncio

class PrefixManager:
    def __init__(self, mongo_uri, sync = False):
        if sync:
            self.client = MongoClient(mongo_uri) #host uri
        else:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)

        self.db = self.client["feyre-mongodb-id"]    #Select the database
        self.prefixes = self.db["prefix"]

    async def dump_prefix_dict(self, prefix_dict):
        await self.prefixes.insert_one(prefix_dict)

    async def get_prefix_dict(self):
        prefix_dict = await self.prefixes.find().sort('_id',-1).limit(1)
        return prefix_dict[0]

    def get_prefix_dict_sync(self): # Used on startup
        prefix_dict = self.prefixes.find().sort('_id',-1).limit(1)[0]
        return prefix_dict
        