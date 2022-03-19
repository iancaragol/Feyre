import traceback

from typing import Optional
from fastapi import APIRouter
from fastapi.responses import Response
from json import dumps

from http import HTTPStatus
from backend_service.api.operation.character_operation import CharacterOperation
from common.redis_helper import RedisHelper
from urllib.parse import unquote_plus

character_router = APIRouter()
redis_helper = RedisHelper()

@character_router.get('/api/backendservice/character')
async def character_get(user : int):
    """
    Gets all character's for the user

    Query Parameters:
        user: (int) The user who used the command
    """

    # Increment the init operation counter
    redis_helper.increment_command("char")

    # Add the user id to the user set
    if user:
        redis_helper.add_to_user_set(user)
    else:
        return Response(content = "Missing user query parameter", status_code = HTTPStatus.BAD_REQUEST)

    try:
        result = await CharacterOperation(user = user).execute_get()

        if result == None:
            return Response(status_code = HTTPStatus.NO_CONTENT)
        return Response(content = result, status_code = HTTPStatus.OK)

    except Exception as e:
        result = {
                "message": f"An exception occurred when attempting the character operations.",
                "stack_trace": traceback.format_exc(),
                "exception_message": str(e)
            }
        return Response(content = dumps(result), status_code = HTTPStatus.INTERNAL_SERVER_ERROR)