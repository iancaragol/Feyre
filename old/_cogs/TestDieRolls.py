import random
import asyncio
import re
import copy
import numpy as np
import math
from asteval import Interpreter
import discord
import json
import re

from discord.ext import commands
from _classes.DiceRollerV2 import ShuntingYard

class TESTDiceRoller(commands.Cog):
    # Very Temporary!

    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
        self.shunting_yard = ShuntingYard()

    @commands.command(aliases = ['TestRoll', 'tr', 'TR'])
    async def troll(self, ctx, *, args = None):

        # Parse user provided message
        if args:
            # Get the @
            at_string, args = await self.parse_ats_helper(ctx.author, args)
            expression, user_msg = await self.parse_user_msg_helper(args)

            roll_results = json.loads(await self.shunting_yard.shunt(expression))

            # TEMP RETURN JSON FIRST ITEM
            #msg = await ctx.send(str(roll_results['parent_result']).replace('\'', '"'))
            response_str = await self.construct_response(roll_results, user_msg, at_string)    

            #embed = discord.Embed(description = response_str, color = self.data.embedcolor)
            #send_msg = await ctx.send(embed = embed)   
            send_msg = await ctx.send(response_str)
            
            # Add emoji to roll
            reroll_emoji = '🔁'
            await send_msg.add_reaction(reroll_emoji)
            await self.reroll_helper(ctx, args, response_str, send_msg, user_msg)

    async def construct_response(self, roll_results_json, user_msg, at_string):
        # Dynamically construct the message to send
        msg_str = ""

        # At the user first
        if len(at_string) > 0:
            msg_str += at_string.strip() + " "

        # Then write their message
        if len(user_msg) > 0:
            msg_str += user_msg.strip() + "\n"

        # Parent result contains a list of child_results which are individual rolls
        # So 1d6+1d20 contains the total and the child results are 1d6 and 1d20
        # Roll_results is a list of rolls so if the counter modifier is used then
        # There will be count # of roll_results
        for roll in roll_results_json['parent_result']: 
            total = roll['total']
            expression = roll['expression'] # 1d20+1d6+6
            for child_roll in roll['child_rolls']:
                replacement_str = ""
                 
                replacement_str += str(child_roll['rolls'][:10]).replace("[", "").replace("]", "") # Strips [ ]
                replacement_str += ", " # This is stripped if its the last entry
                if (len(child_roll['rolls']) > 10):
                    replacement_str += "..."
                # Cross out dropped dice
                if (len(child_roll['dropped']) > 0):
                    replacement_str += "~~"
                    replacement_str += str(child_roll['dropped'][:10]).replace("[", "").replace("]", "")
                    replacement_str += "~~"
                    if (len(child_roll['dropped']) > 10):
                        replacement_str += "..."
                # Bold exploded dice
                if (len(child_roll['exploded']) > 0):
                    replacement_str += "**"
                    replacement_str += str(child_roll['exploded'][:10]).replace("[", "").replace("]", "")
                    replacement_str += "**"
                    if (len(child_roll['exploded']) > 10):
                        replacement_str += "..."

                replacement_str = "[" + replacement_str.strip().rstrip(',') + "]" # Add brackets back
                expression = expression.replace(child_roll['expression'], replacement_str) # [7]+[3]+6
            if (len(roll_results_json['parent_result']) > 1): # There is a count
                msg_str += expression[:-expression.index('c')] + ']'
            else:
                msg_str += expression
            msg_str += " => "
            msg_str += f"**{total}**"
            msg_str += "\n" # Newline for if count was used

        msg_str.strip()
        return msg_str

    async def parse_user_msg_helper(self, message):
        # Returns a tuple with the dice expressionand # message
        split = message.split('#') # Everything after this is the message
        user_msg = "".join(split[1:])
        expression = split[0]
        return expression, user_msg

    async def parse_ats_helper(self, author, message):
        # Takes a message and gets all @ messages from it
        # Removes all of the @ messages from the original
        at_string = ""
        if '@' in message:
            # At messages look like this: '<@!112041042894655488>'
            match = re.findall(r'(?<=\<).+?(?=\>)', message)
            if match:
                for m in match:
                    temp = '<' + m + '>' # I am bad at regex, so add these back
                    message = message.replace(temp, '') # Remove the at_string
                    at_string += temp + '  '
            else: # If only the @ is included, we only @ the person who rolled
                at_string = '<@!' + str(author.id) + '>'
                message = message.replace('@', '') # Remove the at_string
        return at_string, message


    async def reroll_helper(self, ctx, args, roll_msg, msg, user_msg):
        try:
            print("REROLL HELPER")
            reaction, u = await self.bot.wait_for('reaction_add', check=lambda r, u:str(r.emoji) == '🔁' and u.id != self.bot.user.id and r.message.id == msg.id, timeout=1800) # Times out after (1800s) 30 minutes

            if reaction != None:
                at_string, args = await self.parse_ats_helper(ctx.author.id, args)
                args, user_msg = await self.parse_user_msg_helper(args)
                roll_results = json.loads(await self.shunting_yard.shunt(args))
                response_str = await self.construct_response(roll_results, user_msg, at_string)
                if ctx.channel.type is discord.ChannelType.private:
                    await msg.delete()
                    msg = await ctx.send(response_str)
                    await msg.add_reaction('🔁')
                else:
                    await msg.edit(content=roll_msg)
                    await reaction.remove(u)
                await self.reroll_helper(ctx, args, response_str, msg, user_msg)
        
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
            else:
                raise e