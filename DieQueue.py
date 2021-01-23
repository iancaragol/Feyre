class Die:
   def roll(self, expression):
       exp = expression.split('d')
       size = int(exp)

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
            "right_parenthesis": ")"
        }   

    def tokenize(self, expression):
        expression = expression.replace(' ', '').lower()
        for k, v in self.abbrevations.items():
            expression = expression.replace(k, v)

        tokens = []
        new_token = ""

        for i in range(len(expression)):
            if (expression[i].isdigit()):
                if (new_token[:-1] == 'd'): # If the previous character is a d, then this is a dice
                    new_token += expression[i]
                    new_token = ""
                else:
                    new_token += expression[i]
            elif (expression[i] == 'd'):
                new_token += 'd'
            elif (expression[i] == 'k'):
                new_token += 'k'
            elif (expression[i] in self.abbrevations.values()): # Token is an operator
                if (len(new_token) > 0): # Make sure to append any digits
                    tokens.append(new_token)
                    new_token = ""
                tokens.append(expression[i])

        if self.verbose:
            print(f"{expression} -> {tokens}")

        return tokens

    def precedence(self, op):
        if op == '+' or op == '-':
            return 1
        if op == '*' or op == '/':
            return 2
        return 0

    # Function to perform arithmetic operations.
    def applyOp(self, a, b, op):
        if op == '+': return a + b
        if op == '-': return a - b
        if op == '*': return a * b
        if op == '/': return a // b

    # Function that returns value of expression after evaluation.
    def evaluate(self, expression):
        tokens = self.tokenize(expression)
        values = [] # stack to store integers
        ops = [] # stack to store operators
        i = 0
        
        while i < len(tokens):            
            # Current token is an opening brace, push it to 'ops'
            if tokens[i] == '(':
                ops.append(tokens[i])
            
            elif ('d' in tokens[i]): # If token is a dice, evaluate and push it to stack for numbers
                print("dice")
            # Current token is a number, push it to stack for numbers.
            elif tokens[i].isdigit():
                values.append(tokens[i])

            # Closing brace encountered, solve entire brace.
            elif tokens[i] == ')':
                while len(ops) != 0 and ops[-1] != '(':
                    val2 = values.pop()
                    val1 = values.pop()
                    op = ops.pop()
                    values.append(self.applyOp(val1, val2, op))
                # pop opening brace.
                ops.pop()
            
            # Current token is an operator.
            else:
                # While top of 'ops' has same or greater precedence to current token, which is an operator. 
                # Apply operator on top of 'ops'  to top two elements in values stack.
                while (len(ops) != 0 and
                    self.precedence(ops[-1]) >=
                    self.precedence(tokens[i])):
                            
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
        
        # Top of 'values' contains result, return it.
        return values[-1]

# Driver Code
if __name__ == "__main__":
    sy = ShuntingYard(verbose = True)
    print(sy.evaluate("3+5"))

# This code is contributed
# by Rituraj Jain
