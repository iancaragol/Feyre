import traceback

from fastapi import APIRouter
from fastapi.responses import Response
from json import dumps, loads

from http import HTTPStatus
from common.blob_helper import BlobHelper
from common.redis_helper import RedisHelper
from datetime import datetime
from sync_service.api.models.last_sync import LastSync

users_router = APIRouter()
redis_helper = RedisHelper()
blob_helper = BlobHelper()
last_sync = LastSync()

@users_router.put('/api/syncservice/users')
def put_users_set():
    """
    Puts the current user set stored in Redis into the Mongo DB.
    """
    try:
        users = construct_users_json()
        up = blob_helper.upload_blob_from_bytes("users", users["filename"], dumps(users))
    
        print(up, flush=True)

        return Response(content = f"Inserted users set into Blob Storage. Filename is {users['filename']}, insert_time is {users['insert_time']}", status_code = HTTPStatus.OK)
    except Exception as e:
        return f"An exception occurred when updating the Users Table.\n{e}\n{traceback.format_exc()}", HTTPStatus.INTERNAL_SERVER_ERROR

@users_router.get('/api/syncservice/users')
def get_users():
    """
    Returns user_set as a json
    """
    users = construct_users_json()
    
    return Response(content = dumps(users), status_code = HTTPStatus.OK)

@users_router.put('/api/syncservice/users/sync')
def sync_users_set(sync : bool = False):
    """
    Syncs Redis and Blob Storage

    Query Parameters:
        sync=1 : Does a sync operation

    If the sync parameter is set to true, we will check the last update time for user_set in Redis and Blob Storage.

    If the the number of seconds since Blob Storage last update time is less than Redis then Blob Storage holds the most recent set of data. In that case the Redis set needs to be updated.
    This should only happen if there redis backups were deleted, or on a cold start where no volumes are mounted

    If Redis > Blob Storage time, then just PUT the contents of user_set in Blob Storage
    """
    try:
        if sync:
            sync_result = sync_users()
            return Response(content = f"{sync_result}", status_code = HTTPStatus.OK)
        else:
            return Response(content = f"Sync=true query parameter was not provided. This is a NO-OP.", status_code = HTTPStatus.OK)
    except Exception as e:
        return Response(content = f"An exception occurred when syncing.\n{e}\n{traceback.format_exc()}", status_code = HTTPStatus.INTERNAL_SERVER_ERROR)

@users_router.get('/api/syncservice/users/sync')
def get_last_sync_as_json():
    """
    Returns information on the last sync as a json
    """
    
    return Response(content = dumps(last_sync.to_dict()), status_code = HTTPStatus.OK)

def get_last_sync():
    """
    Helper function, used by the metrics collector to get info on the last sync.
    """
    
    return last_sync

def sync_users():
    """
    Syncs Redis and Blob Storage by comparing Redis user_set:update_time and Blob Storage user_set:insert_timestamp

    If Redis contains the most recent data set, we update Blob Storage to match Redis

    If Blob Storage contains the most recent data set, we update Redis to match Blob Storage

    If they are perfectly in sync (very unlikely), its a NO-OP
    """
    now = datetime.utcnow()
    now_string = now.strftime("%m/%d/%Y, %H:%M:%S")
    sync_msg = ""
    completed_successfully = True
    who_updated = "nobody"
    print(f"   [1] Starting sync_users operation. Time is {now_string}", flush = True)

    try:
        # All redis keys have an additional key called key:updated_time which contains the last time that particularly key was updated as timestamp
        # Redis does not store that value by default
        redis_user_set_updated_time_seconds = (now - redis_helper.get_user_set_timestamp_as_datetime()).total_seconds()
        print(f"   [2] Redis user_set was last updated {str(redis_user_set_updated_time_seconds)} seconds ago.", flush = True)

        # Temporarily download the most recent blob
        user_blob_last_entry_name = blob_helper.list_blobs("users", "creation_time", reverse = True)[0].name
        user_blob_last_entry = loads(blob_helper.download_blob_as_bytes("users", user_blob_last_entry_name))
        user_blob_last_entry_seconds = (now - datetime.fromtimestamp(user_blob_last_entry['insert_timestamp'])).total_seconds()
        print(f"   [3] BlobStorage last users entry was added {user_blob_last_entry_seconds} seconds ago.", flush=True)

        # Compare last update time for Redis and Mongo DB
        if (redis_user_set_updated_time_seconds < user_blob_last_entry_seconds):
            users = construct_users_json()
            user_as_bytes = dumps(users)
            up = blob_helper.upload_blob_from_bytes("users", users["filename"], user_as_bytes)
            who_updated = "table"

            sync_msg = f"Redis contained the most recent user_set. No need to update Redis set. Updated Blob Storage to match Redis. FileName: {users['filename']}, Size: {len(user_as_bytes)}"

        elif (redis_user_set_updated_time_seconds > user_blob_last_entry_seconds):
            before_update_count = redis_helper.get_user_set_count()
            before_update_time = redis_helper.get_user_set_timestamp_as_datetime().strftime("%m/%d/%Y, %H:%M:%S")
            redis_helper.add_to_user_set(user_blob_last_entry["user_set"])
            after_update_time = redis_helper.get_user_set_timestamp_as_datetime().strftime("%m/%d/%Y, %H:%M:%S")
            who_updated = "redis"

            sync_msg = f"Blob Storage contained the most recent set. Updated the Redis set to match. Redis user_set contained {before_update_count} entries and was updated at {before_update_time}. Now it contains {len(user_blob_last_entry['user_set'])} entries and was updated at {after_update_time}."

        else:
            sync_msg = f"Wow! Redis and Blob Storage were perfectly in sync! This is a NO-OP."

        print("   [4] " + sync_msg, flush = True)
        print("   [5] Sync operation completed.\n\n", flush = True)
    except Exception as e:
        sync_msg = f"An error occurred when attempting to sync.\n{e}\n{traceback.format_exc()}"
        print(sync_msg, flush = True)
        completed_successfully = False

    # Update the last sync object
    last_sync.message = sync_msg
    last_sync.completed_successfully = completed_successfully
    last_sync.who_updated = who_updated
    last_sync.sync_time = now_string
    last_sync.sync_timestamp = now.timestamp()

    return sync_msg

def construct_users_json():
    """
    Returns user_set json, data is read from Redis
    """
    now = datetime.utcnow()

    users = {}
    users["user_set"] = redis_helper.get_user_set()
    users["insert_time"] = now.strftime("%m-%d-%Y-%H:%M:%S") # File Format Friendly time stamp
    users["insert_timestamp"] = now.timestamp() # This is the one that is always used
    users["filename"] = users["insert_time"] + "-" + "users.txt"

    return users
