from decimal import InvalidOperation
import traceback
import textwrap
import aioodbc

from os import environ
from urllib import response
from itertools import count, filterfalse
from json import dumps, loads
from backend_service.api.model.character_model import Character

class CharacterOperation():
    """
    """

    def __init__(self, user : int, character_id : int = None, character_name : str = None, init_mod : str = None):
        self.user = user
        self.character_id = character_id
        self.character_name = character_name
        self.init_mod = init_mod
        self.uid = environ.get("SQL_DB_UID").strip()
        self.pw = environ.get("SQL_DB_PW").strip()

    async def execute_get(self):
        """
        Gets the user's list of characters

        Returns:
            JSON list of all of the user's characters
        """
        character_list = await self.get_characters()
        character_list_json = {
            "characters" :  [c.to_dict() for c in character_list]
        }
        return dumps(character_list_json)

    async def execute_patch(self):
        """
        Patch updates the character_id to be the selected character

        Returns:
            JSON list of all of the users's characters
        """
        await self.select_character()
        return await self.execute_get()

    async def execute_put(self):
        """
        Adds a new character

        Returns:
            JSON list of all of the users's characters
        """
        await self.add_character()
        return await self.execute_get()

    async def execute_delete(self):
        """
        Deletes the character

        Returns:
            JSON list of all of the users's characters
        """
        await self.remove_character()
        return await self.execute_get()

    async def connect(self):
        """
        Creates a connection to the SQL DB
        """
        driver = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:feyre-db-server.database.windows.net,1433;Database=FeyreDB;"+"Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(self.uid, self.pw)
        cnxn = await aioodbc.connect(dsn=driver)

        return cnxn

    ################################################################
    #   Everything below here is old code, consider reworking it!  #
    ################################################################
    async def select_character(self):
        """
        Updates the character to be the selected character
        """
        cnxn = await self.connect()
        cursor = await cnxn.cursor()

        characters = await self.get_characters()
        currently_selected = 0

        for c in characters:
            if c.is_active == 1:
                currently_selected = c.id
        

        # Disable the currently selected character
        if currently_selected:
            update_string = textwrap.dedent("""
            UPDATE characters SET selected = ? WHERE userId = ? AND characterId = ?""")
            await cursor.execute(update_string,
                            False,
                            self.user, 
                            currently_selected)

            await cnxn.commit()

        # Then select new character
        update_string = textwrap.dedent("""
        UPDATE characters SET selected = ? WHERE userId = ? AND characterId = ?""")
        await cursor.execute(update_string,
                        True,
                        self.user, 
                        self.character_id)

        await cnxn.commit()
        await cursor.close()
        await cnxn.close()

    async def get_characters(self):
        cnxn = await self.connect()
        cursor = await cnxn.cursor()

        selection_string = textwrap.dedent(""" 
            SELECT * From characters WHERE userId = ?""")

        await cursor.execute(selection_string, self.user)
        results = await cursor.fetchall()

        characters = []

        if results:
            for result in results:
                character = Character(user = self.user, id=int(result.characterId), is_active=bool(result.selected), name = result.characterName, initiative_expression = str(result.initMod))
                characters.append(character)

        await cursor.close()
        await cnxn.close()

        return characters

    async def get_active_character(self):
        cnxn = await self.connect()
        cursor = await cnxn.cursor()

        selection_string = textwrap.dedent(""" 
            SELECT * From characters WHERE userId = ? AND selected = 1""")

        await cursor.execute(selection_string, self.user)
        results = await cursor.fetchall()

        characters = []

        if results:
            for result in results:
                character = Character(user = self.user, is_active=bool(result.selected), name = result.characterName, initiative_expression = str(result.initMod))
                characters.append(character)

        await cursor.close()
        await cnxn.close()

        if len(characters) == 1:
            return characters[0]
        else:
            return None

    async def add_character(self):
        cnxn = await self.connect()
        cursor = await cnxn.cursor()

        characters = await self.get_characters()

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
            ids = [c.id for c in characters]
            character_id = int(next(filterfalse(set(ids).__contains__, count(1))))

        selected = 0 # If there are no characters select the new one by default
        if len(ids) == 0:
            selected = 1

        if character_id > 9:
            await cursor.close()
            await cnxn.close()

            raise InvalidOperation(message="Maximum # of characters reached")

        try:
            await cursor.execute(insert_string, self.user, self.character_name, character_id, self.init_mod, selected, 0, 0, 0, 0, 0)
            await cnxn.commit()

            await cursor.close()
            await cnxn.close()

        except Exception as e:
            await cursor.close()
            await cnxn.close()

            raise e

    async def remove_character(self):
        cnxn = await self.connect()
        cursor = await cnxn.cursor()

        delete_string = textwrap.dedent("""
        DELETE FROM characters WHERE userId = ? and characterId = ?""")
        await cursor.execute(delete_string, self.user, self.character_id)
        await cnxn.commit()

        await cursor.close()
        await cnxn.close()