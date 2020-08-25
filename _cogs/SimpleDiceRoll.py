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

    @commands.command()
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

    @commands.command()
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

    @commands.command()
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

    @commands.command()
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

    @commands.command()
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

    @commands.command()
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

    @commands.command()
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

    @commands.command()
    async def Dp(self, ctx, *, args = None):
        await self.dp(ctx, args = args)

    @commands.command()
    async def D20(self, ctx, *, args = None):
        await self.d20(ctx, args = args)

    @commands.command()
    async def D12(self, ctx, *, args = None):
        await self.d12(ctx, args = args)

    @commands.command()
    async def D10(self, ctx, *, args = None):
        await self.d10(ctx, args = args)

    @commands.command()
    async def D8(self, ctx, *, args = None):
        await self.d8(ctx, args = args)

    @commands.command()
    async def D6(self, ctx, *, args = None):
        await self.d6(ctx, args = args)

    @commands.command()
    async def D4(self, ctx, *, args = None):
        await self.d4(ctx, args = args)