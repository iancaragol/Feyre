import traceback
import logging

from typing import Optional
from fastapi import APIRouter
from fastapi.responses import Response
from json import dumps

from http import HTTPStatus

from backend_service.api.operation.initiative_operation import InitiativeOperation
from common.redis_helper import RedisHelper
from urllib.parse import unquote_plus
from common.logger import LoggerNames


initiative_router = APIRouter()
redis_helper = RedisHelper()
logger = logging.getLogger(LoggerNames.backend_logger)

@initiative_router.put('/api/backendservice/initiative')
async def initiative_put(user : int, guild : int, channel : int, character_name : Optional[str] = None, initiative_expression : Optional[str] = None):
    """
    Updates or creates a new initiative tracker object in the guild channel.

    If no tracker exists, then create it

    If a tracker exists, then update it

    When Creating/Updating check user DB for active character or use the provided character name and modifier

    Query Parameters:
        user: (int) The user who used the command
        guild: (int) The guild in which to create the tracker
        channel: (int) The channel in which to create the tracker
        character: (str) (optional) The name of the character to add
        init_mod: (str) (optional) The modifier to roll with
    """

    logger.info(f"[INIT > PUT] Received Initiative PUT request. user: {user}, guild: {guild}, channel: {channel}, character_name: {character_name}, initiative_expression: {initiative_expression}")

    # Increment the init operation counter
    redis_helper.increment_command("init")

    # Add the user id to the user set
    if user:
        redis_helper.add_to_user_set(user)
    else:
        logger.error(f"[INIT > PUT] Init request is missing user parameter. user: {user}, guild: {guild}, channel: {channel}, character_name: {character_name}, initiative_expression: {initiative_expression}")
        return Response(content = "Missing user query parameter", status_code = HTTPStatus.BAD_REQUEST)

    try:
        logger.info(f"[INIT > PUT] Executing InitiativeOperation. user: {user}, guild: {guild}, channel: {channel}, character_name: {character_name}, initiative_expression: {initiative_expression}")
        result = await InitiativeOperation(user = user, guild = guild, channel = channel, character_name = character_name, initiative_expression = initiative_expression).execute_put()
        logger.info(f"[INIT > PUT] InitiativeOperation was successful.")
        return Response(content = result, status_code = HTTPStatus.OK)

    except Exception as e:
        result = {
                "message": f"An exception occurred when attempting the initiative operations.",
                "stack_trace": traceback.format_exc(),
                "exception_message": str(e)
            }
        logger.error(f"[INIT > PUT] Exception occurred in InitiativeOpeartion with user: {user}, guild: {guild}, channel: {channel}, character_name: {character_name}, initiative_expression: {initiative_expression}. Exception Message: {str(e)}. Traceback: {traceback.format_exc()}")
        return Response(content = dumps(result), status_code = HTTPStatus.INTERNAL_SERVER_ERROR)

@initiative_router.get('/api/backendservice/initiative')
async def initiative_get(user : int, guild : int, channel):
    """
    Returns the initiative tracker.

    Query Parameters:
        user: (int) The user who used the command
        guild: (int) The guild where the tracker was created
        channel: (int) The channel  where the tracker was created
    """

    logger.info(f"[INIT > GET] Received Initiative GET request. user: {user}, guild: {guild}, channel: {channel}")

    # Increment the init operation counter
    redis_helper.increment_command("init")

    # Add the user id to the user set
    if user:
        redis_helper.add_to_user_set(user)
    else:
        logger.error(f"[INIT > GET] Init request is missing user parameter. user: {user}, guild: {guild}, channel: {channel}")
        return Response(content = "Missing user query parameter", status_code = HTTPStatus.BAD_REQUEST)

    try:
        logger.info(f"[INIT > GET] Executing InitiativeOperation. user: {user}, guild: {guild}, channel: {channel}")
        result = await InitiativeOperation(user = user, guild = guild, channel = channel).execute_get()
        if result == None:
            logger.info(f"[INIT > GET] InitiativeTracker does not exist in guild {guild}, channel {channel}")
            return Response(status_code = HTTPStatus.NO_CONTENT)
        logger.info(f"[INIT > GET] InitiativeOperation was successful")
        return Response(content = result, status_code = HTTPStatus.OK)

    except Exception as e:
        result = {
                "message": f"An exception occurred when attempting the initiative operations.",
                "stack_trace": traceback.format_exc(),
                "exception_message": str(e)
            }
        logger.error(f"[INIT > GET] Exception occurred in InitiativeOpeartion with user: {user}, guild: {guild}, channel: {channel}, Exception Message: {str(e)}. Traceback: {traceback.format_exc()}")
        return Response(content = dumps(result), status_code = HTTPStatus.INTERNAL_SERVER_ERROR)

