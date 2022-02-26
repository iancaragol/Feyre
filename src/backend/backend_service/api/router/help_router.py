import traceback

from fastapi import APIRouter
from fastapi.responses import Response
from json import dumps

from http import HTTPStatus
from typing import Optional
from common.redis_helper import RedisHelper
from backend_service.api.operation.help_operation import HelpOperation

help_router = APIRouter()
redis_helper = RedisHelper()

@help_router.get('/api/backendservice/help')
async def help(user : int, command : Optional[str] = None):
    """
    Returns the help string for the command

    Query Parameters:
        all: (true/false) Returns all stats instead of a subset
    """
    redis_helper.increment_command("help")

    # Add the user id to the user set
    if user:
        redis_helper.add_to_user_set(user)
    else:
        return Response(content = "Missing user query parameter", status_code = HTTPStatus.BAD_REQUEST)
    try:
        result = dumps(HelpOperation(command = command).execute())
        return Response(content = result, status_code = HTTPStatus.OK)
    except Exception as e:
        return Response(content = f"An exception occurred when getting stats.\n{e}\n{traceback.format_exc()}", status_code = HTTPStatus.INTERNAL_SERVER_ERROR)