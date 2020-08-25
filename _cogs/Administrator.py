import textwrap
import discord
from discord.ext import commands


class Administrator(commands.Cog):
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data

    @commands.command()
    async def admin(self, ctx):
        if (ctx.author.id not in self.data.userSet):
            self.data.userSet.add(ctx.author.id)
        self.data.statsDict['!admin'] += 1

        retstr = '''```!admin is for server administrators. Currently the only command available to adminstrators is !set_prefix.

Commands:
!set_prefix [prefix]
    > Sets the server wide prefix to [prefix]. 
    Prefix must be ?, /, !, ~, `, #, $, %, ^, &, *, ,, ., ;, :, <, or >
Note: If you forget the bot's prefix you will no longer be able to summon it and reset it's prefix.
For this reason, the prefix will be pinned in the channel from which it is changed.```'''

        await ctx.send(retstr)

    @commands.command()
    async def set_prefix(self, ctx, *, args = None):
        #TO DO:
        #Support pinging bot if you do not know the prefix
        #Removing bot from server should reset bot's prefix
        if (ctx.author.id not in self.data.userSet):
            self.data.userSet.add(ctx.author.id)
        self.data.statsDict['!set_prefix'] += 1

        if(not hasattr(ctx.author, 'ctx.author.guild_permissions')):
            await ctx.send(f"This command is for server use only.")

        if args:
            args = args.strip()

            if(ctx.author.guild_permissions.administrator):
                possibleArgs = set(['?','/','!','~','`','#','$','%','^','&','*',',','.',';',':','>','<'])

                if(len(args) < 1):
                    await ctx.send(f"<@{ctx.author.id}>\n You must include arguments! Ex: !set_prefix &")
                    return

                elif (args not in possibleArgs):
                    await ctx.send(f"<@{ctx.author.id}>\n Prefix must be /, !, ~, `, #, $, %, ^, &, *, ,, ., ;, :, <, or >")
                    return

                self.data.prefixDict[str(ctx.message.guild.id)] = args   
            
                msg = await ctx.send(f"<@{ctx.author.id}>\n Prefix for this server set to: {args.strip()}")
                await msg.pin()

            else:
                    await ctx.send("Only server administrators have access to this command.")
        else:
            if(ctx.author.guild_permissions.administrator):
                await ctx.send(f"<@{ctx.author.id}>\n You must include arguments! Ex: !set_prefix &")
                return
            else:
                await ctx.send("Only server administrators have access to this command.")

    
    @commands.command()
    async def Admin(self, ctx, *, args = None):
        await self.admin(ctx)

    @commands.command()
    async def Set_prefix(self, ctx, *, args = None):
        await self.set_prefix(ctx, args = args)