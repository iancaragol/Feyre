import aioodbc
import pyodbc
import textwrap
import asyncio
import operator
import re

import discord
from discord.ext import commands

from itertools import count, filterfalse
from os import path
from _classes.Character import Character

class Bank():
    def __init__(self):
        self.uid = ""
        self.pw = ""

        pyDir = path.dirname(path.dirname(__file__))
        with open(path.join(pyDir, 'db_user.txt'), 'r') as file:
            self.uid = file.readline().strip()
            self.pw = file.readline().strip()

    async def connect(self):
        driver = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:feyre-db-server.database.windows.net,1433;Database=FeyreDB;"+"Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(self.uid, self.pw)
        cnxn = await aioodbc.connect(dsn=driver)

        return cnxn

    async def parse_args(self, user_id, args):
        # Basically the entry point for the bank.
        

        if '-add' in args: # Add character
            args = args.replace('-add', '').strip()
            return await self.add_character(user_id, args)

        elif '-a' in args: # Add character
            args = args.replace('-a', '').strip()
            return await self.add_character(user_id, args)
        
        elif '-remove' in args: # Remove character
            args = args.replace('-remove', '').strip()
            
            # First check if we got a character name or a character id
            try:
                character_id = int(args)
                return await self.remove_character(user_id, None, character_id)
            except ValueError:
                return await self.remove_character(user_id, args, None)

        elif '-r' in args: # Remove character
            args = args.replace('-r', '').strip()
            
            # First check if we got a character name or a character id
            try:
                character_id = int(args)
                return await self.remove_character(user_id, None, character_id)
            except ValueError:
                return await self.remove_character(user_id, args, None)
        
        elif '-deposit' in args:
            character_id = None

            args = args.replace('-deposit', '').strip()
            split = args.split(' ')

            # First check if we got a character name or a character id
            try:
                character_id = int(split[0])
            except ValueError:
                pass

            values = await self.parse_currency_input(args[args.find(split[0])+len(split[0]):].strip())

            if type(values) is str:
                return values

            return await self.change_balance(True, user_id, split[0], character_id, values[0], values[1], values[2], values[3], values[4])

        elif '-d' in args:
            character_id = None

            args = args.replace('-d', '').strip()
            split = args.split(' ')

            # First check if we got a character name or a character id
            try:
                character_id = int(split[0])
            except ValueError:
                pass

            values = await self.parse_currency_input(args[args.find(split[0])+len(split[0]):].strip())

            if type(values) is str:
                return values

            return await self.change_balance(True, user_id, split[0], character_id, values[0], values[1], values[2], values[3], values[4])
        
        elif '-withdraw' in args: # Withdraw
            character_id = None

            args = args.replace('-withdraw', '').strip()
            split = args.split(' ')

            # First check if we got a character name or a character id
            try:
                character_id = int(split[0])
            except ValueError:
                pass

            values = await self.parse_currency_input(args[args.find(split[0])+len(split[0]):].strip())

            if len(values) == 1:
                return values[0]

            return await self.change_balance(False, user_id, split[0], character_id, values[0], values[1], values[2], values[3], values[4])

        elif '-w' in args: # Withdraw
            character_id = None

            args = args.replace('-w', '').strip()
            split = args.split(' ')

            # First check if we got a character name or a character id
            try:
                character_id = int(split[0])
            except ValueError:
                pass

            values = await self.parse_currency_input(args[args.find(split[0])+len(split[0]):].strip())

            if len(values) == 1:
                return values[0]

            return await self.change_balance(False, user_id, split[0], character_id, values[0], values[1], values[2], values[3], values[4])

        else: # Assume user is trying to check balance
            try:
                character_id = int(args)
                return await self.get_character_formatted(user_id, None, character_id)
            except ValueError:
                return await self.get_character_formatted(user_id, args, None)

    async def parse_currency_input(self, inp):
        #13pp10gp4ep9sp8cp
        if len(inp) == 0:
            return """```Missing currency values, see !help bank for examples.```"""

        if '-' in inp:
            return """```Sorry! I can't parse negative currency values right now. Use -w to withdraw from the bank instead.```"""

        try:
            inp = inp.lower().replace(' ', '')

            if ('/' in inp):
                t = inp.split('/')
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
                return """```There was something I didn't understand about your input. See !help bank for examples.\n\nThink this is a bug? Please use !request to report it.```"""
        except Exception as e:
            print("An exception occurred while processing bank input.")
            print(e)
            return """```There was something I didn't understand about your input. See !help bank for examples.\n\nThink this is a bug? Please use !request to report it.```"""

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

        return (pp, gp, ep, sp, cp)

    async def change_balance(self, deposit, user_id, character_name, character_id, pp, gp, ep, sp, cp):
        if not deposit: # If withdrawal then flip values
            pp = pp*-1
            gp = gp*-1
            ep = ep*-1
            sp = sp*-1
            cp = cp*-1

        cnxn = await self.connect()
        cursor = await cnxn.cursor()

        # Select current values
        # Lets do only user_id and char_id for now
        current_character = await self.get_character(user_id, character_name, character_id)

        if current_character: # If this character exists
            current_character.pp += pp
            current_character.gp += gp
            current_character.ep += ep
            current_character.sp += sp
            current_character.cp += cp

            await current_character.coalesce()

            if character_id:
                update_string = textwrap.dedent("""
                UPDATE Bank SET pp = ?, gp = ?, ep = ?, sp = ?, cp = ? WHERE user_id = ? AND character_id = ?""")
                await cursor.execute(update_string,
                               current_character.pp,
                               current_character.gp,
                               current_character.ep,
                               current_character.sp,
                               current_character.cp,
                               user_id, 
                               character_id)

                await cnxn.commit()

                await cursor.close()
                await cnxn.close()

            
            elif character_name:
                update_string = textwrap.dedent("""
                UPDATE Bank SET pp = ?, gp = ?, ep = ?, sp = ?, cp = ? WHERE user_id = ? AND character_name = ?""")
                await cursor.execute(update_string,
                               current_character.pp,
                               current_character.gp,
                               current_character.ep,
                               current_character.sp,
                               current_character.cp,
                               user_id, 
                               character_name)

                await cnxn.commit()

                await cursor.close()
                await cnxn.close()

            
            if pp == 0 and gp == 0 and ep == 0 and sp == 0 and cp == 0:
                return f"```{current_character.character_name}'s account balance did not change.```"

            if deposit:
                s = "```Deposited "
                if pp != 0: s += f"{pp}pp, "
                if gp != 0: s += f"{gp}gp, "
                if ep != 0: s += f"{ep}ep, "
                if sp != 0: s += f"{sp}sp, "
                if cp != 0: s += f"{cp}cp"
                if s[len(s)-2] == ',':s = s[:-2]
                s += f" into {current_character.character_name}'s account.```"

                return s
            
            elif not deposit:
                s = "```Withdrew "
                if pp != 0: s += f"{-pp}pp, "
                if gp != 0: s += f"{-gp}gp, "
                if ep != 0: s += f"{-ep}ep, "
                if sp != 0: s += f"{-sp}sp, "
                if cp != 0: s += f"{-cp}cp"
                if s[len(s)-2] == ',':s = s[:-2]
                s += f" from {current_character.character_name}'s account.```"

                return s

        else:
            await cursor.close()
            await cnxn.close()

            return """```I couldn't find a character by that name or id. Try !bank to see your characters.```"""

    async def get_character(self, user_id, character_name, character_id):
        cnxn = await self.connect()
        cursor = await cnxn.cursor()

        if character_id:
            selection_string = textwrap.dedent(""" 
                SELECT * From Bank WHERE user_id = ? AND character_id = ?""")
            await cursor.execute(selection_string, user_id, character_id)
            results = await cursor.fetchall()

            if results:
                await cursor.close()
                await cnxn.close()

                for result in results:
                    return Character(user_id, result.character_name, int(result.character_id), int(result.pp), int(result.gp), int(result.ep), int(result.sp), int(result.cp))
            else:
                await cursor.close()
                await cnxn.close()

                return None

        elif character_name:
            selection_string = textwrap.dedent("""
                SELECT * From Bank WHERE user_id = ? AND character_name = ?""")
            await cursor.execute(selection_string, user_id, character_name)
            results = await cursor.fetchall()

            if results:
                await cursor.close()
                await cnxn.close()

                for result in results:
                    return Character(user_id, result.character_name, int(result.character_id), int(result.pp), int(result.gp), int(result.ep), int(result.sp), int(result.cp))
            else:
                await cursor.close()
                await cnxn.close()

                return None

    async def get_character_formatted(self, user_id, character_name, character_id):
        character = await self.get_character(user_id, character_name, character_id)

        if not character:
            return """```I could not find that character in your bank. Try !bank to see your characters or !bank -a [character name] to add a new character.```"""

        code_block = textwrap.dedent(f"""
        ```asciidoc
         {character.character_name} | {character.character_id} 
        """)

        underline = ''.join(['-' for s in range(len(character.character_name)+2+len(str(character_id)))])
        code_block += underline

        code_block += textwrap.dedent(f"""
        {character.pp} pp
        {character.gp} gp
        {character.ep} ep
        {character.sp} sp
        {character.cp} cp
        ```""")

        return code_block

    async def get_characters(self, user_id):
        cnxn = await self.connect()
        cursor = await cnxn.cursor()

        selection_string = textwrap.dedent(""" 
            SELECT * From Bank WHERE user_id = ?""")

        await cursor.execute(selection_string, user_id)
        results = await cursor.fetchall()

        characters = []

        if results:
            for result in results:
                character = Character(user_id, result.character_name, int(result.character_id), int(result.pp), int(result.gp), int(result.ep), int(result.sp), int(result.cp))
                characters.append(character)

        await cursor.close()
        await cnxn.close()

        return characters
    
    async def get_characters_formatted(self, user_id):
        code_block = textwrap.dedent("""
        ```asciidoc
        = $ Feyre Bank $ =
        [ Character | ID ]
        """)

        characters = await self.get_characters(user_id)

        for c in sorted(characters, key=operator.attrgetter('character_id')):
            code_block += c.character_name
            code_block += " | "
            code_block += str(c.character_id)
            code_block += '\n'

        code_block = code_block.strip() + "\n\nSee !help bank for examples.```"
        return str(code_block)


    async def add_character(self, user_id, character_name):
        if ' ' in character_name: # TODO Eventuall you should be able to have a character name with a space
            return """```A character's name cannot contain a space. This will be supported at some point!```"""
        
        if '-w' in character_name or '-r' in character_name or '-d' in character_name:
            return """```A character's name cannot contain -w, -r, or -d as these are command arguments.```"""

        cnxn = await self.connect()
        cursor = await cnxn.cursor()

        characters = await self.get_characters(user_id)

        insert_string = textwrap.dedent("""
            INSERT INTO Bank(user_id, character_name, character_id, pp, gp, ep, sp, cp) VALUES(?,?,?,?,?,?,?,?)""")

        # Wizardry to get the smallest id not already taken
        ids = [c.character_id for c in characters]
        character_id = int(next(filterfalse(set(ids).__contains__, count(1))))

        try:
            await cursor.execute(insert_string, user_id, character_name, character_id, 0, 0, 0, 0, 0)
            await cnxn.commit()

            await cursor.close()
            await cnxn.close()

            return f"""```{character_name} was added to your bank!```"""

        except pyodbc.IntegrityError:
            await cursor.close()
            await cnxn.close()

            return """```You already have a character by that name. Try !bank to see your characters.```"""

    async def remove_character(self, user_id, character_name, character_id):
        cnxn = await self.connect()
        cursor = await cnxn.cursor()

        delete_character = await self.get_character(user_id, character_name, character_id)

        if delete_character:
            if character_name:
                delete_string = textwrap.dedent("""
                DELETE FROM Bank WHERE user_id = ? and character_name = ?""")
                await cursor.execute(delete_string, user_id, character_name)
                await cnxn.commit()

                await cursor.close()
                await cnxn.close()

                return f"""```{delete_character.character_name} was removed from your bank.```"""
            
            elif character_id:
                delete_string = textwrap.dedent("""
                DELETE FROM Bank WHERE user_id = ? and character_id = ?""")
                await cursor.execute(delete_string, user_id, character_id)
                await cnxn.commit()

                await cursor.close()
                await cnxn.close()

                return f"""```{delete_character.character_name} was removed from your bank.```"""

        else:
            await cursor.close()
            await cnxn.close()

            if character_id:
                return f"""```A character with an id of {character_id} does not exist. Try !bank to see your characters.```"""
            elif character_name:
                return f"""```{character_name} does not have a bank account. Try !bank to see your characters.```"""
            

class Banker(commands.Cog):
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
        self.bank_class = Bank()

    @commands.command()
    async def bank(self, ctx, *, args = None):
        if (ctx.author.id not in self.data.userSet):
            self.data.userSet.add(ctx.author.id)
        self.data.statsDict['!bank'] += 1

        if not args:
            await ctx.send(await self.bank_class.get_characters_formatted(ctx.author.id))

        if args:
            await ctx.send(await self.bank_class.parse_args(ctx.author.id, args))

    @commands.command()
    async def Bank(self, ctx, *, args = None):
        await self.bank(ctx, args = args)