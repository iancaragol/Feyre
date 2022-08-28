import random
import asyncio
import re
import copy
import numpy as np
import math
from asteval import Interpreter
import discord

from discord.ext import commands

aeval = Interpreter()

#rolls dice
#accepts input in the form of !roll #dTYPE ex: !roll 1d20 + 5
class DiceRoll():
    async def parse(self, inp, gm = False, total_only = False):
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

        ms = re.split(r"([-+*/()><])", m.string)
        ms = list(filter(None, ms)) #remove any empty strings that could cause issues
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

        if total_only:
            return total

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
I interpreted your input as {rES} with advantage.
Totals: [{t1}] & [{t2}]
- You rolled [{max(t1, t2)}] with advantage -```'''

            return outMsg

        elif(disadv):
            outMsg = f'''```diff
I interpreted your input as {rES} with disadvantage.
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
                outMsg = f'''**FEYRE HAS MOVED TO SLASH COMMANDS**

**!roll** is no longer supported, you can use **/roll** instead

See **https://docs.feyre.io** for more information or **!update.**'''
            else:
                outMsg = f'''***FEYRE HAS MOVED TO SLASH COMMANDS**

**!roll** is no longer supported, you can use **/roll** instead

See **https://docs.feyre.io** for more information or **!update.**
'''

        elif float(t).is_integer():
            outMsg = f'''**FEYRE HAS MOVED TO SLASH COMMANDS**

**!roll** is no longer supported, you can use **/roll** instead

See **https://docs.feyre.io** for more information or **!update.**'''

        else:
            outMsg = f'''**FEYRE HAS MOVED TO SLASH COMMANDS**

**!roll** is no longer supported, you can use **/roll** instead

See **https://docs.feyre.io** for more information or **!update.**'''

        return outMsg

    def constructReturnStringNoFormat(self,rES, uES, t):
        """
        Constructs the return string where rES is the original expression, uES is the expression with all rolls, and t is the total
        """
        if(len(uES) > 100):
            uES = "Omitted (# of dice was too large)"

        if(type(t) is bool):
            if(t):
                outMsg = f'''I interpreted your input as {rES}.
Rolls: {uES}
[Ability/Skill Check: Succeeded]'''
            else:
                outMsg = f'''I interpreted your input as {rES}.
Rolls: {uES}
[Ability/Skill Check: Failed]'''

        elif float(t).is_integer():
            outMsg = f'''
I interpreted your input as {rES}.
Rolls: {uES}
- Total: {t} -'''

        else:
            outMsg = f'''
I interpreted your input as {rES}.
Rolls: {uES}
- Total: {"%.2f" % t} -'''

        return outMsg

    def rollDice(self, numDice, typeDice):
        """
        Rolls a number of dice (numDice) of type (typeDice) and returns the rolls as a list.
        """
        rolls = np.random.randint(1,typeDice+1,numDice, dtype=np.int64)     
        return list(rolls)

class DiceRoller(commands.Cog):
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
        self.dice_roll = DiceRoll()

    @commands.command(aliases = ['Gm'])
    async def gm(self, ctx, *, args = None):
        self.data.userSet.add(ctx.author.id)
        self.data.statsDict['!gm'] += 1

        if (ctx.guild == None):
            await ctx.send("```GM rolls must be done in a channel with a dedicated gm.```")
            return

        elif (args == None):
            self.data.gmDict[ctx.channel.id] = ctx.author.id
            await ctx.send(f"```{ctx.author} was made GM of this channel.```")

        elif (args != None):
            args = args.strip()
            if (args.startswith('roll')):
                try:
                    expression = args.replace('roll', '').strip()
                    result = await self.dice_roll.parse(expression, gm = True)

                    gmUser = self.bot.get_user(self.data.gmDict[ctx.channel.id])
                    gmResult = f'''```diff
    Roll from [{ctx.author.name}]
    {result} ```'''

                    await gmUser.send(gmResult)

                    userResult = f'''```diff
    {result}```'''
                    sendUser = self.bot.get_user(ctx.author.id)
                    await sendUser.send(userResult)
                except:
                    await ctx.send("```This channel does not have a dedicated GM. Type !gm to set yourself as GM.```")

    @commands.command(aliases = ['Roll', 'r', 'R'])
    async def roll(self, ctx, *, args = None):
        """
        Rolls any number of dice in any format including skill checks
            Ex: !roll 1d20+5*6>100
        """
        if (ctx.author.id not in self.data.userSet):
            self.data.userSet.add(ctx.author.id)
        self.data.statsDict['!roll'] += 1

        if not args:
            await ctx.send('''```Missing command arguments, see !help roll for more information.\nEx: !roll 1d20+5```''')
            return

        roll_msg = await self.dice_roll.parse(args, gm = False)
        msg = await ctx.send(roll_msg)

        # Add emoji to roll
        arrows = '🔁'
        await msg.add_reaction(arrows)
        await self.reroll_helper(ctx, args, roll_msg, msg)
        

    async def reroll_helper(self, ctx, args, roll_msg, msg):
        try:
            reaction, u = await self.bot.wait_for('reaction_add', check=lambda r, u:str(r.emoji) == '🔁' and u.id != self.bot.user.id and r.message.id == msg.id, timeout=21600) # Times out after 6 hours

            if reaction != None:
                self.data.statsDict['rerolls'] += 1
                roll_msg = await self.dice_roll.parse(args, gm = False)
                if ctx.channel.type is discord.ChannelType.private:
                    await msg.delete()
                    msg = await ctx.send(roll_msg)
                    await msg.add_reaction('🔁')
                else:
                    await msg.edit(content=roll_msg)
                    await reaction.remove(u)
                await self.reroll_helper(ctx, args, roll_msg, msg)
        
        except Exception as e:
            if type(e) is asyncio.TimeoutError:
                if ctx.channel.type is discord.ChannelType.private:
                        contents = msg.content
                        await msg.delete()
                        await ctx.send(contents)
                else:
                    await msg.clear_reaction('🔁')

            elif type(e) is discord.errors.Forbidden:
                contents = msg.content
                contents = contents.rstrip("```")
                contents += "\n\nThe Manage Messages Permission is needed to use the reroll emoji. See !permissions for help.```"
                await msg.edit(content=contents)