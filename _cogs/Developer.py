import textwrap
import discord
import psutil

from ISStreamer.Streamer import Streamer
from discord.ext import commands
from discord.ext.tasks import loop
from _backend.UserManager import UserManager
from _backend.StatsManager import StatsManager
from copy import deepcopy

class DeveloperCog(commands.Cog):
    def __init__(self, bot, data, stats_cog):
        self.bot = bot
        self.data = data
        self.stats_cog = stats_cog

    @commands.command()
    async def dump_user_mongo(self, ctx):
        if(ctx.author.id == 112041042894655488):
            um = UserManager()
            um.dump_user_set(self.data.userSet)
            await ctx.send("```Dumped!```")

    @commands.command()
    async def load_user_mongo(self, ctx):
        if(ctx.author.id == 112041042894655488):
            um = UserManager()
            self.data.userSet = um.get_user_set()
            await ctx.send("```Got!```")

    @commands.command()
    async def dump_stats_mongo(self, ctx):
        if(ctx.author.id == 112041042894655488):
            sm = StatsManager()

            save_stats = deepcopy(self.data.statsDict)
            save_stats['user_count'] = len(self.data.userSet)
            save_stats['server_count'] = len(self.bot.guilds)
            save_stats['total_command_count'] = self.bot.cogs.get('StatsCog').get_total_helper(self.data.userSet)

            sm.dump_stats_dict(save_stats)
            await ctx.send("```Dumped!```")

    @commands.command()
    async def load_stats_mongo(self, ctx):
        if(ctx.author.id == 112041042894655488):
            sm = StatsManager()
            temp = sm.get_stats()
            self.data.statsDict = temp
            await ctx.send("```Got!```")
    
    @commands.command()
    async def change_presence(self, ctx, *, args):
        if(ctx.author.id == 112041042894655488):
            await ctx.send("Changing presence to: " + args)
            await self.bot.change_presence(activity = discord.Game(name=args))

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('```Pong! {0}ms```'.format(round(self.bot.latency, 3)))

    
    @commands.command()
    async def cpu(self, ctx):
        cpu_percent = psutil.cpu_percent()
        virtual_mem = psutil.virtual_memory()._asdict()
        free_mem = virtual_mem['available']/float(1<<20) # Shift 20 places to get MB
        total_mem = virtual_mem['total']/float(1<<20)

        response = textwrap.dedent(
        """
        ```asciidoc
        cpu: {}%
        memory: {:,.0f}/{:,.0f} mb
        ```"""
        ).format(cpu_percent, free_mem, total_mem)

        await ctx.send(response)

    

    