@initiative_router.patch('/api/backendservice/initiative/update')
async def initiative_patch_messageid(guild : int, channel : int, message_id : int):
    """
    Patches the message ID so that the JSON of the initiative tracker always contains the last message
    That was posted for this tracker.

    When the frontend receives a tracker JSON, it should have the messageid unless it is brand new.
    Any future initiative operations that post in the chat will cause the frontend
    to delete its old message using that message id, then post a new one

        Frontend GET Tracker ----> Backend (200 OK)
        <---- Frontend posts message
        Frontend Patch Message ----> Backend (200 OK) 

    Query Parameters:
        guild: (int) The guild where the tracker was created
        channel: (int) The channel  where the tracker was created
        message: (int) The message id of the message that was last posted
    """

    logger.info(f"[INIT > PATCH] Received Initiative PATCH ID request. guild: {guild}, channel: {channel}, message_id: {message_id}")

    try:
        logger.info(f"[INIT > PATCH] Executing InitiativeOperation. guild: {guild}, channel: {channel}, message_id: {message_id}")
        result = await InitiativeOperation(guild = guild, channel = channel, message_id = message_id).execute_patch_message_id()
        logger.info(f"[INIT > PATCH] InitiativeOperation was successful.")

        if result == None:
            logger.info(f"[INIT > PATCH] InitiativeTracker does not exist in guild {guild}, channel {channel}")
            return Response(content = None, status_code = HTTPStatus.NO_CONTENT)
        return Response(content = result, status_code = HTTPStatus.OK)

    except Exception as e:
        result = {
                "message": f"An exception occurred when attempting the initiative operations.",
                "stack_trace": traceback.format_exc(),
                "exception_message": str(e)
            }
        logger.error(f"[INIT > GET] Exception occurred in InitiativeOpeartion with guild: {guild}, channel: {channel}, message_id: {message_id}, Exception Message: {str(e)}. Traceback: {traceback.format_exc()}")
        return Response(content = dumps(result), status_code = HTTPStatus.INTERNAL_SERVER_ERROR)

@initiative_router.patch('/api/backendservice/initiative')
async def initiative_patch(user : int, guild : int, channel):
    """
    Updates the turn order by incrementing turn value by one

    Query Parameters:
        user: (int) The user who used the command
        guild: (int) The guild where the tracker was created
        channel: (int) The channel  where the tracker was created
    """

    logger.info(f"[INIT > PATCH] Received Initiative PATCH request. user: {user}, guild: {guild}, channel: {channel}")

    # Increment the init operation counter
    redis_helper.increment_command("init")

    # Add the user id to the user set
    if user:
        redis_helper.add_to_user_set(user)
    else:
        logger.error(f"[INIT > PATCH] Init request is missing user parameter. user: {user}, guild: {guild}, channel: {channel}")
        return Response(content = "Missing user query parameter", status_code = HTTPStatus.BAD_REQUEST)

    try:
        logger.info(f"[INIT > PATCH] Executing InitiativeOperation. user: {user}, guild: {guild}, channel: {channel}")
        result = await InitiativeOperation(user = user, guild = guild, channel = channel).execute_patch()

        if result == None:
            logger.info(f"[INIT > PATCH] InitiativeTracker does not exist in guild {guild}, channel {channel}")
            return Response(content = None, status_code = HTTPStatus.NO_CONTENT)
        logger.info(f"[INIT > PATCH] InitiativeOperation was successful")
        return Response(content = result, status_code = HTTPStatus.OK)

    except Exception as e:
        result = {
                "message": f"An exception occurred when attempting the initiative operations.",
                "stack_trace": traceback.format_exc(),
                "exception_message": str(e)
            }
        logger.error(f"[INIT > GET] Exception occurred in InitiativeOpeartion with user: {user}, guild: {guild}, channel: {channel}, Exception Message: {str(e)}. Traceback: {traceback.format_exc()}")
        return Response(content = dumps(result), status_code = HTTPStatus.INTERNAL_SERVER_ERROR)

@initiative_router.delete('/api/backendservice/initiative')
async def initiative_delete(user : int, guild : int, channel, character_name : Optional[str] = None):
    """
    Delets the initiative tracker

    Query Parameters:
        user: (int) The user who used the command
        guild: (int) The guild where the tracker was created
        channel: (int) The channel  where the tracker was created
    """

    logger.info(f"[INIT > DELETE] Received Initiative DELETE request. user: {user}, guild: {guild}, channel: {channel}, character_name: {character_name}")

    # Increment the init operation counter
    redis_helper.increment_command("init")

    # Add the user id to the user set
    if user:
        redis_helper.add_to_user_set(user)
    else:
        logger.error(f"[INIT > DELETE] Init request is missing user parameter. user: {user}, guild: {guild}, channel: {channel}, character_name: {character_name}")
        return Response(content = "Missing user query parameter", status_code = HTTPStatus.BAD_REQUEST)

    try:
        logger.info(f"[INIT > DELETE] Executing InitiativeOperation. user: {user}, guild: {guild}, channel: {channel}, character_name: {character_name}")
        result = await InitiativeOperation(user = user, guild = guild, channel = channel).execute_delete(character_name = character_name)
        logger.info(f"[INIT > DELETE] InitiativeOperation was successful")
        return Response(content = result, status_code = HTTPStatus.OK)

    except Exception as e:
        result = {
                "message": f"An exception occurred when attempting the initiative operations.",
                "stack_trace": traceback.format_exc(),
                "exception_message": str(e)
            }
        logger.error(f"[INIT > DELETE] Exception occurred in InitiativeOpeartion with user: {user}, guild: {guild}, channel: {channel}, character_name: {character_name}, Exception Message: {str(e)}. Traceback: {traceback.format_exc()}")
        return Response(content = dumps(result), status_code = HTTPStatus.INTERNAL_SERVER_ERROR)