import traceback
import logging

from fastapi import APIRouter
from fastapi.responses import Response
from json import dumps

from http import HTTPStatus
from typing import Optional
from common.redis_helper import RedisHelper
from backend_service.api.operation.help_operation import HelpOperation
from common.logger import LoggerNames

help_router = APIRouter()
redis_helper = RedisHelper()
logger = logging.getLogger(LoggerNames.backend_logger)

@help_router.get('/api/backendservice/help')
async def help(user : int, command : Optional[str] = None):
    """
    Returns the help string for the command

    Query Parameters:
        all: (true/false) Returns all stats instead of a subset
    """

    logger.info(f"[HELP] Received Help request. user: {user}, command: {command}")

    redis_helper.increment_command("help")

    # Add the user id to the user set
    if user:
        redis_helper.add_to_user_set(user)
    else:
        logger.error(f"[HELP] Help request is missing user parameter. user: {user}, command: {command}")
        return Response(content = "Missing user query parameter", status_code = HTTPStatus.BAD_REQUEST)
    try:
        logger.info(f"[HELP] Executing HelpOperation. user: {user}, command: {command}")
        result = dumps(HelpOperation(command = command).execute())
        logger.info(f"[HELP] HelpOperation was successful.")
        return Response(content = result, status_code = HTTPStatus.OK)
    except Exception as e:
        logger.error(f"[HELP] ExceptionOccurred in HelpOperation. user: {user}, command: {command}. Exception Message: {str(e)}. Traceback: {traceback.format_exc()}")
        return Response(content = f"An exception occurred when getting stats.\n{e}\n{traceback.format_exc()}", status_code = HTTPStatus.INTERNAL_SERVER_ERROR)