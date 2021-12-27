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
        self.show_all = show_all

    def execute(self):
        """
        Excutes the StatsOperation

        Returns the response body
        """
        response_body = self.get_stats()
        response_body["user_count"] = self.get_user_count()
        return response_body

    def get_stats(self):
        """
        Returns a dictionary of command counts
        """
        command_list = Commands.default_commands_list
        if self.show_all:
            command_list = Commands.all_commands_list
        stats_dict = self.redis_helper.get_commands_dictionary(command_list)
        stats_dict = self.add_stats_message(stats_dict)
        return stats_dict

    def add_stats_message(self, stats_dict):
        message = "```asciidoc\n[Statistics]\n"
        for k, v in stats_dict.items():
            message += f"\n{k}: {v}"
        stats_dict["message"] = message + "```"
        return stats_dict

    def get_user_count(self):
        """
        Returns the cardinality (count) of the user set
        """
        return self.redis_helper.get_user_set_count()
