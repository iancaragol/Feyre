from os import path
from json import dumps
from .UserManager import UserManager
from .StatsManager import StatsManager
from copy import deepcopy
from ISStreamer.Streamer import Streamer
from discord.ext import commands
from discord.ext.tasks import loop

class DataManager:
    def __init__(self, bot, common, datadir):
        self.bot = bot
        self.common = common
        self.datadir = datadir

    async def save_to_disk(self):
        pyDir = path.dirname(__file__)
        relPath = self.datadir + "//stats.txt"
        absRelPath = path.join(pyDir, relPath)
        with open(absRelPath, 'w') as file:
            file.write(dumps(self.common.statsDict))

        relPath = self.datadir + "//prefixes.txt"
        absRelPath = path.join(pyDir, relPath)
        with open(absRelPath, 'w') as file:
            file.write(dumps(self.common.prefixDict))

        relPath = self.datadir + "//users.txt"
        absRelPath = path.join(pyDir, relPath)
        with open(absRelPath, 'w') as file:
            file.write(dumps(list(self.common.userSet)))

        relPath = self.datadir + "//gms.txt"
        absRelPath = path.join(pyDir, relPath)
        with open(absRelPath, 'w') as file:
            file.write(dumps(self.common.gmDict))

    async def save_to_mongo(self):
        um = UserManager(self.common.mongo_uri)
        um.dump_user_set(self.common.userSet)
        print("User set saved!")

        sm = StatsManager(self.common.mongo_uri)

        save_stats = deepcopy(self.common.statsDict)
        save_stats['user_count'] = len(self.common.userSet)
        save_stats['server_count'] = len(self.bot.guilds)
        save_stats['total_command_count'] = await self.bot.cogs.get('StatsCog').get_total_helper(self.common.statsDict)

        sm.dump_stats_dict(save_stats)
        print("Stats dictionary saved!")

    @commands.command()
    async def start_stream(self, ctx):
        if(ctx.author.id == 112041042894655488):
            await ctx.send("`Starting stream to Initial State`")
            self.send_data.start()

    @commands.command()
    async def stop_stream(self, ctx):
        if(ctx.author.id == 112041042894655488):
            await ctx.send("`Stopping stream to Initial State`")
            self.send_data.stop()

    #@loop(seconds=10)
    @loop(hours=12)
    async def save_data(self):
        print("Saving data to disk...")
        await self.save_to_disk()
        print("Saved!")
        print("Saving data in cloud...")
        await self.save_to_mongo()
        print("Saved!")

    @loop(seconds=300)
    async def send_data(self):
        stream_data = deepcopy(self.common.statsDict)
        stream_data['user_count'] = len(self.common.userSet)
        stream_data['server_count'] = len(self.bot.guilds)
        stream_data['total_command_count'] = await self.bot.cogs.get('StatsCog').get_total_helper(self.common.statsDict)

        streamer = Streamer(bucket_name="Feyre", bucket_key=self.common.bucket_key, access_key=self.common.access_key, buffer_size=200)
        streamer.log_object(stream_data)

        streamer.flush()
        streamer.close()