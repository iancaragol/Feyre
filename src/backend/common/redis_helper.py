import redis

from datetime import datetime
from os import environ
from common.commands import Commands
from common.redis_keys import RedisKeys

if environ.get('ENV_KUBE', None) == 'true':
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

    def increment_command(self, command):
        updated_time = datetime.now().timestamp()
        self.red.incr(f"{RedisKeys.command_prefix}:{command}", amount = 1)
        self.red.incr(f"{RedisKeys.command_prefix}:total", amount = 1)
        self.red.set(f"{RedisKeys.command_counts}:{RedisKeys.updated_time}", updated_time)
        return updated_time

    def get_commands_dictionary(self, command_list):
        """
        Returns a dictionary of command counts

        Parameter:
            command_list: The list of commands to check
        """
        stats_dict = {}
        prefix = RedisKeys.command_prefix
        for command in command_list:
            val = self.red.get(f"{prefix}:{command}")
            if val:
                stats_dict[command] = int(val.decode("utf-8"))
        total = int(self.red.get(f"{prefix}:total").decode("utf-8"))
        stats_dict["total"] = total
        return stats_dict

    def set_commands_dictionary(self, commands_dictionary):
        prefix = RedisKeys.command_prefix
        for k, v in commands_dictionary.items():
            if k in Commands.all_commands_list:
                self.red.set(f"{prefix}:{k}", v)
        updated_time = datetime.utcnow().timestamp()
        self.red.set(f"{RedisKeys.user_set}:{RedisKeys.updated_time}", updated_time)
        return self.get_commands_dictionary(Commands.all_commands_list)

    def get_commands_dictionary_last_update_timestamp(self):
        """
        Returns the last update time for the command dictionary as a timestamp
        """
        return float(self.red.get(f"{RedisKeys.command_counts}:{RedisKeys.updated_time}"))
    
    def get_commands_dictionary_last_update_time(self):
        """
        Returns the last update time for the command dictionary as a datetime
        """
        return datetime.fromtimestamp(self.get_commands_dictionary_last_update_timestamp())

    # TODO(IAN)
    # Basically everything below this will be removed
    # The best approach is probably to add to the User Table

    def get_user_set(self):
        """
        Returns the user_set as a list
        """
        return [int(u) for u in self.red.smembers(RedisKeys.user_set)]

    def get_user_set_count(self):
        """
        Returns the count (cardinality) of the user set
        """
        return int(self.red.scard(RedisKeys.user_set))

    def get_user_set_timestamp(self):
        """
        Returns the timestamp for the user set's last update time
        """
        return float(self.red.get(f"{RedisKeys.user_set}:{RedisKeys.updated_time}"))

    def get_user_set_timestamp_as_datetime(self):
        """
        Returns the datetime for the user set's last update time
        """
        return datetime.fromtimestamp(self.get_user_set_timestamp())
    
    def add_to_user_set(self, value):
        """
        Adds value(s) to the user_set and updates the last update time

        Returns the new update time
        """
        updated_time = datetime.utcnow().timestamp()

        if type(value) is list:
            self.red.sadd(RedisKeys.user_set, *value)
        else:
            self.red.sadd(RedisKeys.user_set, value)

        self.red.set(f"{RedisKeys.user_set}:{RedisKeys.updated_time}", updated_time)
        return updated_time

    def get_redis_health(self):
        """
        Gets health, memory, cpu, and stats information from redis
        Returns a dictionary with health info
        """
        redis_health = {}
        is_available = self.get_redis_availability()
        redis_health["available"] = is_available
        
        if (is_available):
            redis_health['memory'] = self.get_redis_memory_info()
            redis_health['cpu'] = self.get_redis_cpu_info()
            redis_health['stats'] = self.get_redis_stats_info()

        return redis_health

    def get_redis_memory_info(self):
        """
        Gets memory info from redis and formats it into a simple dictionary
        Returns a dictionary with memory info
        """
        memory_info = self.red.info()
        succint_memory_info = {}
        succint_memory_info['used_memory'] = memory_info['used_memory_human']
        succint_memory_info['used_memory_rss'] = memory_info['used_memory_rss_human']
        succint_memory_info['total_memory'] = memory_info['total_system_memory_human']

        return succint_memory_info

    def get_redis_cpu_info(self):
        """
        Gets cpu info from redis and formats it into a simple dictionary
        Returns a dictionary with cpu info
        """
        cpu_info = self.red.info()
        succint_cpu_info = {}
        succint_cpu_info['used_cpu'] = cpu_info['used_cpu_user']

        return succint_cpu_info

    def get_redis_stats_info(self):
        """
        Gets stats info from redis and formats it into a simple dictionary
        Returns a dictionary with stats info
        """
        stats_info = self.red.info()
        succint_cpu_info = {}
        succint_cpu_info['total_connections_received'] = stats_info['total_connections_received']
        succint_cpu_info['total_commands_processed'] = stats_info['total_commands_processed']

        return succint_cpu_info

    def get_redis_availability(self):
        """
        Checks if the redis server is available by pinging it.
        Returns True if available, False otherwise
        """
        try:
            self.red.ping()
        except (redis.exceptions.ConnectionError, ConnectionRefusedError):
            return False
        return True