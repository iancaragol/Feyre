import os
import pymongo
import traceback

from http import HTTPStatus
from flask import Blueprint, request
from pymongo import MongoClient
from common.redis_helper import RedisHelper
from datetime import datetime
from backend_service.api.operation.stats_operation import StatsOperation

stats_sync_api = Blueprint('stats', __name__)
redis_helper = RedisHelper()

if not os.environ.get('DB_BYPASS', None):
    mongo_uri = os.environ['MONGO_URI']
    mongo_client = MongoClient(mongo_uri)
    command_collection = mongo_client.backend_db.command_stats
    command_collection.create_index("_ts", expireAfterSeconds = 5184000) # TTL is 60 days

# This json is updated whenever the new sync occurs
last_sync = {}
last_sync["message"] = "command_stats has not been synced since service startup."

@stats_sync_api.route('/', methods=['PUT'])
def put_cmd_stats_set():
    """
    Puts the current user set stored in Redis into the Mongo DB.
    """
    try:
        statblock = construct_cmd_stats_json()
        insert_id = command_collection.insert_one(statblock).inserted_id
    
        return f"Inserted stats set into backend_db. ID is {insert_id}. insert_time is {statblock['insert_time']}", HTTPStatus.OK
    except Exception as e:
        return f"An exception occurred when updating the Mongo DB.\n{e}\n{traceback.format_exc()}", HTTPStatus.INTERNAL_SERVER_ERROR

@stats_sync_api.route('/', methods=['GET'])
def get_stats():
    """
    Returns user_set as a json
    """
    stats = construct_cmd_stats_json()
    
    return stats, HTTPStatus.OK

@stats_sync_api.route('/sync', methods=['PUT'])
def sync_stats_set():
    """
    Syncs Redis and Mongo DB

    Query Parameters:
        sync=1 : Does a sync operation

    If the sync parameter is set to true, we will check the last update time for command_stats in Redis and MongoDB.

    If the the number of seconds since Mongo DB last update time is less than Redis then MongoDB holds the most recent set of data. In that case the Redis set needs to be updated.
    This should only happen if there redis backups were deleted, or on a cold start where no volumes are mounted

    If Redis > Mongo DB time, then just PUT the contents of command_stats in MongoDB
    """
    args = request.args

    # sync=1 or sync=true
    sync = False
    if "sync" in args:
        sync = bool(args["sync"])

    try:
        if sync:
            sync_result = sync_stats()
            return f"{sync_result}", HTTPStatus.OK
        else:
            return f"Sync=true query parameter was not provided. This is a NO-OP.", HTTPStatus.OK
    except Exception as e:
        return f"An exception occurred when syncing.\n{e}\n{traceback.format_exc()}", HTTPStatus.INTERNAL_SERVER_ERROR

@stats_sync_api.route('/sync', methods=['GET'])
def get_last_sync():
    """
    Returns information on the last sync as a json
    """
    
    return last_sync, HTTPStatus.OK

def sync_stats():
    """
    Syncs Redis and Mongo DB by comparing Redis c_:updated_time and MongoDB command_stats:insert_timestamp

    If Redis contains the most recent data set, we update Mongo DB to match Redis

    If Mongo DB contains the most recent data set, we update Redis to match Mongo DB

    If they are perfectly in sync (very unlikely), its a NO-OP
    """
    now = datetime.now()
    now_string = now.strftime("%m/%d/%Y, %H:%M:%S")
    sync_msg = ""
    completed_successfully = True
    print(f"   [1] Starting sync_stats operation. Time is {now_string}", flush = True)

    try:
        # All redis keys have an additional key called key:updated_time which contains the last time that particularly key was updated as timestamp
        # Redis does not store that value by default
        redis_stats_dict = construct_cmd_stats_json()
        redis_stats_set_updated_time_seconds = (now - redis_helper.get_stats_set_timestamp_as_datetime()).total_seconds()
        print(f"   [2] Redis c_:updated_time was last updated {str(redis_stats_set_updated_time_seconds)} seconds ago.", flush = True)

        # Get the last entry into the Mongo DB sorted by _id
        # The last entry will ALWAYS be the most recent
        mongoDB_last_entry = command_collection.find_one(sort = [('_id', pymongo.DESCENDING)])
        mongoDB_last_entry_timestamp = datetime.fromtimestamp(mongoDB_last_entry["insert_timestamp"])
        mongoDB_last_entry_seconds = (now - mongoDB_last_entry_timestamp).total_seconds()
        print(f"   [3] MongoDB command_stats was last updated {mongoDB_last_entry_seconds} seconds ago.", flush=True)

        # Compare last update time for Redis and Mongo DB
        if (redis_stats_set_updated_time_seconds < mongoDB_last_entry_seconds):
            stats = construct_cmd_stats_json()
            insert_id = command_collection.insert_one(stats).inserted_id

            sync_msg = f"Redis contained the most recent command stats. No need to update Redis set. Updated MongoDB to match Redis. Insert_ID: {insert_id}"

        elif (redis_stats_set_updated_time_seconds > mongoDB_last_entry_seconds):
            before_update_time = redis_helper.get_stats_set_timestamp_as_datetime().strftime("%m/%d/%Y, %H:%M:%S")
            after_update_time = redis_helper.get_stats_set_timestamp_as_datetime().strftime("%m/%d/%Y, %H:%M:%S")
            update_redis_from_mongoDB(mongoDB_last_entry)
            sync_msg = f"MongoDB contained the most recent command stats. Updated the Redis set to match. Redis command total count was {redis_stats_dict['total']} and was last updated at {before_update_time}. Now the total count is {mongoDB_last_entry['stat_block']['total']}. It was updated at {after_update_time}."

        else:
            sync_msg = f"Wow! Redis and Mongo DB were perfectly in sync! This is a NO-OP."

        print("   [4] " + sync_msg, flush = True)
        print("   [5] Sync Stats operation completed.\n\n", flush = True)
    except Exception as e:
        sync_msg = f"An error occurred when attempting to sync stats.\n{e}\n{traceback.format_exc()}"
        completed_successfully = False

    last_sync["message"] = sync_msg
    last_sync["completed_successfully"] = completed_successfully
    last_sync["sync_time"] = now_string
    last_sync["sync_timestamp"] = now.timestamp()

    return sync_msg

def construct_cmd_stats_json():
    """
    Returns stats json by executing a StatsOperation
    """
    now = datetime.now()

    stats = StatsOperation(show_all = True).execute()
    stats["insert_time"] =now.strftime("%m/%d/%Y, %H:%M:%S") # Friendly time stamp
    stats["insert_timestamp"] = now.timestamp() # This is the one that is always used

    return stats

def update_redis_from_mongoDB(mongoDB_entry):
    for k, v in mongoDB_entry["stat_block"].items():
        redis_helper.set_command(k, v)