from pymongo import MongoClient
from bson.objectid import ObjectId

import motor.motor_asyncio

class UserManager:
    def __init__(self, mongo_uri):
        #self.client = MongoClient(mongo_uri) #host uri
        self.sync_client = MongoClient(mongo_uri) #host uri
        self.sync_users = self.sync_client["feyre-mongodb-id"]["users"]
        self.client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
        self.db = self.client["feyre-mongodb-id"]    #Select the database
        self.users = self.db["users"]

    async def dump_user_set(self, user_set):
        # user_query = {""}
        #self.users.insert_one({"set_id":0,"users":list(user_set)})

        await self.users.find_one_and_update({'_id':ObjectId("5f6fa4ce55656df810b12a26")}, {"$set":{
            'users': list(user_set)
            }
        })

    async def get_user_set(self):
        return set(await self.users.find({'set_id':0}).next()['users'])

    def get_user_set_sync(self): # Used when the bot starts up
        return set(self.sync_users.find({'set_id':0}).next()['users'])