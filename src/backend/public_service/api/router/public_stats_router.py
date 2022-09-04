import traceback
import logging

from fastapi import APIRouter
from fastapi.responses import Response, JSONResponse
from json import dumps
from fastapi.requests import Request
from pydantic import BaseModel

from http import HTTPStatus
from common.logger import LoggerNames

public_stats_router = APIRouter()
logger = logging.getLogger(LoggerNames.public_logger)

# Variable that holds the most recent stats received on the internal API
last_stats = None

class Stats(BaseModel):
    user_reach: int
    guild_total: int
    command_total: int
    user_total: int

@public_stats_router.get('/public/stats')
async def stats(request: Request):
    """
    Returns the stats dictionary
    """
    try:
        logger.info(f"[STATS] Executing Public Metrics Stats Operation")
        logger.info(f"[STATS] StatsOperation was successful")
        if last_stats != None:
            return JSONResponse(content = dumps(last_stats.dict()), status_code = HTTPStatus.OK)
        else:
            return Response(status_code=HTTPStatus.OK)
    except Exception as e:
        logger.error(f"[STATS] Exception occurred in StatsOperation. Traceback: {traceback.format_exc()}")
        return Response(content = f"An exception occurred when getting stats.\n{e}\n{traceback.format_exc()}", status_code = HTTPStatus.INTERNAL_SERVER_ERROR)

@public_stats_router.get('/public/stats/badge/guilds')
async def stats(request: Request):
    """
    Returns the user badge for Shields
    """
    try:
        logger.info(f"[STATS] Executing Public Metrics Stats Operation")
        logger.info(f"[STATS] StatsOperation was successful")
        if last_stats != None:
            badge = {
                "schemaVersion": 1,
                "label": "Servers",
                "message": last_stats.guild_total,
                "color": "success"
            }
            return JSONResponse(content = dumps(badge), status_code = HTTPStatus.OK)
        else:
            return Response(status_code=HTTPStatus.OK)
    except Exception as e:
        logger.error(f"[STATS] Exception occurred in StatsOperation. Traceback: {traceback.format_exc()}")
        return Response(content = f"An exception occurred when getting stats.\n{e}\n{traceback.format_exc()}", status_code = HTTPStatus.INTERNAL_SERVER_ERROR)

@public_stats_router.get('/public/stats/badge/commands')
async def stats(request: Request):
    """
    Returns the user badge for Shields
    """
    try:
        logger.info(f"[STATS] Executing Public Metrics Stats Operation")
        logger.info(f"[STATS] StatsOperation was successful")
        if last_stats != None:
            badge = {
                "schemaVersion": 1,
                "label": "Commands Proccessed",
                "message": last_stats.command_total,
                "color": "informational"
            }
            return JSONResponse(content = dumps(badge), status_code = HTTPStatus.OK)
        else:
            return Response(status_code=HTTPStatus.OK)
    except Exception as e:
        logger.error(f"[STATS] Exception occurred in StatsOperation. Traceback: {traceback.format_exc()}")
        return Response(content = f"An exception occurred when getting stats.\n{e}\n{traceback.format_exc()}", status_code = HTTPStatus.INTERNAL_SERVER_ERROR)

@public_stats_router.get('/public/stats/badge/users')
async def stats(request: Request):
    """
    Returns the user badge for Shields
    """
    try:
        logger.info(f"[STATS] Executing Public Metrics Stats Operation")
        logger.info(f"[STATS] StatsOperation was successful")
        if last_stats != None:
            badge = {
                "schemaVersion": 1,
                "label": "Users",
                "message": last_stats.user_total,
                "color": "success"
            }
            return JSONResponse(content = dumps(badge), status_code = HTTPStatus.OK)
        else:
            return Response(status_code=HTTPStatus.OK)
    except Exception as e:
        logger.error(f"[STATS] Exception occurred in StatsOperation. Traceback: {traceback.format_exc()}")
        return Response(content = f"An exception occurred when getting stats.\n{e}\n{traceback.format_exc()}", status_code = HTTPStatus.INTERNAL_SERVER_ERROR)

@public_stats_router.get('/public/stats/badge/reach')
async def stats(request: Request):
    """
    Returns the user badge for Shields
    """
    try:
        logger.info(f"[STATS] Executing Public Metrics Stats Operation")
        logger.info(f"[STATS] StatsOperation was successful")
        if last_stats != None:
            badge = {
                "schemaVersion": 1,
                "label": "Users",
                "message": last_stats.user_reach,
                "color": "informational"
            }
            return JSONResponse(content = dumps(badge), status_code = HTTPStatus.OK)
        else:
            return Response(status_code=HTTPStatus.OK)
    except Exception as e:
        logger.error(f"[STATS] Exception occurred in StatsOperation. Traceback: {traceback.format_exc()}")
        return

@public_stats_router.post('/internal/stats')
async def stats(stats: Stats):
    """
    Caches the stats from the frontend
    """
    try:
        logger.info(f"[STATS] Caching stats")
        global last_stats
        last_stats = stats
        return JSONResponse(content = dumps(last_stats.dict()), status_code = HTTPStatus.OK)
    except Exception as e:
        logger.error(f"[STATS] Exception occurred when caching stats. Traceback: {traceback.format_exc()}")
        return Response(content = f"An exception occurred when getting stats.\n{e}\n{traceback.format_exc()}", status_code = HTTPStatus.INTERNAL_SERVER_ERROR)