import traceback
import logging

from fastapi import APIRouter
from fastapi.responses import Response
from json import dumps
from fastapi.requests import Request

from http import HTTPStatus
from common.logger import LoggerNames

public_stats_router = APIRouter()
logger = logging.getLogger(LoggerNames.public_logger)

@public_stats_router.get('/public/stats')
async def stats(request: Request):
    """
    Returns the stats dictionary

    Query Parameters:
        all: (true/false) Returns all stats instead of a subset
    """
    try:
        logger.info(f"[STATS] Executing Public Metrics Stats Operation")
        result = dumps({"test":"OK"})
        logger.info(f"[STATS] StatsOperation was successful")
        return Response(content = result, status_code = HTTPStatus.OK)
    except Exception as e:
        logger.error(f"[STATS] Exception occurred in StatsOperation. Traceback: {traceback.format_exc()}")
        return Response(content = f"An exception occurred when getting stats.\n{e}\n{traceback.format_exc()}", status_code = HTTPStatus.INTERNAL_SERVER_ERROR)