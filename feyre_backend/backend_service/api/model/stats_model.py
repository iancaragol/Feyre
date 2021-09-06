class StatsModel:
    def __init__(self):
        # This is a list of the most used commands. These are the commands that are returned with the ALL parameter is set to false
        # It is a SUBSET of all_commands
        self.commands = [
            "roll",
            "stats"
        ]

        # This is the list of ALL commands feyre supports
        self.all_commands = [
            "roll",
            "stats"
        ]

        self.stats_dict = {}