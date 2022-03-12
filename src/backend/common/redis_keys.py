class RedisKeys:
    """
    Common class shared across Backend and Sync services

    All Redis Keys and prefixes are stored here to ensure consistency. This class should only be consumed by RedisHelper
    """
    # Redis Keys is a common class that holds info on all of the different keys used for REDIS
    # Any time we need to enumerate over keys, we can use this class
    # Keys can be changed here, and do not need to be typed all over the place.

    # Updated Time
    # Whenever a <Key, Value> pair is updated in Redis <Set:Updated Time> is also updated with the current timestamp
    # Ex:
    # user_set:updated_time = timestamp
    # command_set:updated_time = timestamp
    updated_time = "updated_time"

    # Command Prefix
    # Appended to the command name
    # Ex:
    # c:roll = 1
    command_prefix = "c"

    # Command set
    # Set of command usage counts
    # Ex:
    # c:roll = 1
    command_counts = "command_counts"

    # ALL OF THIS USER STUFF IS SUBJECT TO CHANGE

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
    user_prefix = "u_"

    # User set
    # Set of Discord User IDs
    # Ex:
    # [101203123, 10239024124, 437854554]
    user_set = "user_set"

    @staticmethod
    def get_it_key(guild : int, channel: int):
        """
        Takes the guild and channel and returns the initiative tracker key
        """

        # Prefix for any initiaitve trackers
        # Used alongside guild and channel
        # it_guild_channel
        initiative_tracker_prefix = "it"

        return f"{initiative_tracker_prefix}:{guild}:{channel}"