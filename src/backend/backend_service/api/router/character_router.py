import traceback
import logging

from typing import Optional
from fastapi import APIRouter
from fastapi.responses import Response
from json import dumps

from http import HTTPStatus
from backend_service.api.operation.character_operation import CharacterOperation
from common.redis_helper import RedisHelper
from urllib.parse import unquote_plus
from common.logger import LoggerNames

character_router = APIRouter()
redis_helper = RedisHelper()
logger = logging.getLogger(LoggerNames.backend_logger)

@character_router.get('/api/backendservice/character')
async def character_get(user : int):
    """
    Gets all character's for the user

    Query Parameters:
        user: (int) The user who used the command
    """

    logger.info(f"[CHAR > GET] Received Character GET request. user: {user}")

    # Increment the init operation counter
    redis_helper.increment_command("char")

    # Add the user id to the user set
    if user:
        redis_helper.add_to_user_set(user)
    else:
        logger.error(f"[CHAR > GET] Char request is missing user parameter. user: {user}")
        return Response(content = "Missing user query parameter", status_code = HTTPStatus.BAD_REQUEST)

    try:
        logger.info(f"[CHAR > GET] Executing CharacterOperation. user: {user}")
        result = await CharacterOperation(user = user).execute_get()

        if result == None:
            logger.info(f"[CHAR > GET] User {user} does not have any characters.")
            return Response(status_code = HTTPStatus.NO_CONTENT)
        logger.info(f"[CHAR > GET] CharacterOperation was successful.")
        return Response(content = result, status_code = HTTPStatus.OK)

    except Exception as e:
        result = {
                "message": f"An exception occurred when attempting the character operations.",
                "stack_trace": traceback.format_exc(),
                "exception_message": str(e)
            }
        logger.error(f"[CHAR > GET] Exception occurred in CharacterOperation with user: {user}. Exception Message: {str(e)}. Traceback: {traceback.format_exc()}")
        return Response(content = dumps(result), status_code = HTTPStatus.INTERNAL_SERVER_ERROR)

@character_router.patch('/api/backendservice/character')
async def character_patch(user : int, character_id : int):
    """
    Gets all character's for the user

    Query Parameters:
        user: (int) The user who used the command
    """

    logger.info(f"[CHAR > PATCH] Received Character PATCH request. user: {user}, character_id: {character_id}")

    # Increment the init operation counter
    redis_helper.increment_command("char")

    # Add the user id to the user set
    if user:
        redis_helper.add_to_user_set(user)
    else:
        logger.error(f"[CHAR > PATCH] Char request is missing user parameter. user: {user}")
        return Response(content = "Missing user query parameter", status_code = HTTPStatus.BAD_REQUEST)

    try:
        logger.info(f"[CHAR > PATCH] Executing CharacterOperation. user: {user}, character_id: {character_id}")
        result = await CharacterOperation(user = user, character_id = character_id).execute_patch()

        if result == None:
            logger.info(f"[CHAR > PATCH] User {user} does not have any characters.")
            return Response(status_code = HTTPStatus.NO_CONTENT)
        logger.info(f"[CHAR > PATCH] CharacterOperation was successful.")
        return Response(content = result, status_code = HTTPStatus.OK)

    except Exception as e:
        result = {
                "message": f"An exception occurred when attempting the character operations.",
                "stack_trace": traceback.format_exc(),
                "exception_message": str(e)
            }

        logger.error(f"[CHAR > PATCH] Exception occurred in CharacterOperation with user: {user}, character_id: {character_id}. Exception Message: {str(e)}. Traceback: {traceback.format_exc()}")
        return Response(content = dumps(result), status_code = HTTPStatus.INTERNAL_SERVER_ERROR)

@character_router.put('/api/backendservice/character')
async def character_put(user : int, character_name : str, initiative_expression : str):
    """
    Gets all character's for the user

    Query Parameters:
        user: (int) The user who used the command
    """

    logger.info(f"[CHAR > PATCH] Received Character PATCH request. user: {user}, character_name: {character_name}, initiative_expression: {initiative_expression}")

    # Increment the init operation counter
    redis_helper.increment_command("char")

    # Add the user id to the user set
    if user:
        redis_helper.add_to_user_set(user)
    else:
        logger.error(f"[CHAR > PATCH] Char request is missing user parameter. user: {user}")
        return Response(content = "Missing user query parameter", status_code = HTTPStatus.BAD_REQUEST)

    try:
        logger.info(f"[CHAR > PATCH] Executing PatchOperation. user: {user}, character_name: {character_name}, initiative_expression: {initiative_expression}")
        result = await CharacterOperation(user = user, character_name = character_name, init_mod = initiative_expression).execute_put()

        if result == None:
            logger.info(f"[CHAR > PATCH] User {user} does not have any characters.")
            return Response(status_code = HTTPStatus.NO_CONTENT)

        logger.info(f"[CHAR > PATCH] CharacterOperation was successful.")
        return Response(content = result, status_code = HTTPStatus.OK)

    except Exception as e:
        result = {
                "message": f"An exception occurred when attempting the character operations.",
                "stack_trace": traceback.format_exc(),
                "exception_message": str(e)
            }

        logger.error(f"[CHAR > PATCH] Exception occurred in CharacterOperation with user: {user}, character_name: {character_name}, initiative_expression: {initiative_expression}. Exception Message: {str(e)}. Traceback: {traceback.format_exc()}")
        return Response(content = dumps(result), status_code = HTTPStatus.INTERNAL_SERVER_ERROR)

@character_router.delete('/api/backendservice/character')
async def character_delete(user : int, character_id : int):
    """
    Removes the character with character_id

    Query Parameters:
        user: (int) The user who used the command
        character_id: (int) The character to remove
    """

    logger.info(f"[CHAR > DELETE] Received Character DELETE request. user: {user}, character_id: {character_id}")

    # Increment the init operation counter
    redis_helper.increment_command("char")

    # Add the user id to the user set
    if user:
        redis_helper.add_to_user_set(user)
    else:
        logger.error(f"[CHAR > DELETE] Char request is missing user parameter. user: {user}")
        return Response(content = "Missing user query parameter", status_code = HTTPStatus.BAD_REQUEST)

    try:
        logger.info(f"[CHAR > DELETE] Executing CharacterOperation. user: {user}, character_id: {character_id}")
        result = await CharacterOperation(user = user, character_id = character_id).execute_delete()

        if result == None:
            logger.info(f"[CHAR > DELETE] User {user} does not have any characters.")
            return Response(status_code = HTTPStatus.NO_CONTENT)
        logger.info(f"[CHAR > DELETE] CharacterOperation was successful.")
        return Response(content = result, status_code = HTTPStatus.OK)

    except Exception as e:
        result = {
                "message": f"An exception occurred when attempting the character operations.",
                "stack_trace": traceback.format_exc(),
                "exception_message": str(e)
            }
        logger.error(f"[CHAR > DELETE] Exception occurred in CharacterOperation with user: {user}, character_id: {character_id}. Exception Message: {str(e)}. Traceback: {traceback.format_exc()}")
        return Response(content = dumps(result), status_code = HTTPStatus.INTERNAL_SERVER_ERROR)