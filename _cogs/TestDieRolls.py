import random
import asyncio
import re
import copy
import numpy as np
import math
from asteval import Interpreter
import discord
import json

from discord.ext import commands
from _classes.DieQueue import ShuntingYard
from _classes.DieQueue import RollFormatter

class TESTDiceRoller(commands.Cog):
    # Very Temporary!

    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
        self.shunting_yard = ShuntingYard()
        self.roll_formatter = RollFormatter()

    @commands.command(aliases = ['TestRoll', 'tr', 'TR'])
    async def troll(self, ctx, *, args = None):
        roll_results = json.loads(await self.shunting_yard.shunt(args))

        # TEMP RETURN JSON FIRST ITEM
        msg = await ctx.send(str(roll_results['parent_result'][0]).replace('\'', '"'))

        # Add emoji to roll
        arrows = '🔁'
        await msg.add_reaction(arrows)
        await self.reroll_helper(ctx, args, formatted_msg, msg)

    async def reroll_helper(self, ctx, args, roll_msg, msg):
        try:
            reaction, u = await self.bot.wait_for('reaction_add', check=lambda r, u:str(r.emoji) == '🔁' and u.id != self.bot.user.id and r.message.id == msg.id, timeout=21600) # Times out after 6 hours

            if reaction != None:
                roll = await self.shunting_yard.shunt(args)
                formatted_msg = await self.roll_formatter.format_roll(roll)
                if ctx.channel.type is discord.ChannelType.private:
                    await msg.delete()
                    msg = await ctx.send(formatted_msg)
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