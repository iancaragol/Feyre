from decimal import InvalidOperation
import traceback
import textwrap
import aioodbc
import logging

from os import environ
from urllib import response
from itertools import count, filterfalse
from json import dumps, loads
from backend_service.api.model.character_model import Character
from common.table_helper import TableHelper
from common.logger import LoggerNames

# TODO(IAN)
# Not sure where to put this
logger = logging.getLogger(LoggerNames.backend_logger)
table_helper = TableHelper(logger=logger)

class CharacterOperation():
    """
    """

    def __init__(self, user : int, character_id : int = None, character_name : str = None, init_mod : str = None, logger = None):
        self.user = user
        self.character_id = character_id
        self.character_name = character_name
        self.init_mod = init_mod
        self.logger = logger

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

    # TODO(Ian):
    # This could be in a helper class rather than being part of the operation?
    # This breaks the backend contract, we talk directly to azure storage instead of redis
    #
    # Example Table Storage JSON:
    # {
    # "characters": [
    #         {
    #             "user": 112041042894655488,
    #             "name": "Frodo",
    #             "initiative_expression": "1d20",
    #             "initiative_value": null,
    #             "is_active": true,
    #             "id": 0
    #         },
    #         {
    #             "user": 112041042894655488,
    #             "name": "Sam",
    #             "initiative_expression": "1d20+5",
    #             "initiative_value": null,
    #             "is_active": false,
    #             "id": 1
    #         }
    #     ]
    # }

    async def select_character(self):
        """
        Updates the character to be the selected character
        """
        self.logger.info(f"[CHAR > DELETE] Removing character for {self.user} with ID {self.character_id}")

        characters_json = await self.get_characters_json()

        if characters_json:
            characters = characters_json["characters"]

            for character in characters:
                # Unselect any selected characters
                if (character["is_active"] and character["id"] != self.character_id):
                    character["is_active"] = False
                elif (character["id"] == self.character_id):
                    character["is_active"] = True

            self.logger.info(f"[CHAR > DELETE] New character list: {character}")

            characters_as_entity = {"RowKey": str(self.user), "character_json": dumps({"characters":characters})}
            table_helper.insert_entity(table_name = "characters", entity_json = characters_as_entity)

            self.logger.info(f"[CHAR > DELETE] Removed character for {self.user} with ID {self.character_id}")

    async def get_characters_json(self):
        entry = table_helper.get_entity("characters", self.user)
        self.logger.info(f"[CHAR > GET] Got {entry} from table storage. User ID: {self.user}")

        character_json = None
        if entry:
            character_json = loads(entry["character_json"])
        return character_json

    async def get_characters(self):
        entry = table_helper.get_entity("characters", self.user)
        character_list = []

        self.logger.info(f"[CHAR > GET] Got {entry} from table storage. User ID: {self.user}")

        characters_json = await self.get_characters_json()
        if characters_json:
            for character in characters_json["characters"]:
                character = Character(user = self.user, id=int(character["id"]), is_active=character["is_active"], name = character["name"], initiative_expression = str(character["initiative_expression"]))
                character_list.append(character)

        self.logger.info(f"[CHAR > GET] Character list for {self.user}: {character_list}")

        return character_list

    async def get_active_character(self):
        self.logger.info(f"[CHAR > GET] Getting active characters for {self.user}")

        characters = await self.get_characters()

        active_character = None
        for character in characters:
            if character.is_active:
                active_character = character
                return active_character
        
        self.logger.info(f"[CHAR > GET] Found active character for {self.user}: {active_character}")
        return active_character

    async def add_character(self):
        self.logger.info(f"[CHAR > ADD] Adding new character for {self.user}")

        # Get our character json
        characters_json = await self.get_characters_json()

        # If there is no character_json then we need to create one
        if (characters_json == None):
            characters_json = {"characters": []}

        # This is a bit messy, but characters is a list []
        characters = characters_json["characters"]

        # Wizardry to get the smallest id not already taken
        character_id = 1
        ids = []
        if characters:
            ids = [c["id"] for c in characters]
            character_id = int(next(filterfalse(set(ids).__contains__, count(1))))
        
        if character_id > 9:
            raise InvalidOperation(message="Maximum # of characters reached")

        is_active = 0 # If there are no characters select the new one by default
        if len(ids) == 0:
            is_active = 1

        # Construct new character json
        new_character = {}
        new_character["name"] = self.character_name
        new_character["initiative_expression"] = self.init_mod
        new_character["user"] = self.user
        new_character["id"] = character_id
        new_character["is_active"] = is_active

        # Add the new character json to the list
        characters.append(new_character)

        self.logger.info(f"[CHAR > ADD] New character json: {characters}")

        # This is funky, but basically an entity is a representation of columns
        characters_as_entity = {"RowKey": str(self.user), "character_json": dumps({"characters":characters})}
        table_helper.insert_entity(table_name = "characters", entity_json = characters_as_entity)

        self.logger.info(f"[CHAR > ADD] Inserted new json.")

    async def remove_character(self):
        self.logger.info(f"[CHAR > DELETE] Removing character for {self.user} with ID {self.character_id}")

        characters_json = await self.get_characters_json()

        if characters_json:
            characters = characters_json["characters"]
            new_characters = [x for x in characters if not (x["id"] == self.character_id)]
        
            self.logger.info(f"[CHAR > DELETE] New character list: {new_characters}")

            characters_as_entity = {"RowKey": str(self.user), "character_json": dumps({"characters":new_characters})}
            table_helper.insert_entity(table_name = "characters", entity_json = characters_as_entity)

            self.logger.info(f"[CHAR > DELETE] Removed character for {self.user} with ID {self.character_id}")


