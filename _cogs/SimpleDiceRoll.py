import textwrap
import discord
import random
from asteval import Interpreter
from discord.ext import commands

class SimpleDiceRoller(commands.Cog):
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
        self.aeval = Interpreter()

    @commands.command(aliases = ['Dp'])
    async def dp(self, ctx, *, args = None):
        self.data.statsDict['!roll'] += 1

        try:
            roll = str(random.randint(1, 100))
            if(args):
                total = self.aeval(roll + args.strip())
                msg = f'''```css\n{roll}{args.replace(' ', '')} = [{"%.2g" % total}%]```'''

            else:
                total = roll
                msg = f'''```asciidoc\n[{total}%]```'''

        except:
            msg = f'''```I didn't understand something about your input. Try !roll for more complicated expressions.```'''

        await ctx.send(msg)

    @commands.command(aliases = ['D20'])
    async def d20(self, ctx, *, args = None):
        self.data.statsDict['!roll'] += 1

        try:
            roll = str(random.randint(1, 20))
            if(args):
                total = self.aeval(roll + args.strip())
                msg = f'''```css\n{roll}{args.replace(' ', '')} = [{"%.2g" % total}]```'''

            else:
                total = roll
                msg = f'''```asciidoc\n[{total}]```'''

        except:
            msg = f'''```I didn't understand something about your input. Try !roll for more complicated expressions.```'''

        await ctx.send(msg)

    @commands.command(aliases = ['D12'])
    async def d12(self, ctx, *, args = None):
        self.data.statsDict['!roll'] += 1

        try:
            roll = str(random.randint(1, 12))
            if(args):
                total = self.aeval(roll + args.strip())
                msg = f'''```css\n{roll}{args.replace(' ', '')} = [{"%.2g" % total}]```'''

            else:
                total = roll
                msg = f'''```asciidoc\n[{total}]```'''

        except:
            msg = f'''```I didn't understand something about your input. Try !roll for more complicated expressions.```'''

        await ctx.send(msg)

    @commands.command(aliases = ['D10'])
    async def d10(self, ctx, *, args = None):
        self.data.statsDict['!roll'] += 1

        try:
            roll = str(random.randint(1, 10))
            if(args):
                total = self.aeval(roll + args.strip())
                msg = f'''```css\n{roll}{args.replace(' ', '')} = [{"%.2g" % total}]```'''

            else:
                total = roll
                msg = f'''```asciidoc\n[{total}]```'''

        except:
            msg = f'''```I didn't understand something about your input. Try !roll for more complicated expressions.```'''

        await ctx.send(msg)

    @commands.command(aliases = ['D8'])
    async def d8(self, ctx, *, args = None):
        self.data.statsDict['!roll'] += 1

        try:
            roll = str(random.randint(1, 8))
            if(args):
                total = self.aeval(roll + args.strip())
                msg = f'''```css\n{roll}{args.replace(' ', '')} = [{"%.2g" % total}]```'''

            else:
                total = roll
                msg = f'''```asciidoc\n[{total}]```'''

        except:
            msg = f'''```I didn't understand something about your input. Try !roll for more complicated expressions.```'''

        await ctx.send(msg)

    @commands.command(aliases = ['D6'])
    async def d6(self, ctx, *, args = None):
        self.data.statsDict['!roll'] += 1

        try:
            roll = str(random.randint(1, 6))
            if(args):
                total = self.aeval(roll + args.strip())
                msg = f'''```css\n{roll}{args.replace(' ', '')} = [{"%.2g" % total}]```'''

            else:
                total = roll
                msg = f'''```asciidoc\n[{total}]```'''

        except:
            msg = f'''```I didn't understand something about your input. Try !roll for more complicated expressions.```'''

        await ctx.send(msg)

    @commands.command(aliases = ['D4'])
    async def d4(self, ctx, *, args = None):
        self.data.statsDict['!roll'] += 1

        try:
            roll = str(random.randint(1, 4))
            if(args):
                total = self.aeval(roll + args.strip())
                msg = f'''```css\n{roll}{args.replace(' ', '')} = [{"%.2g" % total}]```'''

            else:
                total = roll
                msg = f'''```asciidoc\n[{total}]```'''

        except:
            msg = f'''```I didn't understand something about your input. Try !roll for more complicated expressions.```'''

        await ctx.send(msg)