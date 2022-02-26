class ParentRollModel:
    """
    Parent Roll Model contains the final result of a RollOperation and a list of ChildRollModels

    This is what is parsed by the Frontend Service to be displayed to the user.

    Attributes:
        expression: (string) The dice expression that was parsed
        tokens: (list[string]) Dice expression broken down into a list of tokens
        total: (float) The final sum/result of the dice roll
        critical: (bool) Indicates if there were any criticals rolled
        child_rolls: (list[ChildRollModel]) List of Child Roll Models
        md_expression_str: (string) Final expression with dice roleld displayed as markdown text

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
        self.md_result = self.expression_to_md_result()

    def expression_to_md_result(self):
        """
        Takes self.tokens and turns it into a result markdown

        Ex:
            [2d20k1 + 5]
            =>
            [[17, ~~1~~]] + 5]    
        """

        final_result_str = ""

        j = 0
        for i in range(len(self.tokens)):
            if (len(self.tokens[i]) > 1 and not self.tokens[i].isnumeric()): # If token is not an operator
                final_result_str += self.create_roll_list_md_str(self.child_rolls[j])
                j += 1
            else:
                final_result_str += self.tokens[i]

        if (len(final_result_str) > 64):
            final_result_str = final_result_str[:64] + "..."
        
        return final_result_str

    def create_roll_list_md_str(self, child_roll):
        """
        Helper function for expression_to_md_result.
        Constructs each child_roll's markdown string.

        Ex:
            [2d20k1]
            =>
            [17, ~~1~~]
        """

        # This method does a lot of iteration if many dice are rolled (like 1000)
        # Can it be skipped/optimized if too many dice are rolled?
        roll_list_str = "["
        for r in child_roll["rolled"]:
            roll_list_str += str(r)
            roll_list_str += ", "
        
        for d in child_roll["dropped"]:
            roll_list_str += f"~~{d}~~"
            roll_list_str += ", "

        for e in child_roll["exploded"]:
            roll_list_str += f"__{e}__"
            roll_list_str += ", "

        roll_list_str = roll_list_str.rstrip(', ')
        roll_list_str = roll_list_str.strip() + "]"

        return roll_list_str

    def to_dict(self):
        temp_dict = {
            "expression" : self.expression,
            "md_result" : self.md_result,
            "tokens": self.tokens,
            "total" : self.total,
            "critical" : self.critical,
            "child_rolls" : self.child_rolls
        }

        return temp_dict