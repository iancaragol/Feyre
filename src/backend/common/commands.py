class Commands:
    """
    Common class shared across Backend and Sync services

    Provides a list of all commands. This is primarily consumed by the StatsOperation.

    Any new commands need to be added here.
    """
    # This is a list of the most used commands. These are the commands that are returned with the ALL parameter is set to false
    # It is a SUBSET of all_commands
    default_commands_list = [
        "roll",
        "stats"
    ]

    # This is the list of ALL commands feyre supports
    all_commands_list = [
        "roll",
        "stats"
    ]