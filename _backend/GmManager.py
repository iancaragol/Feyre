from pymongo import MongoClient
from bson.objectid import ObjectId

import motor.motor_asyncio

class GmManager:
    def __init__(self, mongo_uri, sync = False):
        if sync:
            self.client = MongoClient(mongo_uri) #host uri
        else:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)

        self.db = self.client["feyre-mongodb-id"]    #Select the database
        self.gms = self.db["gms"]

    async def dump_gm_dict(self, gm_dict):
        await self.gms.insert_one(gm_dict)

    async def get_gm_dict(self):
        gm_dict = await self.gms.find().sort('_id',-1).limit(1)[0]
        return gm_dict

    def get_gm_dict_sync(self): # Used on startup
        gm_dict = self.gms.find().sort('_id',-1).limit(1)[0]
        return gm_dict
        