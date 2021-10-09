from common import redis_keys
from json import dumps
from common.redis_helper import RedisHelper
from common.commands import Commands

class StatsOperation:
    """
    Operation to get the usage count of all commands and return it as a JSON dictionary
    """
    def __init__(self, show_all):
        self.redis_helper = RedisHelper()
        self.commands = Commands()
        self.show_all = show_all

    def execute(self):
        """
        Excutes the StatsOperation

        Returns the response body
        """
        response_body = {"stat_block": self.get_stats()}
        response_body["user_count"] = self.get_user_count()
        return response_body

    def get_stats(self):
        """
        Returns a dictionary of command counts
        """
        command_list = self.commands.commands
        if self.show_all:
            command_list = self.commands.all_commands
        return self.redis_helper.get_commands_dictionary(command_list)

    def get_user_count(self):
        """
        Returns the cardinality (count) of the user set
        """
        return self.redis_helper.get_user_set_count()
