import random
import asyncio
import re
import copy
import numpy as np

#rolls dice
#accepts input in the form of !roll #dTYPE ex: !roll 1d20 + 5
class Roller():
    async def parse(self, input):
        """
        Parses a string of the format !roll #d# +,/,*,- #d# or # ... evaulated 
        Ex: !roll 5d20 + 1d6 * 2
        Returns an invalid input message if the input is not recongnized.
        """
        try:
            input = input.lower()
            input = input.replace('\\','')
            #check formatting
            m = re.match(r"^((\d*)d(\d*)([-+*/><]?\d*))*", input)

            if(m == None):
                return "*I'm sorry, there was something I didnt understand about your input.*"

            ms = re.split(r"([-+*/><])", m.string)

            rollExp = copy.deepcopy(ms)

            for i in range(0, len(ms)):
                if (re.match(r"^((\d*)d(\d*))", ms[i])):
                    split = ms[i].split('d')
                    numDice = int(split[0])
                    typeDice = int(split[1])

                    if(numDice > 100000):
                        return "Your input is too big! Maximum number of dice is 100,000"

                    if(typeDice > 9223372036854775808):
                        return ("Your input is too big! Maximum size is 9,223,372,036,854,775,808")


                    ms[i] = self.rollDice(numDice, typeDice)
       
            unEval = copy.deepcopy(ms)
            evalled = ms

            for i in range(0, len(ms)):
                try:
                    evalled[i] = sum(ms[i])
                except:
                    continue

            
            unEvalStr = ''.join(str(e) for e in unEval)
            evalStr = ''.join(str(e) for e in evalled)
            rollExpStr = ''.join(str(e) for e in rollExp)
            total = eval(evalStr)

            return self.constructReturnString(rollExpStr, unEvalStr, total)
        except Exception as e:
            return ("*I'm sorry, there was something I didnt understand about your input.*\n" + str(e))

 

    def constructReturnString(self,rES, uES, t):
        """
        Constructs the return string where rES is the original expression, uES is the expression with all rolls, and t is the total
        """
        if(len(uES) > 100):
            uES = "Omitted (# of dice was too large)"

        if(type(t) is bool):
            if(t):
                outMsg = f'''```diff
I interpreted your input as {rES}.
Rolls: {uES}
- Ability/Skill Check: Succeeded -```'''
            else:
                outMsg = f'''```diff
I interpreted your input as {rES}.
Rolls: {uES}
- Ability/Skill Check: Failed -```'''

        else:
            outMsg = f'''```diff
I interpreted your input as {rES}.
Rolls: {uES}
- Total: {t} -```'''

        return outMsg

    def rollDice(self, numDice, typeDice):
        """
        Rolls a number of dice (numDice) of type (typeDice) and returns the rolls as a list.
        """
        rolls = np.random.randint(1,typeDice+1,numDice, dtype=np.int64)     
        return list(rolls)