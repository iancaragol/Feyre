# 1d20>15 then 1d8 count 12
import sys
import re
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
        self.expression = expression.lower().strip().replace(' ', '') # The string input
        self.eval_expression = None # The expression to be evaluated, this is constructed and passed to eval function

        self.expression_list = None # 1d20 -> ['1', 'd', '20']
        self.dice_list = None

        self.type = None
        self.result = None

        self.left_side = None # Left side of equality, if this expression is an equality

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

        groups = self.replace_equals(groups)
        self.expression_list = groups

    def replace_equals(self, groups):
        """
        Replaces = with == for aeval
        """
        if '=' not in groups:
            return groups
        else:
            idx = groups.index('=')
            if groups[idx - 1] != '<' or groups[idx - 1] != '>':
                groups[idx] = '=='
        return groups


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

    def evaluate(self):
        """
        Calls all helper functions and returns the result of the dice roll
        """
        self.seperate_string_number()
        self.create_dice_list()
        self.evaluate_dice_list()
        self.set_left_side()

        return self.result, self.left_side

    def set_left_side(self):
        eq_index = -1
        if '<' in self.dice_list:
            eq_index = self.dice_list.index('<')
        elif '>' in self.dice_list:
            eq_index = self.dice_list.index('>')
        elif '<=' in self.dice_list:
            eq_index = self.dice_list.index('<=')
        elif '>=' in self.dice_list:
            eq_index = self.dice_list.index('>=')
        if '==' in self.dice_list:
            eq_index = self.dice_list.index('==')
        
        if eq_index != -1:
            self.left_side = self.dice_list[eq_index - 1]

    def is_integer(self, n):
        try:
            int(n)
        except ValueError:
            return False
        else:
            return True


class ExpressionEvaluator():
    def __init__(self, expression):
        self.expression = expression.lower().strip().replace(' ', '').replace('then', 't').replace('count', 'c')
        self.sub_expression_list = []
        self.failures = []
        self.results = []

    def evaluate(self):
        # Split on instances of t for THEN and c for COUNT
        self.sub_expression_list = re.split('(t|c)', self.expression)

        count = 1 # Default count to 1 (meaning count is not included)

        # Get count
        if self.sub_expression_list.count('c') == 1:
            count_index = self.sub_expression_list.index('c')
            if count_index == len(self.sub_expression_list):
                raise DiceParseError(self.expression, "Invalid count statement", "A count statement must be followed by an integer.")
            else:
                try:
                    count = int(self.sub_expression_list[count_index + 1])
                except:
                    raise DiceParseError(self.expression, "Invalid count statement", f"A count statement must be followed by an integer. {self.sub_expression_list[count_index + 1]} is not an integer.")
        elif self.sub_expression_list.count('c') > 1:
            raise DiceParseError(self.expression, "Invalid count statement", f"Only one instance of count (c) is supported.")
                            
        for j in range(0, count):
            # Evaluate dice rolls 
            temp_sub_expression_list = list(self.sub_expression_list) # Temp list is needed to keep counts independent                  
            for i in range(len(temp_sub_expression_list)):
                # print(temp_sub_expression_list[i])
                if 'd' in temp_sub_expression_list[i]: # First evaluate all dice rolls
                    de = DiceExpressionEvaluator(temp_sub_expression_list[i]).evaluate()
                    temp_sub_expression_list[i] = de # Result, Left Side of Ineq

            # Evaluate then expressions
            if 't' in temp_sub_expression_list:            
                for i in range(len(temp_sub_expression_list)):
                    if temp_sub_expression_list[i] == 't':
                        if isinstance(temp_sub_expression_list[i - 1][0], bool):
                            if temp_sub_expression_list[i - 1]: # If the check was successful
                                if i + 1 >= len(temp_sub_expression_list):
                                    raise DiceParseError(self.expression, "Invalid then statement", "A then statement must be followed by a dice expression.")
                                else:
                                    # If check was successful and the then statement is followed by a valid dice roll, add it
                                    try:
                                        self.results.append(int(temp_sub_expression_list[i+1][0])) 
                                    except:
                                        raise DiceParseError(self.expression, "Invalid then statement", "A then statement must be followed by a dice expression.")
                            else: # Check was unsuccessful
                                if i - 1 < 0:
                                    raise DiceParseError(self.expression, "Invalid then statement", "A then statement must be followed by a dice expression.")
                                else:
                                    # If check was successful and the then statement is followed by a valid dice roll, add it
                                    try:
                                        self.failures.append(int(temp_sub_expression_list[i-1][1]))
                                    except:
                                        raise DiceParseError(self.expression, "Invalid then statement", "A then statement must be followed by a dice expression.")
                        else:
                            raise DiceParseError(self.expression, "Invalid then statement", "A then statement must follow a skill check or other roll that results in True or False.")

        return self.results, self.failures # TODO Failures returns nothing right now


def main():
    ee = ExpressionEvaluator("1d20>15t1d8c10")
    r, f = ee.evaluate()
    print(r)
    print(f)


if __name__ == "__main__":
    main()

