import os
import pymongo
import traceback

from http import HTTPStatus
from flask import Blueprint, request
from pymongo import MongoClient
from common.redis_helper import RedisHelper
from datetime import datetime

users_sync_api = Blueprint('users', __name__)
redis_helper = RedisHelper()

if not os.environ.get('DB_BYPASS', None):
    mongo_uri = os.environ['MONGO_URI']
    mongo_client = MongoClient(mongo_uri)
    users_collection = mongo_client.backend_db.user_set
    users_collection.create_index("_ts", expireAfterSeconds = 5184000) # TTL is 60 days

# This json is updated whenever the new sync occurs
last_sync = {}
last_sync["message"] = "user_set has not been synced since service startup."

@users_sync_api.route('/', methods=['PUT'])
def put_users_set():
    """
    Puts the current user set stored in Redis into the Mongo DB.
    """
    try:
        users = construct_users_json()
        insert_id = users_collection.insert_one(users).inserted_id
    
        return f"Inserted users set into backend_db. ID is {insert_id}. insert_time is {users['insert_time']}", HTTPStatus.OK
    except Exception as e:
        return f"An exception occurred when updating the Mongo DB.\n{e}\n{traceback.format_exc()}", HTTPStatus.INTERNAL_SERVER_ERROR

@users_sync_api.route('/', methods=['GET'])
def get_users():
    """
    Returns user_set as a json
    """
    users = construct_users_json()
    
    return users, HTTPStatus.OK

@users_sync_api.route('/sync', methods=['PUT'])
def sync_users_set():
    """
    Syncs Redis and Mongo DB

    Query Parameters:
        sync=1 : Does a sync operation

    If the sync parameter is set to true, we will check the last update time for user_set in Redis and MongoDB.

    If the the number of seconds since Mongo DB last update time is less than Redis then MongoDB holds the most recent set of data. In that case the Redis set needs to be updated.
    This should only happen if there redis backups were deleted, or on a cold start where no volumes are mounted

    If Redis > Mongo DB time, then just PUT the contents of user_set in MongoDB
    """
    args = request.args

    # sync=1 or sync=true
    sync = False
    if "sync" in args:
        sync = bool(args["sync"])

    try:
        if sync:
            sync_result = sync_users()
            return f"{sync_result}", HTTPStatus.OK
        else:
            return f"Sync=true query parameter was not provided. This is a NO-OP.", HTTPStatus.OK
    except Exception as e:
        return f"An exception occurred when syncing.\n{e}\n{traceback.format_exc()}", HTTPStatus.INTERNAL_SERVER_ERROR

@users_sync_api.route('/sync', methods=['GET'])
def get_last_sync():
    """
    Returns information on the last sync as a json
    """
    
    return last_sync, HTTPStatus.OK

def sync_users():
    """
    Syncs Redis and Mongo DB by comparing Redis user_set:update_time and MongoDB user_set:insert_timestamp

    If Redis contains the most recent data set, we update Mongo DB to match Redis

    If Mongo DB contains the most recent data set, we update Redis to match Mongo DB

    If they are perfectly in sync (very unlikely), its a NO-OP
    """
    now = datetime.utcnow()
    now_string = now.strftime("%m/%d/%Y, %H:%M:%S")
    sync_msg = ""
    completed_successfully = True
    print(f"   [1] Starting sync_users operation. Time is {now_string}", flush = True)

    try:
        # All redis keys have an additional key called key:updated_time which contains the last time that particularly key was updated as timestamp
        # Redis does not store that value by default
        redis_user_set_updated_time_seconds = (now - redis_helper.get_user_set_timestamp_as_datetime()).total_seconds()
        print(f"   [2] Redis user_set was last updated {str(redis_user_set_updated_time_seconds)} seconds ago.", flush = True)

        # Get the last entry into the Mongo DB sorted by _id
        # The last entry will ALWAYS be the most recent
        mongoDB_last_entry = users_collection.find_one(sort = [('_id', pymongo.DESCENDING)])
        mongoDB_last_entry_timestamp = datetime.fromtimestamp(mongoDB_last_entry["insert_timestamp"])
        mongoDB_last_entry_seconds = (now - mongoDB_last_entry_timestamp).total_seconds()
        print(f"   [3] MongoDB user_set was last updated {mongoDB_last_entry_seconds} seconds ago.", flush=True)

        # Compare last update time for Redis and Mongo DB
        if (redis_user_set_updated_time_seconds < mongoDB_last_entry_seconds):
            users = construct_users_json()
            insert_id = users_collection.insert_one(users).inserted_id

            sync_msg = f"Redis contained the most recent user_set. No need to update Redis set. Updated MongoDB to match Redis. Insert_ID: {insert_id}"

        elif (redis_user_set_updated_time_seconds > mongoDB_last_entry_seconds):
            before_update_count = redis_helper.get_user_set_count()
            before_update_time = redis_helper.get_user_set_timestamp_as_datetime().strftime("%m/%d/%Y, %H:%M:%S")
            user_set = redis_helper.get_user_set()
            redis_helper.add_to_user_set(user_set)
            after_update_time = redis_helper.get_user_set_timestamp_as_datetime().strftime("%m/%d/%Y, %H:%M:%S")

            sync_msg = f"MongoDB contained the most recent set. Updated the Redis set to match. Redis user_set contained {before_update_count} entries and was updated at {before_update_time}. Now it contains {len(mongoDB_last_entry['user_set'])} entries and was updated at {after_update_time}."

        else:
            sync_msg = f"Wow! Redis and Mongo DB were perfectly in sync! This is a NO-OP."

        print("   [4] " + sync_msg, flush = True)
        print("   [5] Sync operation completed.\n\n", flush = True)
    except Exception as e:
        sync_msg = f"An error occurred when attempting to sync.\n{e}\n{traceback.format_exc()}"
        completed_successfully = False

    last_sync["message"] = sync_msg
    last_sync["completed_successfully"] = completed_successfully
    last_sync["sync_time"] = now_string
    last_sync["sync_timestamp"] = now.timestamp()

    return sync_msg

def construct_users_json():
    """
    Returns user_set json, data is read from Redis
    """
    now = datetime.utcnow()

    users = {}
    users["user_set"] = redis_helper.get_user_set()
    users["insert_time"] = now.strftime("%m/%d/%Y, %H:%M:%S") # Friendly time stamp
    users["insert_timestamp"] = now.timestamp() # This is the one that is always used

    return users