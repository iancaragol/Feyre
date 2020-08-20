import textwrap

class StatsHandler:
    stats_str = textwrap.dedent(
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
        > !dom: {dom_count}
        > !c: {c_count}
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

    stats_str_all = textwrap.dedent(
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
        > !dom: {dom_count}
        > !c: {c_count}
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

    

    async def get_stats(self, args, stats_dict, user_count, server_count):
        print(args)
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
                dom_count = stats_dict['!dom'],
                c_count = stats_dict['!c'],
                currency_count = stats_dict['!currency'],
                condition_count = stats_dict['!condition'],
                bank_count = stats_dict['!bank'],
                randfeat_count = stats_dict['!randfeat'],
                randmonster_count = stats_dict['!randmonster'],
                user_count = user_count,
                server_count = server_count,
                total_count = sum(stats_dict.values())
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
                dom_count = stats_dict['!dom'],
                c_count = stats_dict['!c'],
                currency_count = stats_dict['!currency'],
                condition_count = stats_dict['!condition'],
                bank_count = stats_dict['!bank'],
                randfeat_count = stats_dict['!randfeat'],
                randmonster_count = stats_dict['!randmonster'],
                tor_horo_count = stats_dict['!tor horo'],
                tor_randchar_count = stats_dict['!tor randchar'],
                tor_styles_count = stats_dict['!tor styles'],
                tor_zodiac_count = stats_dict['!tor zodiac'],
                new_count = stats_dict['!new'],
                gm_count = stats_dict['!gm'],
                admin_count = stats_dict['!admin'],
                setprefix_count = stats_dict['!set_prefix'],
                request_count = stats_dict['!request'],
                vote_count = stats_dict['!vote'],
                dirty_roll_count = stats_dict['dirty_rolls'],
                user_count = user_count,
                server_count = server_count,
                total_count = sum(stats_dict.values())
            )

        else:
            return textwrap.dedent(
                '''
                ```
                I didn't understand your input. Try !stats or !stats all.
                ```
                '''
            )


