import textwrap
import discord
from discord.ext import commands


class Administrator(commands.Cog):
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data

    @commands.command(aliases = ['Admin'])
    async def admin(self, ctx):
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

    @commands.command(aliases = ['Set_prefix'])
    async def set_prefix(self, ctx, *, args = None):
        #TO DO:
        #Support pinging bot if you do not know the prefix
        #Removing bot from server should reset bot's prefix
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
                    await ctx.send(f"<@{ctx.author.id}>\n Prefix must be ?, /, !, ~, `, #, $, %, ^, &, *, ,, ., ;, :, <, or >")
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

    @commands.command(aliases = ['Permissions'])
    async def permissions(self, ctx, *, args = None):
        s = textwrap.dedent("""
        ```asciidoc
        Permissions
        ===========

        [NOTE]
        Manage Messages is now required for the initiative tracker to function properly!

        Feyre requires four permissions:
            - Send Messages
            - Read Message History
            - Manage Messages
            - Add Reactions

        How to update permissions:

        1) If you are an admin, navigate to Server Settings.
        2) Click on Roles and find the role that Feyre has been assigned.
        3) Under text permissions enable Send Messages, Read Message History, Manage Messages, and Add Reactions.    
        ```
        """)

        await ctx.send(s)

        @commands.command(aliases = ['New'])
        async def new(self, ctx):
            """
            Whats new with the bot?

            """
            self.data.userSet.add(ctx.author.id)
            self.data.statsDict['!new'] += 1

            updateString = '''```asciidoc
        [Updates - see !help for more information]
        = Rewrote Initiative tracking (!init) = 
            - Added emoji for adding a character to initiative
            - Added emoji for removing a character from initiative
            - Added support for characters with spaces in their names
            - Added support for more complicated dice expressions using the -i argument

        = Added persistent character storage (!character)=
            - Users can now register up to 9 characters
            - When using the initiative tracker users can add their active character using emojis
            - Users can change their active character using emojis

            > This functionality will eventually be merged with the bank

        = Added ability lookup (!ability)= 
            - Users can search for class abilities such as Rogue's Vanish

        = Added dice reroll emoji (!roll)= 
            - Users can now reroll a dice using the reroll emoji. They no longer need to retype the command.

        = Added a ping command (!ping) = 
            - !ping can be used to check bot latency

        = Bank Command now shows abbreviated version of character accounts =

        [Bugs]
        > Fixed typos
        > Fixed initiative tracker
        > Moved most major functionality into cogs

        Please report bugs using the !request command```'''
            await ctx.send(updateString)