import traceback

from json import dumps
from random import randint
from backend_service.api.model.child_roll_model import ChildRollModel
from backend_service.api.model.parent_roll_model import ParentRollModel

MAX_DICESIZE = 10000

class RollOperation():
    """
    Operation that takes a dice expression, evaluates it, and returns a list of ParentRollModels
    """

    # TODO(Ian)
    # Need to handle typos like ++
    # Need to handle not providing the number of dice like d20
    # Sometimes operators will be missing
    # Ex: 1d20k3+5c3 will lose the +

    def __init__(self, expression = None, verbose = False):
        self.expression = expression
        self.verbose = verbose
        self.abbrevations = {
            "count":'c',
            "then":'t',
            "keep":'k',
            "plus":'+',
            "minus":'-',
            "times":'*',
            "divide":"/",
            "left_parenthesis": "(",
            "right_parenthesis": ")",
            "greater_than":">",
            "less_than":"<",
            "greater_than_equal":">=",
            "less_than_equal":"<=",
            "equal":"="
        }

    def execute(self):
        """
        Executes the RollOperation
        """

        try:
            return self.shunt(self.expression)
        except Exception as e:
            if self.verbose:
                print(traceback.format_exc())
            raise RollOperationException(e, self.expression)

    def shunt(self, expression):
        """
        Entry point for dice rolling

        Returns: A Json list of ParentRollModels
        """
        tokens = self.tokenize(expression)
        count = 1
        roll_results = [] # List of RollResults objects
        
        if 'c' in tokens[-1]: # Special case, with Count. Ex: 1d6+1c3 = 1d6 THREE TIMES
            popped = tokens.pop()
            count = int(popped.replace('c', ''))
        
        # Repeat entire roll for # of count
        # If count was only one, then the list will have length 1
        for i in range(count):
            evaluated = self.evaluate(tokens, expression)
            roll_results.append(evaluated.to_dict())

        roll_results_json = dumps({"parent_result" : roll_results})
        return roll_results_json 

    def tokenize(self, expression):
        """
        Token mappings:
        d = dice
        k = keep
        e = explode (>=)
        ᶒ = explode_on (==) <-- Mapping this to a unique character makes it easier to parse with current parsing methods
        c = count
        t = then
        """
        expression = expression.replace(' ', '').lower()
        for k, v in self.abbrevations.items():
            expression = expression.replace(k, v)
        
        # Basically, users will type >=
        # The algorithm needs to treat this as one token
        expression = expression.replace('<=', '≤').replace('>=', '≥')

        tokens = []
        new_token = ""

        for i in range(len(expression)):
            if (expression[i].isdigit()):
                new_token += expression[i]
            elif (expression[i] == 'd'): # Dice
                new_token += 'd'
            elif (expression[i] == 'k'): # Keep
                new_token += 'k'
            elif (expression[i] == 'e'): # Explode
                if (i < len(expression)):
                    if (expression[i+1] == 'o'): # Explode On
                        new_token += "ᶒ" # This may seem wild, but it makes parsing much easier
                    else:
                        new_token += 'e'
                else:
                    new_token += 'e'
            elif (expression[i] == 'c'): # Count
                tokens.append(new_token)
                new_token = 'c'
            elif (expression[i] in self.abbrevations.values()): # Token is an operator
                if (len(new_token) > 0): # Make sure to append any digits
                    tokens.append(new_token)
                    new_token = ""
                tokens.append(expression[i])
        if (len(new_token) > 0): # Make sure to append the last digit
            tokens.append(new_token)
            new_token = ""

        if self.verbose:
            print(f"{expression} -> {tokens}")

        return tokens

    def precedence(self, op):
        if op == '+' or op == '-':
            return 1
        if op == '*' or op == '/':
            return 2
        return 0

    def applyThen(self, a, b):
        if self.verbose:
            print(f"--> applyThen({a}, {b})")
        if a:
            if self.verbose:
                print(f"a is true, return {b}")
            return b
        else:
            if self.verbose:
                print(f"a is false, return 0")
            return 0

    # Function to perform arithmetic operations.
    def applyOp(self, a, b, op): 
        if self.verbose:
            print(f"--> applyOp({a}, {b}, {op}")
        if op == '+': return float(a) + float(b)
        elif op == '-': return float(a) - float(b)
        elif op == '*': return float(a) * float(b)
        elif op == '/': return float(a) // float(b)
        elif op == '>': return float(a) >= float(b)
        elif op == '<': return float(a) <= float(b)
        elif op == '≥': return float(a) >= float(b)
        elif op == '≤': return float(a) <= float(b)
        elif op == '=': return float(a) == float(b)
        elif op == 't': return self.applyThen(a, b)

    # Function that returns value of expression after evaluation.
    def evaluate(self, tokens, expression):
        roll_results = [] # List of roll results to check for criticals, dropped
        dropped = []
        critical = False
        values = [] # stack to store integers
        ops = [] # stack to store operators
        i = 0

        # Special check to see if there are any counts
        
        while i < len(tokens):            
            if self.verbose:
                print(f"Current token: {tokens[i]}")
            if tokens[i] == '(': # Token is a left parenthesis, push it to ops
                ops.append(tokens[i])

            elif ('d' in tokens[i]): # Token is a dice, evaluate and push it to values
                roll = self.roll(tokens[i])
                roll_results.append(roll.to_dict()) # This is super wacky, need to find a better way to express dropped/critical dice
                dropped.extend(roll.dropped)
                if roll.critical: 
                    critical = True
                values.append(str(roll.value))

            elif tokens[i].isdigit(): # Token is a number, push it to values
                values.append(tokens[i])

            elif tokens[i] == ')': # Token is right parenthesis, push it to ops and evaluate
                while len(ops) != 0 and ops[-1] != '(':
                    val2 = values.pop()
                    val1 = values.pop()
                    op = ops.pop()
                    values.append(self.applyOp(val1, val2, op))
                ops.pop() # Pop (

            else: # Token is an operator
                # While top of 'ops' has same or greater precedence to current token, which is an operator. 
                # Apply operator on top of 'ops'  to top two elements in values stack.
                while (len(ops) != 0 and
                    self.precedence(ops[-1]) >= self.precedence(tokens[i])):
                            
                    val2 = values.pop()
                    val1 = values.pop()
                    op = ops.pop()
                    
                    values.append(self.applyOp(val1, val2, op))
                
                # Push current token to 'ops'.
                ops.append(tokens[i])
            i += 1
        
        # Entire expression has been parsed at this point, apply remaining ops to remaining values.
        while len(ops) != 0:
            val2 = values.pop()
            val1 = values.pop()
            op = ops.pop()
                    
            values.append(self.applyOp(val1, val2, op))
        
        # Create final roll result, and return it
        return ParentRollModel(expression, tokens, values[-1], critical, roll_results)

    def roll(self, expression):
        number = 0
        size = 0
        keep = -1 # If  keep is -1, then keep all
        explode = -1 # If explode is -1, then dont explode (default)
        explode_on = -1 # Explode on is == instead of >=
        last_char = ''
        temp_number = ""
        critical = False # If a critical (20 when 1d20) was rolled

        # This is the list of rolled dice
        # Keep modifier will drop dice from this list
        # and add them to dropped
        rolls = []

        dropped = [] # List of dropped dice

        # List of rolls from exploded dice
        # If there are dice in this list
        # then they will be added to the final result
        exploded = [] 

        if self.verbose:
            print(f"--> roll({expression})") 
        
        for i in range(len(expression)):
            if (expression[i].isdigit()): # If its a number
                temp_number += expression[i]
            if (expression[i] == 'd'): # Expression must have a dice 1d20 then keep/explode modifiers
                number = int(temp_number) if (temp_number != "") else 0 # EX: 1d20, 5d20k5, 5d20e5, 5d20e5k5
                last_char = 'd'
                temp_number = ""

            elif (expression[i] == 'k'):
                if (last_char == 'e'): # If last char is an e, then we have e5k5
                    explode = int(temp_number)
                elif (last_char == 'd'): # If last char is d, then we have d5k5
                    size = int(temp_number)
                last_char = 'k'
                temp_number = ""

            elif (expression[i] == 'e'): # Explode
                if (last_char == 'k'): # If last char is an k, then we have k5e5
                    keep = int(temp_number)
                elif (last_char == 'd'): # If last char is d, then we have d5e5
                    size = int(temp_number)
                last_char = 'e'
                temp_number = ""

            elif (expression[i] == 'ᶒ'): # Explode ON
                if (last_char == 'k'): # If last char is an k, then we have k5e5
                    keep = int(temp_number)
                elif (last_char == 'd'): # If last char is d, then we have d5e5
                    size = int(temp_number)
                last_char = 'ᶒ'
                temp_number = ""
                    
        # Make sure we get whatever was last 
        if (last_char == 'k'):
            keep = int(temp_number)
        if (last_char == 'e'):
            explode = int(temp_number)
        if (last_char == 'ᶒ'):
            explode_on = int(temp_number)
        elif (last_char == 'd'):
            size = int(temp_number)

        if self.verbose:
            print(f"number: {number}, size: {size}, keep: {keep}, explode: {explode}") 

        if number > MAX_DICESIZE:
            raise ValueError(f"The number of dice ({number}) is greater than the maximum of {MAX_DICESIZE}")

        for i in range(number):
            if size == 0:
                roll = 0
            else:    
                roll = randint(1, size)

            # Evaluate dice explosions
            # If the roll is >= to the explode value, it is rolled again and added to the total
            # Currently, you can only explode once
            if explode != -1:
                if roll >= explode:
                    if self.verbose:
                        print(f"exploded (>=) on {roll}")
                    exploded_roll = randint(1, size) # Roll the exploded dice
                    exploded.append(exploded_roll)
            
            # Explode On is the same as explode
            # Except == instead of >=
            if explode_on != -1:
                if roll == explode_on:
                    if self.verbose:
                        print(f"exploded (==) on {roll}")
                    exploded_roll = randint(1, size) # Roll the exploded dice
                    exploded.append(exploded_roll)

            # Add the roll to the final roll list
            rolls.append(roll)

            # By default, criticals are only for D20
            if size == 20 and roll == 20:
                critical = True

            if self.verbose:
                print(f"result (d{size}): {roll}")

        if keep != -1: # If -1, then keep all
            for i in range(number - keep): # Otherwise, drop number - keep dice
                drop_die = rolls.pop(rolls.index(min(rolls))) # Drop lowest dice
                if self.verbose:
                    print(f"dropped {drop_die}")
                dropped.append(drop_die)
        
        value = sum(rolls)
        if (len(exploded) >= 0):
            value += sum(exploded) # Add exploded rolls to the final result

        if self.verbose:        
            print(f"sum: {value}")

        return ChildRollModel(value, expression, dropped, exploded, critical, rolls)

class RollOperationException(Exception):
    """
    Exception raised for errors in the RollOperation

    Attributes:
        exception: The original exception that was thrown
        message: Error message to be returned to the user
    """

    def __init__(self, exception, expression):
        self.exception = exception
        self.expression = expression
        self.message = ""
        
        if str(exception) == "pop from empty list":
            self.message = "Invalid expression string. Two operators (+, -, /, ...) in a row is not supported"

        # Todo(Ian)
        # This is a bit ugly, can make this cleaner.
        # Also should emit or log these messages to prometheus
        if str(exception).startswith("The number of dice"):
            self.message = str(exception)