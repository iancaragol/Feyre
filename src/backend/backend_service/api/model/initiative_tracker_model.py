from backend_service.api.model.character_model import Character

class InitiativeTracker:
    """
    The initiative tracker for the guild's channel. Contains an ordered list of all player's characters and the turn count

    Attributes:
        guild: (int) The guild of the tracker
        channel: (int) The channel of the tracker
        characters: [character] Ordered list of characterss
        turn: (int) The current turn, characters[i] is the current character
    """
    def __init__(self, guild : int = None, channel : int = None, it_dict : dict = None):
        if it_dict:
            self.guild = it_dict["guild"]
            self.channel = it_dict["channel"]
            self.turn = it_dict["turn"]
            self.characters = []
            
            for c in it_dict["characters"]:
                char = Character(char_dict=c)
                self.characters.append(char)
        else:
            self.guild = guild
            self.channel = channel
            self.characters = []
            self.turn = 0

    def to_dict(self):
        """
        Returns the InitiativeTracker as a dictionary
        """
        tracker_dict = {
            "guild" : self.guild,
            "channel" : self.channel,
            "characters" : [],
            "turn" : self.turn
        }

        for c in self.characters:
            tracker_dict["characters"].append(c.to_dict())
        return tracker_dict