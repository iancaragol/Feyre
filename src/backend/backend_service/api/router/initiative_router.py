import traceback

from typing import Optional
from fastapi import APIRouter
from fastapi.responses import Response
from json import dumps

from http import HTTPStatus
from backend_service.api.operation.initiative_operation import InitiativeOperation
from common.redis_helper import RedisHelper
from urllib.parse import unquote_plus

initiative_router = APIRouter()
redis_helper = RedisHelper()

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

    # Increment the init operation counter
    redis_helper.increment_command("init")

    # Add the user id to the user set
    if user:
        redis_helper.add_to_user_set(user)
    else:
        return Response(content = "Missing user query parameter", status_code = HTTPStatus.BAD_REQUEST)

    try:
        result = await InitiativeOperation(user = user, guild = guild, channel = channel, character_name = character_name, initiative_expression = initiative_expression).execute_put()
        return Response(content = result, status_code = HTTPStatus.OK)

    except Exception as e:
        result = {
                "message": f"An exception occurred when attempting the initiative operations.",
                "stack_trace": traceback.format_exc(),
                "exception_message": str(e)
            }
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

    # Increment the init operation counter
    redis_helper.increment_command("init")

    # Add the user id to the user set
    if user:
        redis_helper.add_to_user_set(user)
    else:
        return Response(content = "Missing user query parameter", status_code = HTTPStatus.BAD_REQUEST)

    try:
        result = await InitiativeOperation(user = user, guild = guild, channel = channel).execute_get()

        if result == None:
            return Response(status_code = HTTPStatus.NO_CONTENT)
        return Response(content = result, status_code = HTTPStatus.OK)

    except Exception as e:
        result = {
                "message": f"An exception occurred when attempting the initiative operations.",
                "stack_trace": traceback.format_exc(),
                "exception_message": str(e)
            }
        return Response(content = dumps(result), status_code = HTTPStatus.INTERNAL_SERVER_ERROR)

@initiative_router.patch('/api/backendservice/initiative/update')
async def initiative_patch_messageid(guild : int, channel : int, messageId : int):
    """
    Patches the message ID so that the JSON of the initiative tracker always contains the last message
    That was posted for this tracker.

    When the frontend receives a tracker JSON, it should have the messageid unless it is brand new.
    Any future initiative operations that post in the chat will cause the frontend
    to delete its old message using that message id, then post a new one

        Frontend GET Tracker ----> Backend (200 OK)
        <---- Frontend posts message
        Frontend Patch Messag ----> Backend (200 OK) 

    Query Parameters:
        guild: (int) The guild where the tracker was created
        channel: (int) The channel  where the tracker was created
        message: (int) The message id of the message that was last posted
    """

    try:
        result = await InitiativeOperation(guild = guild, channel = channel, message_id = messageId).execute_patch_message_id()

        if result == None:
            return Response(content = None, status_code = HTTPStatus.NO_CONTENT)
        return Response(content = result, status_code = HTTPStatus.OK)

    except Exception as e:
        result = {
                "message": f"An exception occurred when attempting the initiative operations.",
                "stack_trace": traceback.format_exc(),
                "exception_message": str(e)
            }
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

    # Increment the init operation counter
    redis_helper.increment_command("init")

    # Add the user id to the user set
    if user:
        redis_helper.add_to_user_set(user)
    else:
        return Response(content = "Missing user query parameter", status_code = HTTPStatus.BAD_REQUEST)

    try:
        result = await InitiativeOperation(user = user, guild = guild, channel = channel).execute_patch()

        if result == None:
            return Response(content = None, status_code = HTTPStatus.NO_CONTENT)
        return Response(content = result, status_code = HTTPStatus.OK)

    except Exception as e:
        result = {
                "message": f"An exception occurred when attempting the initiative operations.",
                "stack_trace": traceback.format_exc(),
                "exception_message": str(e)
            }
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

    # Increment the init operation counter
    redis_helper.increment_command("init")

    # Add the user id to the user set
    if user:
        redis_helper.add_to_user_set(user)
    else:
        return Response(content = "Missing user query parameter", status_code = HTTPStatus.BAD_REQUEST)

    try:
        result = await InitiativeOperation(user = user, guild = guild, channel = channel).execute_delete(character_name = character_name)
        return Response(content = result, status_code = HTTPStatus.OK)

    except Exception as e:
        result = {
                "message": f"An exception occurred when attempting the initiative operations.",
                "stack_trace": traceback.format_exc(),
                "exception_message": str(e)
            }
        return Response(content = dumps(result), status_code = HTTPStatus.INTERNAL_SERVER_ERROR)