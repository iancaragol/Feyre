from http import HTTPStatus
from flask import Blueprint, request
from backend_service.api.operation.roll_operation import RollOperation, RollOperationException
from common.redis_helper import RedisHelper

roll_api = Blueprint('roll', __name__)
redis_helper = RedisHelper()

@roll_api.route('/', methods=['GET'])
def roll():
    """
    Creates Roll Operations based on query parameters and returns a JSON object containing a list of ParentRollModels

    Query Paramters:
        verbose: (true/false) Enables print statements for that specific dice roll
        expression: (string) The Dice Expression to be rolled
    ---
    """

    # Increment the roll operation counter
    redis_helper.red.incr('c_roll', amount = 1)

    verbose = False
    args = request.args

    # Add the user id to the user set
    if "user" in args:
        user = args["user"]
        redis_helper.red.sadd("users", user)
    else:
        return "Missing user query parameter", HTTPStatus.BAD_REQUEST

    if "verbose" in args:
        verbose = bool(args["verbose"])

    # Create and exectute a Roll Operation and return the result in the response body
    if "expression" in args:
        expression = args["expression"]

        try:
            result = RollOperation(expression = expression, verbose = verbose).execute()
            return result, HTTPStatus.OK
        except RollOperationException as e:
            return e.message, HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        return "Missing expression query parameter", HTTPStatus.BAD_REQUEST