import random
import asyncio
import re
import copy

#rolls dice
#accepts input in the form of !roll #dTYPE ex: !roll 1d20 + 5
class Roller():
    async def BotParse(self, input):
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
                    if(numDice >= 1000 and typeDice >= 100):
                        return "*I'm sorry but that input is too big.*"
                    if(numDice >= 100 and typeDice >= 10000):
                        return "*I'm sorry but that input is too big.*"
                    if(numDice >= 100000):
                        return "*I'm sorry but that input is too big.*"
                    if(typeDice >= 100000000000):
                        return "*I'm sorry but that input is too big.*"

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

    async def parse(self, input):
        """
        Parses a string of the format !roll #d# +,/,*,- #d# or # ... evaulated 
        Ex: !roll 5d20 + 1d6 * 2
        Returns an invalid input message if the input is not recongnized.
        """
        try:
            input = input.lower()
            diceExpression = input.replace(' ', '')[5:] #remove !roll
            #check formatting
            m = re.match(r"^((\d*)d(\d*)([-+*/><]?\d*))*", diceExpression)

            if(m == None):
                return "*I'm sorry, there was something I didnt understand about your input.*"

            ms = re.split(r"([-+*/><])", m.string)

            rollExp = copy.deepcopy(ms)

            for i in range(0, len(ms)):
                if (re.match(r"^((\d*)d(\d*))", ms[i])):
                    split = ms[i].split('d')
                    numDice = int(split[0])
                    typeDice = int(split[1])
                    if(numDice >= 1000 and typeDice >= 10000):
                        return "*I'm sorry but that input is too big.*"
                    if(numDice >= 100000):
                        return "*I'm sorry but that input is too big.*"
                    if(typeDice >= 100000000000):
                        return "*I'm sorry but that input is too big.*"

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
        if(type(t) is bool):
            if(t):
                outMsg = f'''I interperted your input as {rES}.
Rolls: {uES}
**Ability/Skill Check**: Succeeded'''
            else:
                outMsg = f'''I interperted your input as {rES}.
Rolls: {uES}
**Ability/Skill Check**: Failed'''

        else:
            outMsg = f'''I interperted your input as {rES}.
Rolls: {uES}
**Total:** {t}'''

        return outMsg

    def rollDice(self, numDice, typeDice):
        """
        Rolls a number of dice (numDice) of type (typeDice) and returns the rolls as a list.
        """
        rolls = [0]*numDice           
        for i in range(0, numDice):
            roll = random.randint(1, typeDice)
            rolls[i] = roll
         
        return rolls