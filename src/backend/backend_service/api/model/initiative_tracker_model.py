class InitiativeTracker:
    """
    The initiative tracker for the guild's channel. Contains an ordered list of all player's characters and the turn count

    Attributes:
        guild: (int) The guild of the tracker
        channel: (int) The channel of the tracker
        characters: [character] Ordered list of characterss
        turn: (int) The current turn, characters[i] is the current character
    """
    def __init__(self, guild, channel):
        self.guild = guild
        self.channel = channel
        self.characters = []
        self.turn = 0

    def to_dict(self):
        """
        Returns the InitiativeTracker as a dictionary
        """
        tracker_dict = {
            "guild" = self.guild,
            "channel" = self.channel,
            "characters" = self.characters,
            "turn" = self.turn
        }

        return tracker_dict

    def from_dict(self, tracker_dict):
        """
        Updates the values of the InitiativeTracker form a dictionary
        """

        self.guild = tracker_dict["guild"]
        self.channel = tracker_dict["channel"]
        
        for (c in tracker_dict["characters"]):
            print("Convert to character json here")

        self.turn = tracker_dict["turn"]