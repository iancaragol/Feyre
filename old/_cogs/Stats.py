import textwrap
import discord
from discord.ext import commands

class StatsCog(commands.Cog):
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
        self.stats_str = textwrap.dedent(
        '''
        ```asciidoc
        = Lifetime Stats =
        > !help: {help_count}
        > !hello: {hello_count}
        > !init: {init_count}
        > !roll: {roll_count}

        [D&D 5E]
        > !feat: {feat_count}
        > !mm: {mm_count}   
        > !spell: {spell_count}
        > !weapon: {weapon_count}
        > !item {item_count}
        > !dom: {dom_count}
        > !class: {c_count}
        > !ability: {ability_count}
        > !currency: {currency_count}
        > !condtion: {condition_count}
        > !bank: {bank_count}
        > !randfeat: {randfeat_count}
        > !randmonster: {randmonster_count}

        = Unique users: {user_count} =
        = Server count: {server_count} =
        = Total command count: {total_count} =
        ```
        '''
        )

        self.stats_str_all = textwrap.dedent(
        '''
        ```asciidoc
        = Lifetime Stats =
        > !help: {help_count}
        > !hello: {hello_count}
        > !init: {init_count}
        > !roll: {roll_count}

        [D&D 5E]
        > !feat: {feat_count}
        > !mm: {mm_count}   
        > !spell: {spell_count}
        > !weapon: {weapon_count}
        > !item: {item_count}
        > !dom: {dom_count}
        > !class: {c_count}
        > !ability: {ability_count}
        > !currency: {currency_count}
        > !condtion: {condition_count}
        > !bank: {bank_count}
        > !randfeat: {randfeat_count}
        > !randmonster: {randmonster_count}

        [Book of Tor]
        > !tor horo: {tor_horo_count}
        > !tor randchar: {tor_randchar_count}
        > !tor styles: {tor_styles_count}
        > !tor zodiac: {tor_zodiac_count}

        [Others]
        > !char: {char_count}
        > !new: {new_count}
        > !gm: {gm_count}
        > !admin: {admin_count}
        > !set-prefix: {setprefix_count}
        > !request: {request_count}
        > !vote: {vote_count}
        > (dirty rolls): {dirty_roll_count}

        = Unique users: {user_count} =
        = Server count: {server_count} =
        = Total command count: {total_count} =
        ```
        '''
        )

        # When creating the command counts we want to exclude some items
        # Put those keys here
        self.count_exclusion = ['user_count',
                               'server_count', 
                               'total_command_count',
                               'date']

    
    async def get_total_helper(self, stats_dict):
        return sum([v for k,v in stats_dict.items() if k not in self.count_exclusion])


    async def get_stats(self, args, stats_dict, user_count, server_count):
        # print(args)
        if args == None:
            return self.stats_str.format(
                help_count = stats_dict['!help'],
                hello_count = stats_dict['!hello'],
                init_count = stats_dict['!init'],
                roll_count = stats_dict['!roll'],
                feat_count = stats_dict['!feat'],
                mm_count = stats_dict['!mm'],
                spell_count = stats_dict['!spell'],
                weapon_count = stats_dict['!weapon'],
                item_count = stats_dict['!item'],
                dom_count = stats_dict['!dom'],
                c_count = stats_dict['!c'],
                ability_count = stats_dict['!ability'],
                currency_count = stats_dict['!currency'],
                condition_count = stats_dict['!condition'],
                bank_count = stats_dict['!bank'],
                randfeat_count = stats_dict['!randfeat'],
                randmonster_count = stats_dict['!randmonster'],
                user_count = user_count,
                server_count = server_count,
                total_count = await self.get_total_helper(stats_dict)
            )

        elif args == "all":
            return self.stats_str_all.format(
                help_count = stats_dict['!help'],
                hello_count = stats_dict['!hello'],
                init_count = stats_dict['!init'],
                roll_count = stats_dict['!roll'],
                feat_count = stats_dict['!feat'],
                mm_count = stats_dict['!mm'],
                spell_count = stats_dict['!spell'],
                weapon_count = stats_dict['!weapon'],
                item_count = stats_dict['!item'],
                dom_count = stats_dict['!dom'],
                c_count = stats_dict['!c'],
                ability_count = stats_dict['!ability'],
                currency_count = stats_dict['!currency'],
                condition_count = stats_dict['!condition'],
                bank_count = stats_dict['!bank'],
                randfeat_count = stats_dict['!randfeat'],
                randmonster_count = stats_dict['!randmonster'],
                tor_horo_count = stats_dict['!tor horo'],
                tor_randchar_count = stats_dict['!tor randchar'],
                tor_styles_count = stats_dict['!tor styles'],
                tor_zodiac_count = stats_dict['!tor zodiac'],
                char_count = stats_dict['!character'],
                new_count = stats_dict['!new'],
                gm_count = stats_dict['!gm'],
                admin_count = stats_dict['!admin'],
                setprefix_count = stats_dict['!set_prefix'],
                request_count = stats_dict['!request'],
                vote_count = stats_dict['!vote'],
                dirty_roll_count = stats_dict['dirty_rolls'],
                user_count = user_count,
                server_count = server_count,
                total_count = await self.get_total_helper(stats_dict)
            )

        else:
            return textwrap.dedent(
                '''
                ```
                I didn't understand your input. Try !stats or !stats all.
                ```
                '''
            )

    @commands.command(aliases=['Stats'])
    async def stats(self, ctx, *, args = None):
        """
        Shows the lifetime stats of the bot

        """
        self.data.userSet.add(ctx.author.id)

        if args != None:
            args = args.lower().strip()
        
        await ctx.send(await self.get_stats(args, self.data.statsDict, len(self.data.userSet), len(self.bot.guilds)))


