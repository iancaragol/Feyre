import redis

from datetime import datetime
from os import environ
from common.redis_keys import RedisKeys

if environ.get('ENV_KUBE', None) == 'True':
    HOST = 'redis.redis'
else:
    HOST = 'redis-primary'

class RedisHelper:
    """
    Common class shared across Backend and Sync services

    Provides a set of helper functions to ensure consistency when accessing Redis. Any calls made to Redis should be written as functions here.
    """
    def __init__(self):
        redis_pw = ""
        if environ['REDIS_PASSWORD']:
            redis_pw = environ['REDIS_PASSWORD']

        self.red = redis.StrictRedis(host=HOST, port=6379, db=0, password=redis_pw)
        self.keys = RedisKeys()

    def increment_command(self, command):
        updated_time = datetime.now().timestamp()
        self.red.incr(f"c_{command}", amount = 1)
        self.red.set(f"c_:{self.keys.updated_time}", updated_time)
        return updated_time

    def get_commands_dictionary(self, command_list):
        """
        Returns a dictionary of command counts

        Parameter:
            command_list: The list of commands to check
        """
        stats_dict = {}
        prefix = self.keys.command_prefix
        for command in command_list:
            val = self.red.get(f"{prefix}{command}")
            if val:
                stats_dict[command] = int(val.decode("utf-8"))
        return stats_dict

    def get_user_set(self):
        """
        Returns the user_set as a list
        """
        return [int(u) for u in self.red.smembers(self.keys.user_set)]

    def get_user_set_count(self):
        """
        Returns the count (cardinality) of the user set
        """
        return int(self.red.scard(self.keys.user_set))

    def get_user_set_timestamp(self):
        """
        Returns the timestamp for the user set's last update time
        """
        return float(self.red.get(f"{self.keys.user_set}:{self.keys.updated_time}"))

    def get_user_set_timestamp_as_datetime(self):
        """
        Returns the datetime for the user set's last update time
        """
        return datetime.fromtimestamp(self.get_user_set_timestamp())
    
    def add_to_user_set(self, *value):
        """
        Adds value(s) to the user_set and updates the last update time

        Returns the new update time
        """
        updated_time = datetime.now().timestamp()
        self.red.sadd(self.keys.user_set, *value)
        self.red.set(f"{self.keys.user_set}:{self.keys.updated_time}", updated_time)
        return updated_time
