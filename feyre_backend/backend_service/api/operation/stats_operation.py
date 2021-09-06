from json import dumps
from backend_service.api.model.stats_model import StatsModel

class StatsOperation:
    def __init__(self, redis, show_all):
        self.red = redis
        self.show_all = show_all

    def execute(self):
        response_body = {"commands": self.get_stats()}
        response_body["user_count"] = self.get_user_count()
        return dumps(response_body)

    def get_stats(self):
        stats_model = StatsModel()

        command_list = stats_model.commands
        if self.show_all:
            command_list = stats_model.all_commands

        for command in command_list:
            val = self.red.get(command)
            if val:
                stats_model.stats_dict[command] = int(val.decode("utf-8"))

        return stats_model.stats_dict

    def get_user_count(self):
        """
        Returns the cardinality (count) of the user set

        https://redis.io/commands/scard
        """
        return int(self.red.scard("users"))
