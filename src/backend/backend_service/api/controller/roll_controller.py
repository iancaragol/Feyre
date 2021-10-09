import traceback

from datetime import datetime
from http import HTTPStatus
from flask import Blueprint, request, make_response, jsonify
from backend_service.api.operation.roll_operation import RollOperation, RollOperationException
from common.redis_helper import RedisHelper

roll_api = Blueprint('roll_api', __name__)
redis_helper = RedisHelper()

@roll_api.route('/', methods=['GET'])
def roll():
    """
    Creates Roll Operations based on query parameters and returns a JSON object containing a list of ParentRollModels

    Query Parameters:
        verbose: (true/false) Enables print statements for that specific dice roll
        expression: (string) The Dice Expression to be rolled
    ---
    """

    # Increment the roll operation counter
    redis_helper.increment_command("roll")

    verbose = False
    args = request.args

    # Add the user id to the user set
    if "user" in args:
        user = args["user"]
        redis_helper.add_to_user_set(user)
    else:
        return make_response("Missing user query parameter", HTTPStatus.BAD_REQUEST)

    if "verbose" in args:
        verbose = bool(args["verbose"])

    # Create and exectute a Roll Operation and return the result in the response body
    if "expression" in args:
        expression = args["expression"]

        try:
            result = RollOperation(expression = expression, verbose = verbose).execute()
            return make_response(result, HTTPStatus.OK)

        except RollOperationException as e:
            return make_response(f"An exception occurred when attempting the roll operation with expression = {expression}.\n{e}\n{traceback.format_exc()}", HTTPStatus.INTERNAL_SERVER_ERROR)
    else:
        return make_response("Missing expression query parameter", HTTPStatus.BAD_REQUEST)