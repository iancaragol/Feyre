from pymongo import MongoClient
from bson.objectid import ObjectId

class UserManager:
    def __init__(self, mongo_uri):
        self.client = MongoClient(mongo_uri) #host uri
        self.db = self.client["feyre-mongodb-id"]    #Select the database
        self.users = self.db["users"]

    def dump_user_set(self, user_set):
        # user_query = {""}
        #self.users.insert_one({"set_id":0,"users":list(user_set)})

        self.users.find_one_and_update({'_id':ObjectId("5f6fa4ce55656df810b12a26")}, {"$set":{
            'users': list(user_set)
            }
        })

    def get_user_set(self):
        return set(self.users.find({'set_id':0}).next()['users'])