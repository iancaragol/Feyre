import datetime
import traceback

from fastapi import APIRouter
from fastapi.responses import Response
from json import dumps

from http import HTTPStatus
from backend_service.api.operation.stats_operation import StatsOperation
from common.redis_helper import RedisHelper

stats_router = APIRouter()
redis_helper = RedisHelper()

@stats_router.get('/api/backendservice/stats')
async def stats(user : str, all : bool):
    """
    Returns the stats dictionary

    Query Parameters:
        all: (true/false) Returns all stats instead of a subset
    ---
    """
    redis_helper.increment_command("stats")

    # Add the user id to the user set
    if user:
        redis_helper.add_to_user_set(user)
    else:
        return Response(content = "Missing user query parameter", status_code = HTTPStatus.BAD_REQUEST)
    try:
        result = dumps(StatsOperation(show_all = all).execute())
        return Response(content = result, status_code = HTTPStatus.OK)
    except Exception as e:
        return Response(content = f"An exception occurred when getting stats.\n{e}\n{traceback.format_exc()}", status_code = HTTPStatus.INTERNAL_SERVER_ERROR)