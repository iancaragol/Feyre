class RedisKeys:
    def __init__(self):
        # Redis Keys is a common class that holds info on all of the different keys used for REDIS
        # Any time we need to enumerate over keys, we can use this class

        # This is a list of the most used commands. These are the commands that are returned with the ALL parameter is set to false
        # It is a SUBSET of all_commands
        self.commands = [
            "c_roll",
            "c_stats"
        ]

        # This is the list of ALL commands feyre supports
        self.all_commands = [
            "c_roll",
            "c_stats"
        ]

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
        self.user_prefix = 'u_'

        

        