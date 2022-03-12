class Character:
    """
    Representation of a character

    Attributes:
        user: User id of character owner
        name: Name of the character
        initiative_expression: Initiative roll expression
        initiative_value: Initiative roll value
    """
    def __init__(self, user : int = None, name : str = None, initiative_expression : str = None, initiative_value : float = None, char_dict : dict = None):
        if char_dict:
            self.user = char_dict["user"]
            self.name = char_dict["name"]
            self.initiative_expression = char_dict["initiative_expression"]
            self.initiative_value = char_dict["initiative_value"]
        else:
            self.user = user
            self.name = name
            self.initiative_expression = initiative_expression
            self.initiative_value = initiative_value

    def to_dict(self):
        """
        Returns the Character as a dictionary
        """
        char_dict = {
            "user" : self.user,
            "name" : self.name,
            "initiative_expression" : self.initiative_expression,
            "initiative_value" : self.initiative_value
        }

        return char_dict
        
        
