import textwrap
import discord
from discord.ext import commands


class Helper(commands.Cog):
    def __init__(self, bot, data):
        self.command_list = [
            "help", "hello", "init", 
            "roll", "d", "gm",
            "feat", "condition", "weapon",
            "item", "mm", "spell", "c",
            "currency", "bank", "dom",
            "stats", "request", "admin", 
            "new", "vote", "ability", "character"
        ]

        self.bot = bot
        self.data = data

#region Help_Strings
        self.help_str_base = textwrap.dedent(
            '''
            ```asciidoc
            Hello! My name is Feyre. You can use chat or DM's to summon me. 
            ===============================================================

            [Read the Documentation]
            feyre.readthedocs.io

            [Join the Support Server]
            !support

            The default prefix is !. To learn more about a command type !help [command].
            Like this: !help roll

            `NOTE: Lots of updates! See !new'

            [Commands]
            > hello - Hi!

            > init- Initiative tracking
            > roll - Dice rolling with complicated expressions
            > d - Simple dice rolling
            > gm - GM only dice rolling

            `> char - Manage your character(s) for initiative tracking (NEW)'

            > feat - Feat lookup
            > condition - Condition lookup
            > weapon - Weapon lookup
            > item - Wondrous item lookup
            > mm - Monster Manual lookup
            > spell - Spell lookup
            > c - Class lookup
            `> ability - Class Ability lookup (NEW)'

            > currency - Currency conversions
            > bank - Manage your all of your characters' wallets

            > dom - Draw from the Deck of Many Things

            > stats - Bot usage statistics
            > request - Request new features & report bugs
            > admin - Change default command prefix
            > new - New features & updates
            > vote - Vote for Feyre on top.gg
            > permissions - See Feyre's required permissions
            > invite - Get an invite link for Feyre

            Feyre always responds in the channel or direct message from which it was summoned.

            Like Feyre?
            ===========
            Use !invite to add Feyre to your server!
            Also consider voting for Feyre on top.gg using the `!vote' command :)
            ```
            ''' 
        )

        self.help_str_init = textwrap.dedent(
            '''
            ```
            !init is a per channel based initiative tracker. 

            Buttons:
                Crossed Swords : Moves turn icon (>).
                Plus Sign : Adds user's active character to initiative, see !help character for details.
                Skull and Crossbones : Removes the user's most recent character from initiative.

            If you need to insert a player into the middle of initative use decimals.

            Commands (can be shortened to !i):
            !init start
                > Starts a new initiative tracker in the same channel, also used to create a new one
            !init start -v
                > Starts a new initiative tracker with verbosity.
            !init bottom OR !init -b
                > Brings the initiative tracker to the bottom of the channel
            !init
                > Adds the player to initiative with their active character and that characters initiative modifier.
            !init [player name]
                > Adds a player with [player name] to initiative and rolls 1d20 for them
            !init [player name] [initiative]
                > Adds a player with [player name] and [initiative] to initiative.
            !init [player name] -i [any dice expression]
                > Adds a player with [player name] and rolls any dice expression for them.
            !!init -r [player name]
                > Removes a player from initiative. 
            !init -r
                > Removes the most recent player added by the user from initiative.
            !init [name] [modifier] or [modifier] [name]
                > Adds a player to inititative after rolling 1d20 and applying the modifier.

            Ex:
            !init start
            !i Legolas 15
            !i Aragorn 15.1
            !i Sauron +5
            !init Gandalf 1
            !init Frodo
            !init remove Frodo
            !init -r Gandalf
            !init round 3

            Reset tracker but keep Legolas, Aragorn, and Sauron's rolls.
            !init reset
            ```
            '''
        )

        self.help_str_character = textwrap.dedent(
            '''
            ```
            !character is used to set your active character which is used by the initiative tracker. You can create up to 9 characters and set a character as active using emojis or the command argument [id]. Characters follow you across servers and are persistent.

            This command can also be shortened to !char
            
            Commands:
            !character
                > Shows your character list and lets you select your active character using the UI
            !character -a [Character Name] -i [Initiative Dice Expression]
                > Adds a character with [Character Name] to your character list. [Initiative Dice Expression] will be rolled whenever this character is added to initiative. The -i tag is optional and if it is not included that character's initiative will default to rolling 1d20.
            !character -r [ID]
                > Removes the character with [ID] from your character list. You can find your character's ID's using !character
            !character [ID]
                > Sets the character with [ID] as your active character

            Example:
            !character -a Gandalf -i 1d20-5
            !character
            !character 1
            !character -r 1
            !character -a Frodo
            ```
            '''
        )

        self.help_str_roll = textwrap.dedent(
            '''
            ```
            !roll can be used to roll dice of any size with complicated expressions and built in skill checks. Press the reroll emoji to reroll that dice expression.

            Dice are represented with the standard [# of dice]d[size of dice] format. You can also use !r.

            Ex: !roll 4d6
            !roll 1d6*2
            !r 1d20 + 5
            !r 1d1000 + 2d2000 * 3 / 3 - 1

            Skill checks can be built into the dice expression using the < and > symbols.
            Ex: !roll 1d20 > 15

            You can roll with advantage or disadvantage using the -a and -d flags before the dice expression.
            Ex: !roll -a 1d20
                !roll -d 1d20+5
            ```
            '''
        )

        self.help_str_d = textwrap.dedent(
            '''
            ```
            !d[size] [expression] can be used if you only want to roll one dice.
            This command supports standard dice sizes [4,6,8,10,12,20] and expressions. A space is neccessary between the dice and any modifiers.

            You can also use !dp to roll for percentile.

            Ex:
            !d20
            !d6 +2
            !dp
            ```
            ''' 
        )

        self.help_str_stats = textwrap.dedent(
            '''
            ```
            Feyre keeps track of the number of times each command has been used and the total user count.
            ```
            '''
        )

        self.help_str_feat = textwrap.dedent(
            '''
            ```
            !feat can be used to lookup feats from the Standard Reference Document.

            Why does !feat link to D&D Beyond? Feats are not part of the Standard Reference Document so I cannot display them here.

            Commands:
            !feat [feat name] 
                > Searches for a feat
            !randfeat
                > Gives a random feat
            Ex:
            !feat Keen Mind
            ```
            '''
        )

        self.help_str_conditions = textwrap.dedent(
            '''
            ```
            !condition can be used to conditions from the PHB 

            Commands:
            !condition
                > Lists all conditions
            !condition [condition]
                > Gives more info on the specified condition
            Ex:
            !condition Prone
            ```
            '''
        )

        self.help_str_mm = textwrap.dedent(
            '''
            ```
            !mm can be used to lookup monsters from the Monster Manual.

            Commands:
            !mm [monster name]
                > Searches for a monster
            !randmonster
                > Gives a random monster
            Ex:
            !mm Young Black Dragon
            !mm Tarrasque
            ```
            '''
        )

        self.help_str_class = textwrap.dedent(
            '''
            ```
            !c can be used to look up all of the features of a class. This can be a lot of text!

            Why is the command !c and not !class? Thats because class is a python keyword.

            Ex:
            !c wizard
            !c fighter
            ```
            ''' 
        )

        self.help_str_currency = textwrap.dedent(
            '''
            ```
            !currency can be used to convert any denomination of platinum, gold, electrum, silver, and copper to gold, silver and copper.
            It can also be used to evenly divide an amount of currency between any number of players by including a /x at the end where x is the number of players.

            pp = Platinum
            gp = Gold
            ep = Electrum
            sp = Silver
            cp = Copper

            When providing the amounts there is no need to worry about capitlization or spacing. See the examples below :)

            Commands:
            !currency [amount][abbreviation]
            !currency [amount][abbreviation] / [number of players] <- Optional
            !convert [amount][abbreviation]
            !convert [amount][abbreviation] / [number of players] <- Optional
            !cur [amount][abbreviation]
            !cur [amount][abbreviation] / [number of players] <- Optional

            Ex:
            !currency 10gp 55ep 5sp
            !convert 13gp55pp/4 <- Divides amongst 4 players
            !cur 11sp 333ep 4cp
            ```
            '''
        )

        self.help_str_spell = textwrap.dedent(
            '''
            ```
            !spell can be used to lookup spells from the Standard Reference Document.

            !spell [spell name]

            Ex: 
            !spell Wish
            !spell Cure Wounds
            ```
            '''
        )

        self.help_str_dom = textwrap.dedent(
            '''
            ```
            !dom can be used to draw a card from the deck of many things. The -i flag will include an image!

            Commands:
            !dom
                > Draws one card from the Deck of Many Things
            !dom -i
                > Draws one card form the Deck of Many Things and includes an image of the card
            Ex:
            !dom
            !dom -i
            ```
            '''
        )

        self.help_str_tor = textwrap.dedent(
            '''
            ```
            !tor can be used to find character styles, horoscope, race/class combinations, and zodiac from the Book of Tor.

            Commands:
            !tor styles
                > Displays character styles
            !tor horo
                > Gives a Torian horoscope
            !tor zodiac
                > Gives a Torian zodiac
            !tor randchar
                > Gives a random Torian race/class combination.
            ```
            '''
        )

        self.help_str_admin = textwrap.dedent(
            '''
            ```
            !admin is for server administrators. Currently the only command available to adminstrators is !set_prefix.

            Commands:
            !set_prefix [prefix]
                > Sets the server wide prefix to [prefix]. Prefix must be ?, !, ~, `, #, $, %, ^, &, *, ,, ., ;, :, <, or >
            Note: If you forget the bot's prefix you will no longer be able to summon it and reset it's prefix (as of now).
            ```
            '''
        )

        self.help_str_request = textwrap.dedent(
            '''
            ```
            Please help improve the bot by requesting features you would like to see!

            !request [feature]
            ```
            '''
        )

        self.help_str_vote = textwrap.dedent(
            '''
            ```
            top.gg ranks discord bots based on the number of votes that they have. Please vote for Feyre using !vote. Thanks!
            ```
            '''
        )

        self.help_str_hello = textwrap.dedent(
           '''
           ```
           Hi?
           ```
           ''' 
        )

        self.help_str_gm = textwrap.dedent(
            '''
            ```
            !gm can be used to send dice rolls to the GM without other players being able to see the result.
            GM's are set on a per channel basis.
                            
            Commands:
            !gm
                > Sets the channels GM to the user
            !gm roll [expression]
                > Rolls dice and sends the result to the user and the GM

            Ex:
            !gm
            !gm roll 1d20
            ```
            '''
        )

        self.help_str_weapon = textwrap.dedent(
            '''
            ```
            !weapon or !w can be used to lookup weapons from the players handbook. 
            If you find any errors or a weapon is missing please use !request to let me know.

            Built in attack rolls are coming soon.

            Ex:
            !w Longbow
            ```
            '''
        )

        self.help_str_item = textwrap.dedent(
            '''
            ```
            !item can be used to lookup items from the Dungeon Master's Guide. 
            If you find any errors or a item is missing please use !request to let me know. Some items have a lot of text, and may be sent in multiple message blocks.

            Ex:
            !item Portable Hole
            ```
            '''
        )

        self.help_str_ability = textwrap.dedent(
            '''
            ```
            !ability can be used to lookup class abilities such as Barbarian's Danger Sense. All abilities from the PHB are supported. If you think an ability is missing or incorrect please report it with the !request command.

            Some classes have abilities with the same names. To specify which class you are interested in include the name of the class.

            Ex:
            !ability Danger Sense
            !ability spellcasting wizard
            !ability vanish
            ```
            '''
        )

        self.help_str_bank = textwrap.dedent(
            '''
            ```
            You can use Feyre to manage all of your character's wallets. Your bank is tied to your Discord ID and can be accessed from any server/channel or by direct messaging Feyre.

            Interacting with your bank requires the use of argument flags (-a, -r, -d, -w). If you have any suggestions on how this experience can be streamlined please use the !request command and let me know!

            Commands:
            !bank
                > Shows all of your characters and their unique IDs. The character's id (a unique number representing that character) can be used instead of [character name].

            !bank -a [character name]
                > Adds a new character to your bank with [character name]. This character will also be assigned a unique ID which can be used to access its account.

            !bank -r [character name] OR [character id]
                > Deletes the account associated with [character name] or [character id]

            !bank -d [character name] [currency values] OR [character name] [currency values]
                > Deposits the specified [currency values] into the account associated with [character name] or [character id]

            !bank -w [character name] [currency values] OR [character name] [currency values]
                > Withdraws the specified [currency values] into the account associated with [character name] or [character id]

            [currency values] have the same format as the !currency command. For example you can represent 10 platinum, 9 gold, 8 electrum, 7 silver, and 6 copper like this: 10pp9gp8ep7sp6cp.

            Examples:
            !bank -a Bilbo
                > Add a character with the name Bilbo to your bank

            !bank -d Bilbo 10sp5cp
                > Deposit (-d) 10 silver and 5 copper into Bilbo's account

            !bank
                > See all of your characters and their unique ids

            !bank -w 1 3cp
                > Withdraw 3 copper from Bilbo's account. In this example Bilbo has been assigned the unique ID 1 because he is the first character associated with the example user

            !bank -r Bilbo
                > Delete Bilbo from the bank
            ```
            ''' 
        )

        self.help_str_new = textwrap.dedent(
            '''
            ```
            !new shows any new features, bug fixes, etc...
            ```
            '''
        )

        self.command_not_found = textwrap.dedent(
            '''
            ```
            I could not find that command. See !help for a list of commands.
            ```
            '''
        )

