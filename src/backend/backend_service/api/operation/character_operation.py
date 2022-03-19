import traceback
import textwrap
import aioodbc

from os import environ
from urllib import response
from json import dumps, loads
from backend_service.api.model.character_model import Character

class CharacterOperation():
    """
    """

    def __init__(self, user : int):
        self.user = user
        self.uid = environ.get("SQL_DB_UID").strip()
        self.pw = environ.get("SQL_DB_PW").strip()

    async def execute_get(self):
        """
        Gets the user's list of characters
        """
        character_list = await self.get_characters()
        character_list_json = {
            "characters" :  [c.to_dict() for c in character_list]
        }
        return dumps(character_list_json)

    async def connect(self):
        driver = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:feyre-db-server.database.windows.net,1433;Database=FeyreDB;"+"Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(self.uid, self.pw)
        cnxn = await aioodbc.connect(dsn=driver)

        return cnxn

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
                character = Character(user = self.user, is_active=bool(result.selected), name = result.characterName, initiative_value = str(result.initMod))
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
