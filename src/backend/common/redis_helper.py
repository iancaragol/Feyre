import redis

from datetime import datetime
from os import environ
from json import loads, dumps

from backend_service.api.model.initiative_tracker_model import InitiativeTracker
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

    def increment_command(self, command : str):
        """
        Increments the # of times <command> has been used and the <total> counter. Updates the <commands updated time> value

        Parameter:
            command: The command to increment

        Returns:
            The time of the update
        """
        updated_time = datetime.now().timestamp()
        self.red.incr(f"{RedisKeys.command_prefix}:{command}", amount = 1)
        self.red.incr(f"{RedisKeys.command_prefix}:total", amount = 1)
        self.red.set(f"{RedisKeys.command_counts}:{RedisKeys.updated_time}", updated_time)
        return updated_time

    def get(self, key):
        """
        Gets a value directly from Redis

        Parameter:
            key: The Key of the Value

        Returns:
            The value at key
        """
        return self.red.get(key)

    def set(self, key, value):
        """
        Sets a value in Redis

        Parameter:
            key: The key
            value: The value

        Returns:
            True/False if the set was successful
        """
        return self.red.set(key, value)

    def delete(self, key):
        """
        Delets value at key from redis

        Parameter:
            key: The key

        Returns:
            True/False if the set was successful
        """
        return self.red.delete(key)

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

        tot = self.red.get(f"{prefix}:total")
        if tot:
            total = int(tot.decode("utf-8"))
            stats_dict["total"] = total
        else:
            stats_dict["total"] = 0
        return stats_dict

    def set_commands_dictionary(self, commands_dictionary):
        prefix = RedisKeys.command_prefix
        for k, v in commands_dictionary.items():
            if k in Commands.all_commands_list or k == "total": # Special case, need to make to sure to include the total
                self.red.set(f"{prefix}:{k}", v)
        updated_time = datetime.utcnow().timestamp()
        self.red.set(f"{RedisKeys.user_set}:{RedisKeys.updated_time}", updated_time)
        return self.get_commands_dictionary(Commands.all_commands_list)

    def get_commands_dictionary_last_update_timestamp(self):
        """
        Returns the last update time for the command dictionary as a timestamp
        """
        val = self.red.get(f"{RedisKeys.command_counts}:{RedisKeys.updated_time}")
        if val:
            return float(self.red.get(f"{RedisKeys.command_counts}:{RedisKeys.updated_time}"))
        return 0.0
    
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
        val = self.red.get(f"{RedisKeys.user_set}:{RedisKeys.updated_time}")
        if val:
            return float(val)
        return 0.0

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

    def get_initiative_tracker(self, guild : int, channel : int):
        """
        Gets the initiative tracker <guild, channel> and returns it as a JSON

        Returns:
            JSON of initiative tracker model if present
            NONE if not present
        """
        key = RedisKeys.get_it_key(guild = guild, channel = channel)
        tracker = self.get(key = key)

        if tracker:
            return loads(tracker)
        else:
            return None

    def put_initiative_tracker(self, guild: int, channel: int, tracker : str):
        """
        Puts the tracker as a JSON into Redis

        Parameters:
            guild: guild for the tracker
            channel: channel for the tracker
            tracker: tracker object converted to JSON
        """
        key = RedisKeys.get_it_key(guild = guild, channel = channel)
        self.set(key = key, value = tracker)

    def delete_initiative_tracker(self, guild: int, channel: int):
        """
        Deletes the tracker from redis

        Parameters:
            guild: guild for the tracker
            channel: channel for the tracker
        """
        key = RedisKeys.get_it_key(guild = guild, channel = channel)
        self.delete(key=key)