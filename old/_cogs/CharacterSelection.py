import asyncio
import textwrap
from itertools import count, filterfalse
from os import path, environ

import aioodbc
import operator
import discord
from discord.ext import commands

import pyodbc
from _classes.Character import Character


class CharacterSelectionHandler:
    def __init__(self):
        self.uid = ""
        self.pw = ""

        pyDir = path.dirname(path.dirname(__file__))
        try:
            self.uid = environ['dbuser']
            self.pw = environ['dbpw']
        except KeyError:
            with open(path.join(pyDir, 'db_user.txt'), 'r') as file:
                self.uid = file.readline().strip()
                self.pw = file.readline().strip()

    async def connect(self):
        driver = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:feyre-db-server.database.windows.net,1433;Database=FeyreDB;"+"Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(self.uid, self.pw)
        cnxn = await aioodbc.connect(dsn=driver)

        return cnxn

    async def get_characters(self, user_id):
        cnxn = await self.connect()
        cursor = await cnxn.cursor()

        selection_string = textwrap.dedent(""" 
            SELECT * From characters WHERE userId = ?""")

        await cursor.execute(selection_string, user_id)
        results = await cursor.fetchall()

        characters = []

        if results:
            for result in results:
                character = Character(user_id, result.characterName, int(result.characterId), int(result.pp), int(result.gp), int(result.ep), int(result.sp), int(result.cp), selected=bool(result.selected), init_mod=str(result.initMod))
                characters.append(character)

        await cursor.close()
        await cnxn.close()

        return characters

    async def get_character(self, user_id, character_id):
        cnxn = await self.connect()
        cursor = await cnxn.cursor()

        selection_string = textwrap.dedent(""" 
            SELECT * From characters WHERE userId = ? AND characterId = ?""")

        await cursor.execute(selection_string, user_id, character_id)
        results = await cursor.fetchall()

        characters = []

        if results:
            for result in results:
                character = Character(user_id, result.characterName, int(result.characterId), int(result.pp), int(result.gp), int(result.ep), int(result.sp), int(result.cp), selected=bool(result.selected), init_mod=str(result.initMod))
                characters.append(character)

        await cursor.close()
        await cnxn.close()

        if len(characters) == 1:
            return characters[0]
        else:
            return None
        
    async def get_selected_character(self, user_id):
        cnxn = await self.connect()
        cursor = await cnxn.cursor()

        selection_string = textwrap.dedent(""" 
            SELECT * From characters WHERE userId = ? AND selected = 1""")

        await cursor.execute(selection_string, user_id)
        results = await cursor.fetchall()

        characters = []

        if results:
            for result in results:
                character = Character(user_id, result.characterName, int(result.characterId), int(result.pp), int(result.gp), int(result.ep), int(result.sp), int(result.cp), selected=bool(result.selected), init_mod=str(result.initMod))
                characters.append(character)

        await cursor.close()
        await cnxn.close()

        if len(characters) == 1:
            return characters[0]
        else:
            return None

    async def add_character(self, user_id, character_name, init_mod):
        cnxn = await self.connect()
        cursor = await cnxn.cursor()

        characters = await self.get_characters(user_id)

        insert_string = textwrap.dedent("""
            INSERT INTO characters(userId,
            characterName,
            characterId, 
            initMod,
            selected,
            pp, gp, ep, sp, cp) VALUES(?,?,?,?,?,?,?,?,?,?)""")

        # Wizardry to get the smallest id not already taken
        character_id = 1
        ids = []
        if characters:
            ids = [c.character_id for c in characters]
            character_id = int(next(filterfalse(set(ids).__contains__, count(1))))

        selected = 0 # If there are no characters select the new one by default
        if len(ids) == 0:
            selected = 1

        if character_id > 9:
            await cursor.close()
            await cnxn.close()
            return f"""```Maximum character limit reached! You can have a maximum of nine characters at a time.```"""

        try:
            await cursor.execute(insert_string, user_id, character_name, character_id, init_mod, selected, 0, 0, 0, 0, 0)
            await cnxn.commit()

            await cursor.close()
            await cnxn.close()

            return f"""```{character_name} was added to your character list.```"""

        except pyodbc.IntegrityError:
            await cursor.close()
            await cnxn.close()

            return """```An error occurred. Please report the issue with !request.```"""

    async def remove_character(self, user_id, character_id):
        cnxn = await self.connect()
        cursor = await cnxn.cursor()

        delete_character = await self.get_character(user_id, character_id)

        if delete_character:
            delete_string = textwrap.dedent("""
            DELETE FROM characters WHERE userId = ? and characterId = ?""")
            await cursor.execute(delete_string, user_id, character_id)
            await cnxn.commit()

            await cursor.close()
            await cnxn.close()

            return f"""```{delete_character.character_name} was removed from your character list.```"""

        else:
            await cursor.close()
            await cnxn.close()

            if character_id:
                return f"""```A character with an id of {character_id} does not exist. Try !char to see your characters.```"""
            return f"""```Something went wrong...```"""


    async def get_characters_formatted(self, user_id):
        code_block = textwrap.dedent("""
        ```asciidoc
        ====================== Your Characters =======================
        [           Character           |  ID |  Active |    Init    ]
        """)

        characters = await self.get_characters(user_id)

        for c in sorted(characters, key=operator.attrgetter('character_id')):
            if c.selected:
                code_block += "`"

            temp_name = (c.character_name[:27] + '...') if len(c.character_name) > 29 else c.character_name
            if c.selected:
                code_block += f"{temp_name.ljust(30)}"
            else:
                code_block += f"{temp_name.ljust(31)}"

            code_block += " |   "
            code_block += str(c.character_id)
            code_block += " | "
            code_block += "  [x]  " if c.selected else "       "
            code_block += " | "
            code_block += str(c.init_mod)
            if c.selected:
                code_block += "'"
            code_block += '\n'

        code_block = code_block.strip() + "\n\nSee !help character for instructions.```"
        return str(code_block)

    async def select_character(self, user_id, character_id):
        cnxn = await self.connect()
        cursor = await cnxn.cursor()

        characters = await self.get_characters(user_id)
        currently_selected = 0

        for c in characters:
            if c.selected == 1:
                currently_selected = c.character_id
        

        # Disable the currently selected character
        if currently_selected:
                update_string = textwrap.dedent("""
                UPDATE characters SET selected = ? WHERE userId = ? AND characterId = ?""")
                await cursor.execute(update_string,
                               False,
                               user_id, 
                               currently_selected)

                await cnxn.commit()

        # Then select new character
        update_string = textwrap.dedent("""
                UPDATE characters SET selected = ? WHERE userId = ? AND characterId = ?""")
        await cursor.execute(update_string,
                        True,
                        user_id, 
                        character_id)

        await cnxn.commit()
        await cursor.close()
        await cnxn.close()

    async def parse_args(self, user_id, args = None):
        if args == None: # If none then return character list
            return await self.get_characters_formatted(user_id)

        args_list = args.strip().split(' ')

        if "-a" in args_list: # Add character
            if "-i" not in args_list: # If no init is included
                try:
                    return await self.add_character(user_id, " ".join(args_list[args_list.index("-a")+1:]).strip(), "1d20")
                except Exception as e:
                    print(e)
                    return "```Something went wrong. Are you missing your character's name? See !help characters for more info. \n\nIf you believe this is a bug use the !request command to report it.```"
            else: # Init is included
                try:
                    return await self.add_character(user_id, " ".join(args_list[args_list.index("-a")+1:args_list.index("-i")]).strip(), " ".join(args_list[args_list.index("-i")+1:]).strip())
                except Exception as e:
                    print(e)
                    return "```Something went wrong. Are you missing your character's initiative or name? See !help characters for more info. \n\nIf you believe this is a bug use the !request command to report it.```"

        if "-r" in args_list:
            try:
                return await self.remove_character(user_id, int(" ".join(args_list[args_list.index("-r")+1:]).strip()))
            except Exception as e:
                print(e)
                return "```Something went wrong. Check your character's id and try again. See !help characters for more info. \n\nIf you believe this is a bug use the !request command to report it.```"

        else:
            # Try and treat args as int
            if args.strip().isdigit():
                i = int(args.strip())
                if i <= 0 or i > 9:
                    return f"```The provided character id ({i}) is out of range. You can have a maximum of nine characters with ids 1-9. See !help character for details.```"
                else:
                    await self.select_character(user_id, i)
                    selected_character = await self.get_selected_character(user_id)
                    return f"```{selected_character.character_name} is now your active character.```"
            
            else:
                return "```I couldn't understand your input. See !help character for information on how to use this command.\n\nIf you believe this is a bug use the !request command to report it.```"

