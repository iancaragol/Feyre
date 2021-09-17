import datetime
import traceback

from http import HTTPStatus
from flask import Blueprint, request
from backend_service.api.operation.stats_operation import StatsOperation
from common.redis_helper import RedisHelper

stats_api = Blueprint('stats', __name__)
redis_helper = RedisHelper()

@stats_api.route('/', methods=['GET'])
def stats():
    """
    Returns the stats dictionary

    Query Parameters:
        all: (true/false) Returns all stats instead of a subset
    ---
    """
    redis_helper.increment_command("stats")

    show_all = False
    args = request.args

    # Add the user id to the user set
    if "user" in args:
        user = args["user"]
        redis_helper.add_to_user_set(user)
    else:
        return "Missing user query parameter", HTTPStatus.BAD_REQUEST

    if "all" in args:
        show_all = bool(args["all"])
    try:
        result = StatsOperation(show_all = show_all).execute()
        return result, HTTPStatus.OK
    except Exception as e:
        return f"An exception occurred when getting stats.\n{e}\n{traceback.format_exc()}", HTTPStatus.INTERNAL_SERVER_ERROR
    