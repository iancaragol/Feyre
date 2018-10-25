import random
import asyncio
import re
import copy

#rolls dice
#accepts input in the form of !roll #dTYPE ex: !roll 1d20 + 5
class Roller():

    async def parse(self, input):
        input = input.lower()
        diceExpression = input.replace(' ', '')[5:]
        m = re.match(r"^((\d*)d(\d*)([-+*/]?\d*))*", diceExpression)

        ms = re.split(r"([-+*/])", m.string)
        rollExp = copy.deepcopy(ms)

        for i in range(0, len(ms)):
            if (re.match(r"^((\d*)d(\d*))", ms[i])):
                split = ms[i].split('d')
                numDice = int(split[0])
                typeDice = int(split[1])
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

        print(unEval)
        print(eval)
        print(evalStr)
        print(total)

        return self.constructReturnString(rollExpStr, unEvalStr, total)

    def constructReturnString(self, rES, uES, t):
        outMsg = f'''*I interperted your input as {rES}.*
Rolls: {uES}
**Total:** {t}'''
        return outMsg


    def rollDice(self, numDice, typeDice):
        rolls = [0]*numDice           
        for i in range(0, numDice):
            roll = random.randint(1, typeDice)
            rolls[i] = roll
         
        return rolls

    async def roll(self, input):
        outMsg = ""
        try:   
            #split to parse out !roll
            split = []
            split.append(input[:5])

            #find d
            di = 0
            #find +, -, *, /
            ei = 0

            for i in range(0, len(input)):
                if(input[i] == 'd' or input[i] == 'D'):
                    di = i-1
                if(input[i] == '+' or input[i] == '-' or input[i] == '*' or input[i] == '/'):
                    ei = i
                    break

            if(ei != 0):
                tmp = input[di:ei]
            else:
                tmp = input[di:]

            findType = tmp.split('d')
            findType[0] = findType[0].strip()
            findType[1] = findType[1].strip()
            #number of dice
            numDice = int(findType[0])
            #type of dice
            typeDice = int(findType[1])

            mod = ''
            if(ei < len(input) and ei != 0):
                mod = input[ei:].strip()

            outMsg = outMsg + f"I interperted this as rolling [{findType[0]}] dice of size [{findType[1]}] with a modifier of [{mod}]"

            rolls = [0]*numDice           
            for i in range(0, numDice):
                roll = random.randint(1, typeDice)
                rolls[i] = roll

            total = sum(rolls)
            totalStr = str(total)
        
            evalStr = totalStr + mod
            finalTotal = eval(evalStr)

            if(mod!= ''):
                outMsg += f"\nRoll(s): {rolls} {mod}"
            else:
                outMsg += f"\nRoll(s): {rolls}"

            outMsg += f"\n**Total: {finalTotal}**"
         
        #invalid input     
        except Exception as e:
          #   print(e)
          outMsg = "*I'm sorry. There was something that I did not understand in your command. Please contact <@112041042894655488> so we can resolve this issue.*"
             
        return outMsg