class CharacterSelector(commands.Cog):
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
        self.character_selection_handler = CharacterSelectionHandler()

    @commands.command(aliases=['char', 'Character', 'Char'])
    async def character(self, ctx, *, args = None):
        self.data.userSet.add(ctx.author.id)
        self.data.statsDict['!character'] += 1

        contents = await self.character_selection_handler.parse_args(ctx.author.id, args = args)
        characters = await self.character_selection_handler.get_characters(ctx.author.id)

        msg = await ctx.send(contents)


        # Add reactions for managing the character

        if args == None:
            contents = await self.character_selection_handler.get_characters_formatted(ctx.author.id)
            
            numerals = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

            for c in characters:
                await msg.add_reaction(numerals[c.character_id-1])

            await self.character_helper(ctx, args, contents, msg)
        

    async def character_helper(self, ctx, args, contents, msg):
        numerals = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']


        reaction, u = await self.bot.wait_for('reaction_add', check=lambda r, u:u.id != self.bot.user.id and u.id == ctx.author.id and r.message.id == msg.id, timeout=21600)

        if reaction != None:
            selected_id = numerals.index(str(reaction.emoji))+1
            await self.character_selection_handler.select_character(ctx.author.id, selected_id)
            new_contents = await self.character_selection_handler.get_characters_formatted(ctx.author.id)

            if ctx.channel.type is discord.ChannelType.private: # If user has DM'd the bot
                await msg.delete()
                await self.character(ctx, args = args)

            else:
                await msg.edit(content=new_contents)
                await reaction.remove(u)
                await self.character_helper(ctx, args, new_contents, msg)