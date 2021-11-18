import os
import traceback

from http import HTTPStatus
from flask import Blueprint, request
from datetime import datetime
from common.redis_helper import RedisHelper
from common.table_helper import TableHelper
from backend_service.api.operation.stats_operation import StatsOperation

stats_sync_api = Blueprint('stats', __name__)
redis_helper = RedisHelper()
table_helper = TableHelper()

#if not os.environ.get('STORAGE_BYPASS', None):
environment = os.environ.get("ENV")  

# This json is updated whenever the new sync occurs
last_sync = {}
last_sync["message"] = "command_stats has not been synced since service startup."

@stats_sync_api.route('/', methods=['PUT'])
def put_cmd_stats_set():
    """
    Puts the current user set stored in Redis into the Stats Table.
    """
    try:
        statblock = construct_cmd_stats_json()
        insert_row_key = table_helper.insert_entity("stats", statblock)
    
        return f"Inserted stats set into Table. RowKey is {insert_row_key} insert_time is {statblock['insert_time']}", HTTPStatus.OK
    except Exception as e:
        return f"An exception occurred when updating the Table.\n{e}\n{traceback.format_exc()}", HTTPStatus.INTERNAL_SERVER_ERROR

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
    Syncs Redis and Stats Table

    Query Parameters:
        sync=1 : Does a sync operation

    If the sync parameter is set to true, we will check the last update time for command_stats in Redis and Stats Table.

    If the the number of seconds since Stats Table last update time is less than Redis then Stats Table holds the most recent set of data. In that case the Redis set needs to be updated.
    This should only happen if there redis backups were deleted, or on a cold start where no volumes are mounted

    If Redis > Stats Table time, then just PUT the contents of command_stats in Stats Table
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
    Syncs Redis and Stats Table by comparing Redis c_:updated_time and Stats Table insert_timestamp

    If Redis contains the most recent data set, we update Stats Table to match Redis

    If Stats Table contains the most recent data set, we update Redis to match the Stats Table

    If they are perfectly in sync (very unlikely), its a NO-OP
    """
    now = datetime.utcnow()
    now_string = now.strftime("%m/%d/%Y, %H:%M:%S")
    sync_msg = ""
    completed_successfully = True
    print(f"   [1] Starting sync_stats operation. Time is {now_string}", flush = True)

    try:
        # All redis keys have an additional key called key:updated_time which contains the last time that particularly key was updated as timestamp
        # Redis does not store that value by default
        redis_stats_dict = construct_cmd_stats_json()
        redis_stats_dict_update_time = redis_helper.get_commands_dictionary_last_update_time()
        redis_stats_set_updated_time_seconds = (now - redis_stats_dict_update_time).total_seconds()
        print(f"   [2] Redis c_:updated_time was last updated {str(redis_stats_set_updated_time_seconds)} seconds ago.", flush = True)

        # Get the last entry into the stats Table
        # The last entry will ALWAYS be the most recent
        table_storage_last_entry = table_helper.get_entity("stats")
        print(table_storage_last_entry, flush=True)
        table_storage_last_entry_seconds = (now - datetime.fromtimestamp(table_storage_last_entry['insert_timestamp'])).total_seconds()
        print(f"   [3] TableStorage stats last entry was added {table_storage_last_entry_seconds} seconds ago.", flush=True)

        # Compare last update time for Redis and Table Storage
        if (redis_stats_set_updated_time_seconds < table_storage_last_entry_seconds):
            stats = construct_cmd_stats_json()
            table_helper.insert_entity("stats", stats)

            sync_msg = f"Redis contained the most recent command stats. No need to update Redis set. Updated Table to match Redis."

        elif (redis_stats_set_updated_time_seconds > table_storage_last_entry_seconds):
            updated_table = update_redis_from_table(table_storage_last_entry)
            after_update_time = redis_helper.get_commands_dictionary_last_update_time().strftime("%m/%d/%Y, %H:%M:%S")

            sync_msg = f"Table contained the most recent command stats. Updated the Redis set to match. Redis command total count was {redis_stats_dict['total']} and was last updated at {redis_stats_dict_update_time}. Now the total count is {updated_table['total']}. It was updated at {after_update_time}."

        else:
            sync_msg = f"Wow! Redis and Table were perfectly in sync! This is a NO-OP."

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
    now = datetime.utcnow()

    stats = StatsOperation(show_all = True).execute()
    stats["insert_time"] = now.strftime("%m/%d/%Y, %H:%M:%S") # Friendly time stamp
    stats["insert_timestamp"] = now.timestamp() # This is the one that is always used

    return stats

def update_redis_from_table(table_entry):
    return redis_helper.set_commands_dictionary(table_entry)