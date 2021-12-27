from common import redis_keys
from json import dumps
from common.redis_helper import RedisHelper
from common.commands import Commands

class HelpOperation:
    """
    Operation to get the help message for each command
    """
    def __init__(self, command):
        self.redis_helper = RedisHelper()
        self.command = command

    def execute(self):
        """
        Excutes the HelpOperation

        Returns the response body
        """
        response_body = {}
        response_body['message'] = self.get_help_message(command = self.command)
        return response_body

    def get_help_message(self, command : str):
        if command == "roll":
            return "Roll Help string!"
        else:
            return "No filter provided!"
