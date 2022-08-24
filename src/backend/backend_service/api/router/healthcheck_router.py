from sys import excepthook
import traceback
import logging

from http import HTTPStatus

from fastapi import APIRouter
from fastapi.responses import Response
from json import dumps

from werkzeug.wrappers import response
from common.redis_helper import RedisHelper
from common.logger import LoggerNames

healthcheck_router = APIRouter()
redis_helper = RedisHelper()
logger = logging.getLogger(LoggerNames.backend_logger)

@healthcheck_router.get('/api/backendservice/healthcheck')
async def healthcheck(user : int):
    """
    Healthcheck endpoint
    """

    logger.info(f"[HEALTH] Received Health request. user: {user}")

    if user:
        redis_helper.add_to_user_set(user)
    else:
        logger.error(f"[HEALTH] Health request is missing user parameter. user: {user}")
        return Response(content = "Missing user query parameter", status_code = HTTPStatus.BAD_REQUEST)

    try:
        logger.info(f"[HEALTH] Getting RedisHealth. user: {user}")
        response = {
            "status": 200,
            "message": "OK",
            "backend" : "Healthy",
            "redis" : redis_helper.get_redis_health()
        }
        return Response(content = dumps(response), status_code = HTTPStatus.OK)
    except Exception as e:
        logger.error(f"[HEALTH] ExceptionOccurred when getting Health. user: {user}. Exception Message: {str(e)}. Traceback: {traceback.format_exc()}")
        return Response(content = f"An exception occurred when getting health.\n{e}\n{traceback.format_exc()}", status_code = HTTPStatus.INTERNAL_SERVER_ERROR)