#endregion

    @commands.command()
    async def support(self, ctx, *, args = None):
        await ctx.send("https://discord.gg/zjyrtWZ")

    @commands.command(aliases=['Help'])
    async def help(self, ctx, *, args = None):
        if (ctx.author.id not in self.data.userSet):
            self.data.userSet.add(ctx.author.id)
        self.data.statsDict['!help'] += 1

        if args != None:
            args = args.strip().lower()

        help_str = await self.helper(args)

        await ctx.send(help_str)

    async def helper(self, args):
        if not args:
            return self.help_str_base

        elif args == "init":
            return self.help_str_init
        
        elif args == "roll":
            return self.help_str_roll

        elif args == "d":
            return self.help_str_d 
        
        elif args == "stats":
            return self.help_str_stats 

        elif args == "feat":
            return self.help_str_feat

        elif args == "condition":
            return self.help_str_conditions

        elif args == "c" or args == "class":
            return self.help_str_class

        elif args == "currency" or args == "cur" or args == "convert":
            return self.help_str_currency

        elif args == "spell":
            return self.help_str_spell

        elif args == "mm":
            return self.help_str_mm
        
        elif args == "dom":
            return self.help_str_dom
        
        elif args == "tor":
            return self.help_str_tor

        elif args == "request":
            return self.help_str_request

        elif args == "admin":
            return self.help_str_admin

        elif args == "vote":
            return self.help_str_vote
        
        elif args == "hello":
            return self.help_str_hello

        elif args == "gm":
            return self.help_str_gm

        elif args == "weapon":
            return self.help_str_weapon

        elif args == "item":
            return self.help_str_item

        elif args == "ability":
            return self.help_str_ability

        elif args == "bank":
            return self.help_str_bank

        elif args == "new":
            return self.help_str_new

        elif args == "character" or args == "char":
            return self.help_str_character
        
        else:
            return self.command_not_found