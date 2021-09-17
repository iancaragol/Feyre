class ParentRollModel:
    """
    Parent Roll Model contains the final result of a RollOperation and a list of ChildRollModels

    This is what is parsed by the Frontend Service to be displayed to the user.

    Attributes:
        expression: (string) The dice expression that was parsed
        tokens: (list[string]) Dice expression broken down into a list of tokens
        total: (float) The final sum/result of the dice roll
        critical: (bool) Indicates if there were any criticals rolled
        child_rolls (list[ChildRollModel]) List of Child Roll Models

    Ex: 1d20 + 5d6 is the dice expression so 1d20 and 5d6 are both child rolls
        The Parent is the final value

        ChildRoll 1d20 = 10
        ChildRoll 5d6 = 18

        Then the total = 28
    """
    def __init__(self, expression, tokens, total, critical, child_rolls):
        self.expression = expression
        self.tokens = tokens
        self.total = total
        self.critical = critical
        self.child_rolls = child_rolls

    def to_dict(self):
        temp_dict = {
            "expression" : self.expression,
            "tokens": self.tokens,
            "total" : self.total,
            "critical" : self.critical,
            "child_rolls" : self.child_rolls
        }

        return temp_dict