import random
import asyncio
import re
import copy
import numpy as np
import math
from asteval import Interpreter

aeval = Interpreter()

#rolls dice
#accepts input in the form of !roll #dTYPE ex: !roll 1d20 + 5
class Roller():
    async def parse(self, inp, gm = False):
        """
        Parses a string of the format !roll #d# +,/,*,- #d# or # ... evaulated 
        Ex: !roll 5d20 + 1d6 * 2
        Returns an invalid input message if the input is not recongnized.
        """
        #try:
            #TODO: Fix this spaget
        advantage = False
        disadvantage = False
        inp = inp.lower().strip()
        inp = inp.replace('\\','')
        if(inp.startswith('-a')):
            advantage = True
            inp = inp.replace('-a', '').strip()

        if(inp.startswith('-d')):
            disadvantage = True
            inp = inp.replace('-d', '').strip()

        #check formatting
        illegal = "abcefghijklmnopqrstuvwxyz!,[]|&"
        inp = inp.replace(' ', '')
        m = re.match(r"^((\d*)d(\d*)([-+*/><]?\d*))*", inp)
    
        #sanitize inp
        sanitize = any(c in inp.lower() for c in illegal)

        if(sanitize == True):
            return "```I'm sorry, there was something I didnt understand about your input. See !help roll for more info```"

        ms = re.split(r"([-+*/><])", m.string)
        adv = copy.deepcopy(ms)

        rollExp = copy.deepcopy(ms)

        for i in range(0, len(ms)):
            if (re.match(r"^((\d*)d(\d*))", ms[i])):
                split = ms[i].split('d')
                try:
                    numDice = int(split[0])

                except ValueError:
                    numDice = int(1)

                typeDice = int(split[1])

                if(numDice > 100000):
                    return "Your inp is too big! Maximum number of dice is 100,000"

                if(typeDice > 9223372036854775808):
                    return ("Your inp is too big! Maximum size is 9,223,372,036,854,775,807")


                ms[i] = self.rollDice(numDice, typeDice)
                if(advantage or disadvantage):
                    adv[i] = self.rollDice(numDice, typeDice)
       
        unEval = copy.deepcopy(ms)
        if(advantage or disadvantage):
            unEvalAdv = copy.deepcopy(adv)
            evalledAdv = adv

        evalled = ms
        
        for i in range(0, len(ms)):
            try:
                evalled[i] = sum(ms[i])
            except:
                continue

        if(advantage or disadvantage):
            for i in range(0, len(adv)):
                try:
                    evalledAdv[i] = sum(adv[i])
                except:
                    continue
            unEvalStrAdv = ''.join(str(e) for e in unEvalAdv)
            evalStrAdv = ''.join(str(e) for e in evalledAdv)
            totalAdv = aeval(evalStrAdv)
            
        unEvalStr = ''.join(str(e) for e in unEval)
        evalStr = ''.join(str(e) for e in evalled)
        rollExpStr = ''.join(str(e) for e in rollExp)
        total = aeval(evalStr)

        if(advantage or disadvantage):
            return self.constructReturnStringAdvantage(advantage, disadvantage, rollExpStr, unEvalStr, unEvalStrAdv, total, totalAdv)

        if(not gm):
            return self.constructReturnString(rollExpStr, unEvalStr, total)
        if(gm and not advantage or not disadvantage):
            return self.constructReturnStringNoFormat(rollExpStr, unEvalStr, total)
        

        #except Exception as e:
            #return ("*I'm sorry, there was something I didnt understand about your inp.*\n" + str(e))

    def constructReturnStringAdvantage(self, adv, disadv, rES, uES, uES2, t1, t2):
        """
        Constructs the return string where rES is the original expression, uES is the expression with all rolls, and t is the total
        """
        if(len(uES) > 100 or len(uES2) > 100):
            uES = "Omitted (# of dice was too large)"

        if(adv):
            outMsg = f'''```diff
I interpreted your inp as {rES} with advantage.
Totals: [{t1}] & [{t2}]
- You rolled [{max(t1, t2)}] with advantage -```'''

            return outMsg

        elif(disadv):
            outMsg = f'''```diff
I interpreted your inp as {rES} with disadvantage.
Totals: [{t1}] & [{t2}]
- You rolled [{min(t1, t2)}] with disadvantage -```'''

            return outMsg

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

    def constructReturnStringNoFormat(self,rES, uES, t):
        """
        Constructs the return string where rES is the original expression, uES is the expression with all rolls, and t is the total
        """
        if(len(uES) > 100):
            uES = "Omitted (# of dice was too large)"

        if(type(t) is bool):
            if(t):
                outMsg = f'''I interpreted the input as {rES}.
Rolls: {uES}
[Ability/Skill Check: Succeeded]'''
            else:
                outMsg = f'''I interpreted the input as {rES}.
Rolls: {uES}
[Ability/Skill Check: Failed]'''

        else:
            outMsg = f'''
I interpreted the input as {rES}.
Rolls: {uES}
[Total: {t}]'''

        return outMsg

    def rollDice(self, numDice, typeDice):
        """
        Rolls a number of dice (numDice) of type (typeDice) and returns the rolls as a list.
        """
        rolls = np.random.randint(1,typeDice+1,numDice, dtype=np.int64)     
        return list(rolls)