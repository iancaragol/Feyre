class ChildRollModel():
    """
    A child roll result is a single dice roll in a dice roll expression

    Attributes:
        value: (float) The result of this child roll
        expression: (string) The child dice expression that was parsed
        dropped: (list[float]) A list of any dropped dice
        exploded: (list[float]) A list of any exploded dice
        critical: (bool) Indicates if there were any criticals rolled
        all_rolls (list[float]) List of all rolled values
    
    Ex: 1d20 + 5d6 is the dice expression so 1d20 and 5d6 are both child rolls
        The Parent is the final value
    """
    def __init__(self, value, expression, dropped, exploded, critical, all_rolls):
        self.value = value
        self.expression = expression
        self.dropped = dropped
        self.exploded = exploded
        self.critical = critical
        self.all_rolls = all_rolls

    def to_string(self):
        return f"Value: {self.value}, Dropped: {self.dropped}, Crit: {self.critical}"

    def to_dict(self):
        temp_dict = {
            "value" : self.value,
            "expression" : self.expression,
            "dropped" : self.dropped,
            "exploded" : self.exploded,
            "critical" : self.critical,
            "rolls" : self.all_rolls
        }

        return temp_dict