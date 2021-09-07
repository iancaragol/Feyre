from http import HTTPStatus
from flask import Blueprint, request
from common.redis_helper import RedisHelper

sync_api = Blueprint('sync', __name__)
redis_helper = RedisHelper()

@sync_api.route('/', methods=['PUT'])
def sync():
    """
    Starts a sync operation

    ---
    """

    return "Operation completed.", HTTPStatus.OK