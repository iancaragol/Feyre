import asyncio
import textwrap
from itertools import count, filterfalse
from os import path

import aioodbc
import operator

import pyodbc
from _classes.Character import Character


class CharacterSelectionHandler:
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
                print("CH: " + result.characterName)
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

            return """```An error occured. Please report the issue with !request.```"""

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
        = Your Characters =
        [ Character | ID | Init | Active]
        """)

        characters = await self.get_characters(user_id)

        for c in sorted(characters, key=operator.attrgetter('character_id')):
            code_block += c.character_name
            code_block += " | "
            code_block += str(c.character_id)
            code_block += " | "
            code_block += str(c.init_mod)
            code_block += " | "
            code_block += "x" if c.selected else ""
            code_block += '\n'

        code_block = code_block.strip() + "```"
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
                    return await self.add_character(user_id, "".join(args_list[args_list.index("-a")+1:]).strip(), "1d20")
                except Exception as e:
                    print(e)
                    return "```Something went wrong. Are you missing your character's name? See !help characters for more info. \n\nIf you believe this is a bug use the !request command to report it.```"
            else: # Init is included
                try:
                    return await self.add_character(user_id, "".join(args_list[args_list.index("-a")+1:args_list.index("-i")]).strip(), "".join(args_list[args_list.index("-i")+1:]).strip())
                except Exception as e:
                    print(e)
                    return "```Something went wrong. Are you missing your character's initiative or name? See !help characters for more info. \n\nIf you believe this is a bug use the !request command to report it.```"

        if "-r" in args_list:
            try:
                return await self.remove_character(user_id, int("".join(args_list[args_list.index("-r")+1:]).strip()))
            except Exception as e:
                print(e)
                return "```Something went wrong. Check your character's id and try again. See !help characters for more info. \n\nIf you believe this is a bug use the !request command to report it.```"