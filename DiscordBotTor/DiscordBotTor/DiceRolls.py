import random

class Roller():
    def roll(self, input):
        outMsg = ""
        try:   
            #split to parse out !roll
            split = input.lower().split(' ')
            tmp = str(split[1])

            findType = tmp.split('d')
            #number of dice
            numDice = int(findType[0])
            #type of dice
            typeDice = int(findType[1])


            outMsg = outMsg + f"Interperted as rolling [{findType[0]}] dice of size [{findType[1]}]\n"

            total = 0
            for i in range(0, numDice):
                roll = random.randint(1, typeDice)
                total += roll
                outMsg = outMsg + f"[{roll}] "

            outMsg += f"\n**Total: {total}**"
          
        except:
            outMsg = "*I'm sorry. There was something that I did not understand in your command. Please contact <@112041042894655488> so we can resolve this issue.*"
             
        return outMsg

