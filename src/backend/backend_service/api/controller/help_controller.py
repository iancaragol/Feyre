import traceback
import json

from http import HTTPStatus
from flask import Blueprint, make_response, jsonify, request
from werkzeug.wrappers import response
from common.redis_helper import RedisHelper
from backend_service.api.operation.help_operation import HelpOperation

help_api = Blueprint('help_api', __name__)
redis_helper = RedisHelper()

@help_api.route('/', methods=['GET'])
def help():
    """
    Returns the stats dictionary

    Query Parameters:
        all: (true/false) Returns all stats instead of a subset
    ---
    """
    redis_helper.increment_command("help")

    show_all = False
    args = request.args

    # Add the user id to the user set
    if "user" in args:
        user = args["user"]
        redis_helper.add_to_user_set(user)
    else:
        return make_response("Missing user query parameter", HTTPStatus.BAD_REQUEST)

    if "command" in args:
        command = str(args["command"])
    else:
        command = None
    try:
        result = HelpOperation(command = command).execute()
        return make_response(result, HTTPStatus.OK)
    except Exception as e:
        return make_response(f"An exception occurred when getting stats.\n{e}\n{traceback.format_exc()}", HTTPStatus.INTERNAL_SERVER_ERROR)