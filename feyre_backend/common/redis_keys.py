class RedisKeys:
    """
    Common class shared across Backend and Sync services

    All Redis Keys and prefixes are stored here to ensure consistency. This class should only be consumed by RedisHelper
    """
    def __init__(self):
        # Redis Keys is a common class that holds info on all of the different keys used for REDIS
        # Any time we need to enumerate over keys, we can use this class
        # Keys can be changed here, and do not need to be typed all over the place.

        # Updated Time
        # Whenever a <Key, Value> pair is updated in Redis <Key:Updated Time> is also updated with the current timestamp
        # Ex:
        # user_set:updated_time = timestamp
        self.updated_time = "updated_time"

        # Command Prefix
        # Appended to the command name
        # Ex:
        # c_roll = 1
        self.command_prefix = "c_"

        # User prefix
        # Example User:
        # u_123456 : {
        #   characters = [
        #       {
        #           name = "gandalf",
        #           init = "1d20-10",
        #           bank = [0 , 0, 10, 0]   
        #       }
        #   ]
        # }
        self.user_prefix = "u_"

        # User set
        # Set of Discord User IDs
        # Ex:
        # [101203123, 10239024124, 437854554]
        self.user_set = "user_set"
        

        