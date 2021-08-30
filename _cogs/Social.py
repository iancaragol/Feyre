import discord
from discord.ext import commands

class SocialCog(commands.Cog):
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data

    @commands.command(aliases = ['Vote'])
    async def vote(self, ctx,  *, args = None):
        self.data.userSet.add(ctx.author.id)
        self.data.statsDict['!vote'] += 1

        embed = discord.Embed(description="If you have a moment, please [vote](https://top.gg/bot/500733845856059402) for Feyre on top.gg! This helps more people find the bot. Thanks :)")
        embed.set_image(url='https://media.giphy.com/media/zGnnFpOB1OjMQ/giphy.gif')
        await ctx.send(embed = embed)

    @commands.command(aliases = ['Invite'])
    async def invite(self, ctx,  *, args = None):
        embed = discord.Embed(title="Invite Feyre to your Server", description="Share Feyre with your friends!\n\nhttps://discord.com/oauth2/authorize?client_id=500733845856059402&scope=bot&permissions=75840")
        await ctx.send(embed = embed)
    
    @commands.command(aliases = ['Hello'])
    async def hello(self, ctx):
        """
        Hi!
        """
        self.data.userSet.add(ctx.author.id)
        self.data.statsDict['!hello'] += 1

        embed = discord.Embed()
        embed.set_image(url='https://cdn.discordapp.com/attachments/401837411291627524/538476988357148675/hello.gif')
        await ctx.send(embed=embed)
    
