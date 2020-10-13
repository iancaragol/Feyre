# 1d20>15 then 1d8 count 12
import sys
from asteval import Interpreter
from random import randint

class DiceParseError(Exception):
    """Exception raised for errors dice rolls

    Attributes:
        expression -- input expression which caused the error
        message -- explanation of the error
    """

    def __init__(self, expression, exception_type, message):
        self.expression = expression
        self.exception_type = exception_type
        self.message = message
        super().__init__(self.message)

class Die:
    def __init__(self, number, size):
        self.size = size
        self.number = number
        self.modifiers = []

        self.rolls = []
        self.dropped = []
        self.criticals = []
        self.failures = []
        self.result = None

    def evaluate(self):
        # First do all dice rolls
        for i in range(0, self.number):
            roll = randint(1, self.size)

            if self.size == 20: # If the dice is a d20
                if roll == 1:
                    self.failures.append(roll)
                elif roll == 20:
                    self.criticals.append(roll)

            self.rolls.append(roll)

        # Then apply modifiers
        for mod in self.modifiers:
            if mod[0] == 'keep': # If this is a keep modifier
                for i in range(len(self.rolls) - mod[1]):
                    self.dropped.append(self.rolls.pop(self.rolls.index(min(self.rolls))))
                
        self.result = sum(self.rolls)
        return self.result

class DiceExpressionEvaluator:
    def __init__(self, expression):
        self.expression = expression.lower().strip() # The string input
        self.eval_expression = None # The expression to be evaluated, this is constructed and passed to eval function

        self.expression_list = None # 1d20 -> ['1', 'd', '20']
        self.dice_list = None

        self.type = None
        self.result = None

    def seperate_string_number(self):
        """
        Seperates the dice expression into a strings

        1d20+5 -> ['1', 'd', '20', '+' '5']
        """
        # https://stackoverflow.com/questions/430079/how-to-split-strings-into-text-and-number
        previous_character = self.expression[0]
        groups = []
        newword = self.expression[0]
        for x, i in enumerate(self.expression[1:]):
            if i.isalpha() and previous_character.isalpha():
                newword += i
            elif i.isnumeric() and (previous_character.isnumeric() or previous_character == '.'):
                newword += i
            elif i == '.' and previous_character.isnumeric():
                newword += i
            else:
                if newword != ' ': # Skip spaces
                    groups.append(newword)
                newword = i

            previous_character = i

            if x == len(self.expression) - 2:
                groups.append(newword)
                newword = ''

        self.expression_list = groups

    def create_dice_list(self):
        """
        ['1', 'd', '20', '+' '5'] -> [('dice', 1, 20), +, '5']
        """
        dice_list = [] 
        i = 0
        for j in range(len(self.expression_list)): # Because pyhton is weird, our iterator is actually i
            delete_previous_char = True # If true, then the previous char will be treated as part of the dice. False if previous is +, /, -, etc...

            if i >= len(self.expression_list):
                break

            # DICE
            if self.expression_list[i] == 'd':
                size = 0
                number = 0
                
                # Expression ends with a d
                if i == len(self.expression_list) - 1: 
                    raise DiceParseError(self.expression, "Invalid dice size", f"Size of dice was not specified (expression ends with d) \n\n{self.expression_list}")
                
                # First check if number of dice is valid
                try:
                    size = int(self.expression_list[i+1])
                except:
                    raise DiceParseError(self.expression, "Invalid dice size", f"The value {self.expression_list[i+1]} at index {i+1} is not a valid dice size because it is not an integer. \n\n{self.expression_list}")

                # Now check the number of dice
                if i == 0: # Saftey check for out of bounds, if starts with d assume 1
                    number = 1
                
                else: # Otherwise get number
                    try:
                        number = int(self.expression_list[i-1]) # If its an int then set that as number
                    except:   
                        try:                   
                            number = float(self.expression_list[i-1]) # If its a float, raise an error
                        except:
                            number = 1 # Otherwise treat number as 1
                            delete_previous_char = False
                        if type(number) is float:
                            raise DiceParseError(self.expression, "Invalid number of dice", f"{number} is not a valid number of dice because it is not an integer. \n\n{self.expression_list}")

                if i > 0:            
                    if len(dice_list) > 0 and delete_previous_char:
                        del dice_list[len(dice_list)-1]

                i += 1 # Skip over next value
                dice_list.append(Die(number, size)) # This tuple is a die

            # KEEP Modifier
            elif self.expression_list[i] == 'k':
                keep_count = sys.maxsize # By default, keep all dice
                
                # Expression ends with a k
                if i == len(self.expression_list) - 1: 
                    raise DiceParseError(self.expression, "Invalid keep count", f"The number of dice to keep was not specified. (Expression ends in k) \n\n{self.expression_list}")
                
                # First check if the keep number is valid
                try:
                    keep_count = int(self.expression_list[i+1])
                except:
                    raise DiceParseError(self.expression, "Invalid keep count", f"The value {self.expression_list[i+1]} at index {i+1} is not a valid number of dice to keep because it is not an integer. \n\n{self.expression_list}")

                if len(dice_list) > 0:
                    if isinstance(dice_list[len(dice_list)-1], Die): # Make sure last value was a dice
                        dice_list[len(dice_list)-1].modifiers.append(('keep', keep_count)) # This tuple is a keep flag
                        i += 1 #Skip next value
                    else: # keep without a dice before it
                        raise DiceParseError(self.expression, "Invalid keep position", f"The keep flag at index {i+1} does directly follow a dice expression. \n\n{self.expression_list}")
                else:
                    raise DiceParseError(self.expression, "Invalid keep position", f"A dice expression cannot start with a keep flag.\n\n{self.expression_list}")

            #OTHER MODIFIERS GO HERE

            else:
                dice_list.append(self.expression_list[i]) # Add it to expression
                # if not self.is_integer(self.expression_list[i]) and self.expression_list[i] not in ['d', 'k']: # If its not an integer and its not a flag
            i += 1

        self.dice_list = dice_list

    def evaluate_dice_list(self):
        """
        Evaluates each dice in the dice list, constructs and evaluates final string
        """
        self.eval_expression = ""
        for i in range(len(self.dice_list)):
            if isinstance(self.dice_list[i], Die):
                roll_result = self.dice_list[i].evaluate()
                self.eval_expression += str(roll_result)
            else:
                self.eval_expression += self.dice_list[i]

        # Evaluate the constructed string
        aeval = Interpreter()
        self.result = aeval.eval(self.eval_expression)

        return self.result

    def evaluate(self):
        """
        Calls all helper functions and returns the result of the dice roll
        """
        self.seperate_string_number()
        self.create_dice_list()
        return self.evaluate_dice_list()

    def is_integer(self, n):
        try:
            int(n)
        except ValueError:
            return False
        else:
            return True

def main():
    test_die = DiceExpressionEvaluator("5d20k1>15")
    print(test_die.evaluate())
    print()

if __name__ == "__main__":
    main()
