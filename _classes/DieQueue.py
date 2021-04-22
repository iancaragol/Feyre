import json
from random import randint

class ChildRollResult:
    """
    A child roll result is a single dice roll in a dice roll expression
    
    Ex: 1d20 + 5d6 is the dice expression so 1d20 and 5d6 are both child rolls
        The Parent is the final value
    """
    def __init__(self, value, expression, dropped, critical, all_rolls):
        self.value = value
        self.expression = expression
        self.dropped = dropped
        self.critical = critical
        self.all_rolls = all_rolls

    def to_string(self):
        return f"Value: {self.value}, Dropped: {self.dropped}, Crit: {self.critical}"

    def to_dict(self):
        temp_dict = {
            "value" : self.value,
            "expression" : self.expression,
            "dropped" : self.dropped,
            "critical" : self.critical,
            "rolls" : self.all_rolls
        }

        return temp_dict

class ParentRollResult:
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
    

class ShuntingYard:
    def __init__(self, verbose = False):
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
            "greater_than_eqaul":">=",
            "less_than_equal":"<=",
            "equal":"="
        }

    async def shunt(self, expression):
        """
        Entry point for dice rolling
        """
        tokens = await self.tokenize(expression)
        count = 1
        roll_results = [] # List of RollResults objects
        
        if 'c' in tokens[-1]: # Special case, with Count. Ex: 1d6+1c3 = 1d6 THREE TIMES
            popped = tokens.pop()
            count = int(popped.replace('c', ''))
        
        # Repeat entire roll for # of count
        # If count was only one, then the list will have length 1
        for i in range(count):
            evaluated = await self.evaluate(tokens, expression)
            roll_results.append(evaluated.to_dict())

        roll_results_json = json.dumps({"parent_result" : roll_results})
        return roll_results_json 

    async def tokenize(self, expression):
        expression = expression.replace(' ', '').lower()
        for k, v in self.abbrevations.items():
            expression = expression.replace(k, v)

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

    async def precedence(self, op):
        if op == '+' or op == '-':
            return 1
        if op == '*' or op == '/':
            return 2
        return 0

    async def applyThen(self, a, b):
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
    async def applyOp(self, a, b, op): 
        if self.verbose:
            print(f"--> applyOp({a}, {b}, {op}")
        if op == '+': return float(a) + float(b)
        elif op == '-': return float(a) - float(b)
        elif op == '*': return float(a) * float(b)
        elif op == '/': return float(a) // float(b)
        elif op == '>': return float(a) >= float(b)
        elif op == '<': return float(a) <= float(b)
        elif op == '>=': return float(a) >= float(b)
        elif op == '<=': return float(a) <= float(b)
        elif op == '=': return float(a) == float(b)
        elif op == 't': return await self.applyThen(a, b)

    # Function that returns value of expression after evaluation.
    async def evaluate(self, tokens, expression):
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
                roll = await self.roll(tokens[i])
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
                    values.append(await self.applyOp(val1, val2, op))
                ops.pop() # Pop (

            else: # Token is an operator
                # While top of 'ops' has same or greater precedence to current token, which is an operator. 
                # Apply operator on top of 'ops'  to top two elements in values stack.
                while (len(ops) != 0 and
                    await self.precedence(ops[-1]) >= await self.precedence(tokens[i])):
                            
                    val2 = values.pop()
                    val1 = values.pop()
                    op = ops.pop()
                    
                    values.append(await self.applyOp(val1, val2, op))
                
                # Push current token to 'ops'.
                ops.append(tokens[i])
            i += 1
        
        # Entire expression has been parsed at this point, apply remaining ops to remaining values.
        while len(ops) != 0:
            val2 = values.pop()
            val1 = values.pop()
            op = ops.pop()
                    
            values.append(await self.applyOp(val1, val2, op))
        
        # Create final roll result, and return it
        return ParentRollResult(expression, tokens, values[-1], critical, roll_results)

    async def roll(self, expression):
        number = 0
        size = 0
        keep = -1 # If  keep is -1, then keep all
        explode = -1 # If explode is -1, then dont explode (default)
        last_char = ''
        temp_number = ""
        critical = False # If a critical (20 when 1d20) was rolled

        rolls = []
        dropped = []

        if self.verbose:
            print(f"--> roll({expression})") 
        
        for i in range(len(expression)):
            if (expression[i].isdigit()): # If its a number
                temp_number += expression[i]
            if (expression[i] == 'd'): # Expression must have a dice 1d20 then keep/explode modifires
                number = int(temp_number) # EX: 1d20, 5d20k5, 5d20e5, 5d20e5k5
                last_char = 'd'
                temp_number = ""

            elif (expression[i] == 'k'):
                if (last_char == 'e'): # If last char is an e, then we have e5k5
                    explode = int(temp_number)
                elif (last_char == 'd'): # If last char is d, then we have d5k5
                    size = int(temp_number)
                last_char = 'k'
                temp_number = ""

            elif (expression[i] == 'e'):
                if (last_char == 'k'): # If last char is an k, then we have k5e5
                    keep = int(temp_number)
                elif (last_char == 'd'): # If last char is d, then we have d5e5
                    size = int(temp_number)
                last_char = 'e'
                temp_number = ""
            
        # Make sure we get whatever was last 
        if (last_char == 'k'):
            keep = int(temp_number)
        if (last_char == 'e'):
            explode = int(temp_number)
        elif (last_char == 'd'):
            size = int(temp_number)

        if self.verbose:
            print(f"number: {number}, size: {size}, keep: {keep}, explode: {explode}") 

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
                    rolls.append(roll)
                    if self.verbose:
                        print(f"exploded on {roll}")
                    roll = randint(1, size)

            rolls.append(roll)

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
        if self.verbose:        
            print(f"sum: {value}")

        return ChildRollResult(value, expression, dropped, critical, rolls)

class RollFormatter():
    async def format_roll(self, roll_results):
        output_string = ""
        # Most standard case, Count = 1
        if len(roll_results) == 1:
            result = roll_results[0]
            
            output_string += "-> "
            output_string += f"**{result.value}**"

            if result.critical:
                output_string += ", *Critical!*"
            
            return output_string
            

    async def  format_roll_verbose(self, roll_results):
        print("TO DO")
    


