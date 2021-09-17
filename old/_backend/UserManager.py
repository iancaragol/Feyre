from pymongo import MongoClient
from bson.objectid import ObjectId

import motor.motor_asyncio
import pymongo

class UserManager:
    def __init__(self, mongo_uri):
        #self.client = MongoClient(mongo_uri) #host uri
        self.sync_client = MongoClient(mongo_uri) #host uri
        self.sync_users = self.sync_client["feyre-mongodb-id"]["users"]
        self.client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
        self.db = self.client["feyre-mongodb-id"]    #Select the database
        self.users = self.db["users"]

    async def dump_user_set(self, user_set):
        user_dict = {"user_list" : list(user_set)}
        await self.users.insert_one(user_dict)

    async def get_user_set(self):
        as_list = list(self.sync_users.find().sort('_id', pymongo.DESCENDING).limit(1))
        as_set = set(as_list[0]["user_list"])
        return as_set

    def get_user_set_sync(self): # Used when the bot starts up
        as_list = list(self.sync_users.find().sort('_id', pymongo.DESCENDING).limit(1))
        as_set = set(as_list[0]["user_list"])
        return as_set