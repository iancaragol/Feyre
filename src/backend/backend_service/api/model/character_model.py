class Character:
    """
    Representation of a character

    Attributes:
        user: User id of character owner
        name: Name of the character
        initiative_expression: Initiative roll expression
        initiative_value: Initiative roll value
    """
    def __init__(self, user : int = None,  id : int = None, is_active : bool = False, name : str = None, initiative_expression : str = None, initiative_value : float = None, char_dict : dict = None):
        if char_dict:
            self.user = char_dict["user"]
            self.name = char_dict["name"]
            self.initiative_expression = char_dict["initiative_expression"]
            self.initiative_value = char_dict["initiative_value"]
            self.is_active = None # is_active is only used when joining initiative, its not stored as part of the InitiativeTracker
            self.id = None # Id is also only used by the initiative tracker
        else:
            self.user = user
            self.name = name
            self.initiative_expression = initiative_expression
            self.initiative_value = initiative_value
            self.is_active = is_active
            self.id = id

    def to_dict(self):
        """
        Returns the Character as a dictionary
        """
        char_dict = {
            "user" : self.user,
            "name" : self.name,
            "initiative_expression" : self.initiative_expression,
            "initiative_value" : self.initiative_value,
            "is_active" : self.is_active,
            "id" : self.id
        }

        return char_dict
        
        
