from common.redis_keys import RedisKeys

class StatsModel:
    def __init__(self):
        # Redis Keys is a common class that holds info on all of the different keys used for REDIS
        # Any time we need to enumerate over keys, we can use this class
        rk = RedisKeys()
        
        self.commands = rk.commands
        self.all_commands = rk.all_commands

        self.stats_dict = {}