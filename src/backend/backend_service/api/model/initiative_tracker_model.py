from backend_service.api.model.character_model import Character

class InitiativeTracker:
    """
    The initiative tracker for the guild's channel. Contains an ordered list of all player's characters and the turn count

    Attributes:
        guild: (int) The guild of the tracker
        channel: (int) The channel of the tracker
        characters: [character] Ordered list of characters
        turn: (int) The current turn, characters[i] is the current character
        message_id: (int) The integer id of the last message that the frontend posted for this tracker
    """
    def __init__(self, guild : int = None, channel : int = None, it_dict : dict = None):
        if it_dict:
            self.guild = it_dict["guild"]
            self.channel = it_dict["channel"]
            self.turn = it_dict["turn"]
            self.characters = []
            self.message_id = it_dict["message_id"]

            for c in it_dict["characters"]:
                char = Character(char_dict=c)
                self.characters.append(char)
        else:
            self.guild = guild
            self.channel = channel
            self.characters = []
            self.turn = 1
            self.message_id = None

    def to_dict(self):
        """
        Returns the InitiativeTracker as a dictionary
        """
        tracker_dict = {
            "guild" : self.guild,
            "channel" : self.channel,
            "characters" : [],
            "turn" : self.turn,
            "message_id" : self.message_id
        }

        for c in self.characters:
            tracker_dict["characters"].append(c.to_dict())
        return tracker_dict