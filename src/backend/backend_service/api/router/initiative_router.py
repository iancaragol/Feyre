import traceback

from fastapi import APIRouter
from fastapi.responses import Response
from json import dumps

from http import HTTPStatus
from backend_service.api.operation.roll_operation import RollOperation, RollOperationException
from common.redis_helper import RedisHelper
from urllib.parse import unquote_plus

initiative_router = APIRouter()
redis_helper = RedisHelper()

@initiative_router.put('/api/backendservice/initiative')
async def initiative_put(user : int, guild : int, channel : int, character = None : str, init_mod = None : str):
    """
    Updates or creates a new initiative tracker object in the guild channel.

    If no tracker exists, then create it

    If a tracker exists, then update it

    When Creating/Updating check user DB for active character or use the provided character name and modifier

    Query Parameters:
        user: (int) The user who used the command
        guild: (int) The guild in which to create the tracker
        channel: (int) The channel in which to create the tracker
        character: (str) (optional) The name of the character to add
        init_mod: (str) (optional) The modifier to roll with
    """

    # Increment the init operation counter
    redis_helper.increment_command("init")

    # Add the user id to the user set
    if user:
        redis_helper.add_to_user_set(user)
    else:
        return Response(content = "Missing user query parameter", status_code = HTTPStatus.BAD_REQUEST)

    try:
        result = InitiativeOperation(user = user, guild = guild, channel = channel, character = character, init_mod = init_mod)
        return Response(content = result, status_code = HTTPStatus.OK)

    except Exception as e:
        result = {
                "message": f"An exception occurred when attempting the initiative operations.",
                "stack_trace": traceback.format_exc(),
                "exception_message": e.message
            }
        return Response(content = dumps(result), status_code = HTTPStatus.INTERNAL_SERVER_ERROR)