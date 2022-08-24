import traceback
import logging

from fastapi import APIRouter
from fastapi.responses import Response
from json import dumps

from http import HTTPStatus
from backend_service.api.operation.stats_operation import StatsOperation
from common.redis_helper import RedisHelper
from common.logger import LoggerNames

stats_router = APIRouter()
redis_helper = RedisHelper()
logger = logging.getLogger(LoggerNames.backend_logger)

@stats_router.get('/api/backendservice/stats')
async def stats(user : int, all : bool = True):
    """
    Returns the stats dictionary

    Query Parameters:
        all: (true/false) Returns all stats instead of a subset
    """
    logger.info(f"[STATS] Received stats request. user: {user}, all: {all}")

    redis_helper.increment_command("stats")

    # Add the user id to the user set
    if user:
        redis_helper.add_to_user_set(user)
    else:
        logger.error(f"[STATS] Stats request is missing user parameter. user: {user}, all: {all}")
        return Response(content = "Missing user query parameter", status_code = HTTPStatus.BAD_REQUEST)
    try:
        logger.info(f"[STATS] Executing StatsOperation")
        result = dumps(StatsOperation(show_all = all).execute())
        logger.info(f"[STATS] StatsOperation was successful")
        return Response(content = result, status_code = HTTPStatus.OK)
    except Exception as e:
        logger.error(f"[STATS] Exception occurred in StatsOperation. Traceback: {traceback.format_exc()}")
        return Response(content = f"An exception occurred when getting stats.\n{e}\n{traceback.format_exc()}", status_code = HTTPStatus.INTERNAL_SERVER_ERROR)