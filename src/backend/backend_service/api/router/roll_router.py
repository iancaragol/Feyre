import traceback
import logging

from fastapi import APIRouter
from fastapi.responses import Response
from json import dumps

from http import HTTPStatus
from backend_service.api.operation.roll_operation import RollOperation, RollOperationException
from common.redis_helper import RedisHelper
from common.logger import LoggerNames
from urllib.parse import unquote_plus

roll_router = APIRouter()
redis_helper = RedisHelper()
logger = logging.getLogger(LoggerNames.backend_logger)

@roll_router.get('/api/backendservice/roll')
async def roll(user : int, expression : str, verbose : bool = False):
    """
    Creates Roll Operations based on query parameters and returns a JSON object containing a list of ParentRollModels

    Query Parameters:
        verbose: (true/false) Enables print statements for that specific dice roll
        expression: (string) The Dice Expression to be rolled
        user: (int) The user who rolled the dice
    """

    logger.info(f"[ROLL] Received roll request. user: {user}, expression: {expression}, verbose: {verbose}")

    # Increment the roll operation counter
    redis_helper.increment_command("roll")

    # Add the user id to the user set
    if user:
        redis_helper.add_to_user_set(user)
    else:
        logger.error(f"[ROLL] Roll request is missing user parameter. user: {user}, expression: {expression}, verbose: {verbose}")
        return Response(content = "Missing user query parameter", status_code = HTTPStatus.BAD_REQUEST)

    # Create and exectute a Roll Operation and return the result in the response body
    if expression:
        try:
            logger.info(f"[ROLL] Executing RollOperation. expression: {expression}")
            result = await RollOperation(expression = expression, verbose = verbose).execute()
            logger.info(f"[ROLL] RollOperation was successful. expression: {expression}")
            return Response(content = result, status_code = HTTPStatus.OK)

        except RollOperationException as e:
            result = {
                    "message": f"An exception occurred when attempting the roll operation with expression = {unquote_plus(expression)}.",
                    "stack_trace": traceback.format_exc(),
                    "exception_message": e.message,
                    "expression": expression,
                    "is_expected" : e.is_expected
                }

            if not e.is_expected:
                logger.error(f"[ROLL] Exception occurred in RollOperation with user: {user}, expression: {expression}, verbose: {verbose}. Exception Message: {e.message}. Traceback: {traceback.format_exc()}")
            else:
                logger.info(f"[ROLL] Expected exception occurred in RollOperation with user: {user}, expression: {expression}, verbose: {verbose}. Exception Message: {e.message}")

            return Response(content = dumps(result), status_code = HTTPStatus.INTERNAL_SERVER_ERROR)
    else:
        logger.error(f"[ROLL] Roll request is missing expression parameter. user: {user}, expression: {expression}, verbose: {verbose}")
        return Response(content = "Missing expression query parameter", status_code = HTTPStatus.BAD_REQUEST)