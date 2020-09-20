import re
import textwrap
import discord

from discord.ext import commands

class CurrencyConvert:
    async def parse_input(self, inp):
        #13pp10gp4ep9sp8cp/4

        try:
            inp = inp.lower().replace(' ', '')
            num_players = None

            if ('/' in inp):
                t = inp.split('/')
                num_players = int(t[len(t)-1])
                inp = t[0]

            p = list(filter(None, re.split('(pp|gp|ep|sp|cp)', inp)))

            if p.count('pp') > 1:
                return """```You included pp (platinum) more than once. Im not sure what value to use.```"""
            if p.count('gp') > 1:
                return """```You included gp (gold) more than once. Im not sure what value to use.```"""
            if p.count('ep') > 1:
                return """```You included ep (electrum) more than once. Im not sure what value to use.```"""
            if p.count('sp') > 1:
                return """```You included sp (silver) more than once. Im not sure what value to use.```"""
            if p.count('cp') > 1:
                return """```You included cp (copper) more than once. Im not sure what value to use.```"""
            
            currency = {}
            for i in range(len(p)):
                if(not i%2 and i < len(p) - 1):
                    currency[p[i+1]] = int(p[i])
            
            if len(currency.keys()) == 0: 
                return """```There was something I didn't understand about your input. See !help currency for examples.\n\nThink this is a bug? Please use !request to report it.```"""
        except:
            return """```There was something I didn't understand about your input. See !help currency for examples.\n\nThink this is a bug? Please use !request to report it.```"""

        pp, gp, ep, sp, cp = 0, 0, 0, 0, 0
        if 'pp' in currency.keys():
            pp = currency['pp']
        if 'gp' in currency.keys():
            gp = currency['gp']
        if 'ep' in currency.keys():
            ep = currency['ep']
        if 'sp' in currency.keys():
            sp = currency['sp']
        if 'cp' in currency.keys():
            cp = currency['cp']

        if num_players:
            s_gp, s_sp, s_cp, r_gp, r_sp, r_cp = await self.player_split(num_players, await self.convert_cp(pp, gp, ep, sp, cp))
            return await self.format_split(num_players, pp, gp, ep, sp, cp, s_gp, s_sp, s_cp, r_gp, r_sp, r_cp)

        else:
            t_gp, t_sp, t_cp = await self.convert(pp, gp, ep, sp, cp)
            return await self.format(pp, gp, ep, sp, cp, t_gp, t_sp, t_cp)
        

    async def convert_cp(self, pp, gp, ep, sp, cp):
        return pp*1000 + gp*100 + ep*50 + sp*10 + cp


    async def convert(self, pp, gp, ep, sp, cp):
        total_gp = gp
        total_sp = 0
        total_cp = 0

        total_gp += pp*10

        if(cp > 0):
            s, c = divmod(cp, 10)
            sp += s
            total_cp += c
                  
        if (ep > 0):
            g, e = divmod(ep, 2)
            total_gp += g
            sp += e*5

        if(sp > 0):
            g, s = divmod(sp, 10)
            total_gp += g
            total_sp += s

        return total_gp, total_sp, total_cp

    async def player_split(self, num_players, cp):
        # First divy up all cp
        p_cp, r_cp = divmod(cp, num_players)
        # now convert player's cp to gp, sp, cp
        split_gp, split_sp, split_cp = await self.convert(0, 0, 0, 0, p_cp)
        remaining_gp, remaining_sp, remaining_cp = await self.convert(0, 0, 0, 0, r_cp)

        return split_gp, split_sp, split_cp, remaining_gp, remaining_sp, remaining_cp

    async def format(self, pp, gp, ep, sp, cp, t_gp, t_sp, t_cp):
        # Some craziness here
        s = "```asciidoc\n"
        if pp: s += f"{pp}pp, "
        if gp: s += f"{gp}gp, "
        if ep: s += f"{ep}ep, "
        if sp: s += f"{sp}sp, "
        if cp: s += f"{cp}cp"
        if s[len(s)-2] == ',':s = s[:-2]
        s += "->\n["
        if t_gp: s += f"{t_gp}gp, "
        if t_sp: s += f"{t_sp}sp, "
        if t_cp: s += f"{t_cp}cp, "
        if s[len(s)-2] == ',':s = s[:-2]
        s += "]```"
        return s

    async def format_split(self, num_players, pp, gp, ep, sp, cp, split_gp, split_sp, split_cp, remaining_gp, remaining_sp, remaining_cp):
        # This is basically a decision tree. Anyone know how to make a decision tree inside of an f string?
        if(remaining_gp == 0):
            if(remaining_sp == 0):
                if(remaining_cp != 0): # Remainder is only cp
                    s = textwrap.dedent(f"""```
{pp}pp, {gp}gp, {ep}ep, {sp}sp, {cp}cp divided among {num_players} players.

Each player receives {split_gp}gp, {split_sp}sp, {split_cp}cp with {remaining_cp}cp leftover.```""")
                    return s
                elif(remaining_cp == 0): # No remainder
                    s = textwrap.dedent(f"""```
{pp}pp, {gp}gp, {ep}ep, {sp}sp, {cp}cp divided among {num_players} players.

Each player receives {split_gp}gp, {split_sp}sp, {split_cp}cp.```""")
                    return s
            elif(remaining_sp != 0):
                if(remaining_cp != 0): # Remainder is only sp, cp
                    s = textwrap.dedent(f"""```
{pp}pp, {gp}gp, {ep}ep, {sp}sp, {cp} cp divided among {num_players} players.

Each player receives {split_gp}gp, {split_sp}sp, {split_cp}cp with {remaining_sp}sp, {remaining_cp}cp leftover.
                    ```""")
                    return s
                elif(remaining_cp == 0): # Remainder is only sp
                    s = textwrap.dedent(f"""```
{pp}pp, {gp}gp, {ep}ep, {sp}sp, {cp} cp divided among {num_players} players.

Each player receives {split_gp}gp, {split_sp}sp, {split_cp}cp with {remaining_sp} sp leftover.```""")
                    return s
        elif(remaining_gp != 0):
            if(remaining_sp == 0):
                if(remaining_cp != 0): # Remainder is only cp
                    s = textwrap.dedent(f"""```
{pp}pp, {gp}gp, {ep}ep, {sp}sp, {cp}cp divided among {num_players} players.

Each player receives {split_gp}gp, {split_sp}sp, {split_cp}cp with {remaining_gp}gp, {remaining_cp}cp leftover.```""")
                    return s
            elif(remaining_sp != 0):
                if(remaining_cp != 0): # Remainder is only sp, cp
                    s = textwrap.dedent(f"""```
{pp}pp, {gp}gp, {ep}ep, {sp}sp, {cp} cp divided among {num_players} players.

Each player receives {split_gp}gp, {split_sp}sp, {split_cp}cp with {remaining_gp}gp, {remaining_sp}sp, {remaining_cp}cp leftover.```""")
                    return s
                elif(remaining_cp == 0): # Remainder is only sp
                    s = textwrap.dedent(f"""```
{pp}pp, {gp}gp, {ep}ep, {sp}sp, {cp} cp divided among {num_players} players.

Each player receives {split_gp}gp, {split_sp}sp, {split_cp}cp with {remaining_gp} gp, {remaining_sp} sp leftover.```""")
                    return s

class CurrencyConverter(commands.Cog):
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
        self.currency_convert = CurrencyConvert()

    async def currency_helper(self, ctx, args):
        self.data.userSet.add(ctx.author.id)
        self.data.statsDict['!currency'] += 1

        if not args:
            await ctx.send('''```Missing command arguments, see !help currency for more information.\nEx: !currency 10gp 55ep 5sp```''')
            return
        await ctx.send(await self.currency_convert.parse_input(args))

    @commands.command(aliases = ['cur', 'convert', 'Currency', 'Cur', 'Convert'])
    async def currency(self, ctx, *, args = None):
        await self.currency_helper(ctx, args)