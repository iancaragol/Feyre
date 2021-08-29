import textwrap
import discord
import psutil

from ISStreamer.Streamer import Streamer
from discord.ext import commands
from discord.ext.tasks import loop
from _backend.UserManager import UserManager
from _backend.StatsManager import StatsManager
from _backend.PrefixesManager import PrefixManager
from _backend.GmManager import GmManager
from copy import deepcopy

class DeveloperCog(commands.Cog):
    def __init__(self, bot, data, stats_cog):
        self.bot = bot
        self.data = data
        self.stats_cog = stats_cog

    @commands.command()
    async def dump_users(self, ctx):
        if(ctx.author.id == 112041042894655488):
            um = UserManager(self.data.mongo_uri)
            await um.dump_user_set(self.data.userSet)
            await ctx.send("```Dumped!```")

    @commands.command()
    async def load_users(self, ctx):
        if(ctx.author.id == 112041042894655488):
            um = UserManager(self.data.mongo_uri)
            self.data.userSet = await um.get_user_set()
            await ctx.send("```Got!```")

    @commands.command()
    async def dump_stats(self, ctx):
        if(ctx.author.id == 112041042894655488):
            sm = StatsManager(self.data.mongo_uri)

            save_stats = deepcopy(self.data.statsDict)
            save_stats['user_count'] = len(self.data.userSet)
            save_stats['server_count'] = len(self.bot.guilds)
            save_stats['total_command_count'] = await self.bot.cogs.get('StatsCog').get_total_helper(self.data.statsDict)

            await sm.dump_stats_dict(save_stats)
            await ctx.send("```Dumped!```")

    @commands.command()
    async def load_stats(self, ctx):
        if(ctx.author.id == 112041042894655488): #112041042894655488
            sm = StatsManager(self.data.mongo_uri)
            temp = await sm.get_stats()
            self.data.statsDict = temp
            await ctx.send("```Got!```")

    @commands.command()
    async def dump_prefixes(self, ctx):
        if(ctx.author.id == 112041042894655488):
            pm = PrefixManager(self.data.mongo_uri)

            save_prefix = deepcopy(self.data.prefixDict)

            await pm.dump_prefix_dict(save_prefix)
            await ctx.send("```Dumped!```")

    @commands.command()
    async def load_prefixes(self, ctx):
        if(ctx.author.id == 112041042894655488): #112041042894655488
            pm = PrefixManager(self.data.mongo_uri)

            temp = await pm.get_prefix_dict()
            self.data.prefixDict = temp
            await ctx.send("```Got!```")

    @commands.command()
    async def dump_gms(self, ctx):
        if(ctx.author.id == 112041042894655488):
            gm = GmManager(self.data.mongo_uri)

            save_gm = deepcopy(self.data.gmDict)

            await gm.dump_gm_dict(save_gm)
            await ctx.send("```Dumped!```")

    @commands.command()
    async def load_gms(self, ctx):
        if(ctx.author.id == 112041042894655488): #112041042894655488
            gm = GmManager(self.data.mongo_uri)

            temp = await gm.get_gm_dict()
            self.data.gmDict = temp
            await ctx.send("```Got!```")
    
    @commands.command()
    async def change_presence(self, ctx, *, args):
        if(ctx.author.id == 112041042894655488):
            await ctx.send("Changing presence to: " + args)
            await self.bot.change_presence(activity = discord.Game(name=args))

    @commands.command()
    async def shards(self, ctx):
        if(ctx.author.id == 112041042894655488):
            msg = "```"
            for shard in self.bot.shards:
                msg += "\n"
                msg += "ID: {} | Count: {} | Latency: {}".format(shard, self.bot.get_shard(shard).shard_count, self.bot.get_shard(shard).latency)
            msg += "```"
            await ctx.send(msg)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('```Pong! {0}ms```'.format(round(self.bot.latency, 3)))

    
    @commands.command()
    async def cpu(self, ctx):
        cpu_percent = psutil.cpu_percent()
        virtual_mem = psutil.virtual_memory()._asdict()
        free_mem = virtual_mem['available']/float(1<<20) # Shift 20 places to get MB
        total_mem = virtual_mem['total']/float(1<<20)
        used_mem = total_mem - free_mem

        response = textwrap.dedent(
        """
        ```asciidoc
        cpu: {}%
        memory: {:,.0f}/{:,.0f} mb
        ```"""
        ).format(cpu_percent, used_mem, total_mem)

        await ctx.send(response)

    

    