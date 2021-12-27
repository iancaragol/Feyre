from http import HTTPStatus

from fastapi import APIRouter
from fastapi.responses import Response
from json import dumps

from werkzeug.wrappers import response
from common.redis_helper import RedisHelper

healthcheck_router = APIRouter()
redis_helper = RedisHelper()

@healthcheck_router.get('/api/backendservice/healthcheck')
async def healthcheck(user : str):
    """
    Healthcheck endpoint
    """
    if user:
        redis_helper.add_to_user_set(user)
    else:
        return Response(content = "Missing user query parameter", status_code = HTTPStatus.BAD_REQUEST)

    response = {
        "status": 200,
        "message": "OK",
        "backend" : "Healthy",
        "redis" : redis_helper.get_redis_health()
    }

    return Response(content = dumps(response), status_code = HTTPStatus.OK)