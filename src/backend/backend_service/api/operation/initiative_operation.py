import traceback

from json import dumps, loads
from random import randint
from unicodedata import name
from unittest import result

from backend_service.api.operation.roll_operation import RollOperation
from backend_service.api.operation.character_operation import CharacterOperation

from backend_service.api.model.character_model import Character
from backend_service.api.model.initiative_tracker_model import InitiativeTracker
from common.redis_helper import RedisHelper

class InitiativeOperation():
    """
    Operation that edits an initiative tracker resource
    """

    def __init__(self, user : int = None, guild : int = None, channel : int = None, message_id :int = None, character_name : str = None, initiative_expression : str = None):
        self.user = user
        self.guild = guild
        self.channel = channel
        self.message_id = message_id
        self.character_name = character_name
        self.initiative_expression = initiative_expression
        self.redis_helper = RedisHelper()

    async def execute_get(self):
        """
        Gets the initiative tracker from Redis

        Returns:
            Tracker JSON if present in Redis
            None if not present
        """
        tracker = await self.get_tracker()
        if tracker:
            return dumps(tracker.to_dict())
        else:
            tracker = await self.new_tracker(guild = self.guild, channel = self.channel)
            return dumps(tracker.to_dict())

    async def execute_put(self):
        """
        Updates the  initiative tracker with a new character.

        If the tracker does not exist, create a new one

        Returns:
            The updated initiative tracker as a dictionary
        """

        tracker = await self.get_tracker()

        # If tracker is not present in Redis then create a new one
        if not tracker:
            tracker = await self.new_tracker(guild=self.guild, channel=self.channel)

        # If they provided the character and modifier then just use that!
        if self.character_name and self.initiative_expression:
            character = Character(user = self.user, name = self.character_name, initiative_expression = self.initiative_expression)
            await self.add_character(tracker=tracker, character=character)
        # Otherwise need to query the database
        else:
            print("Query the database and get the user's character!", flush = True)
            character = await self.get_selected_char(user=self.user)
            await self.add_character(tracker=tracker, character=character)

        # Put the tracker back into Redis
        await self.put_tracker(tracker)

        return dumps(tracker.to_dict())
        
    async def execute_patch(self):
        """
        Increment's the initiative tracker's turn order

        Returns:
            The update initiative tracker as a dictionary
        """

        # Should probably add some error handling here in case the tracker does not exist
        # Although if the request comes from the frontend the tracker will need to exist
        tracker = await self.get_tracker()
        if tracker:
            tracker.turn += 1
            await self.put_tracker(tracker)
            return dumps(tracker.to_dict())
        return None
    
    async def execute_patch_message_id(self):
        """
        Updates the tracker's message id

        Returns:
            The update initiative tracker as a dictionary
        """

        tracker = await self.get_tracker()
        if tracker:
            tracker.message_id = self.message_id
            await self.put_tracker(tracker)
            return dumps(tracker.to_dict())
        return None

    async def execute_delete(self, character_name = None):
        """
        If character_name and user is provided, then just delete that character

        Otherwise delete the tracker

        Returns:
            Updated initiative tracker as a dictionary if a character was deleted

            True/False if the whole tracker was deleted
        """

        if character_name:
            tracker = await self.get_tracker()
            await self.remove_character(tracker, character_name)
            await self.put_tracker(tracker)
            return dumps(tracker.to_dict())
        else:
            
            return dumps({"result": self.redis_helper.delete_initiative_tracker(self.guild, self.channel)})

    async def get_selected_char(self, user):
        """
        Gets the user's selected character and its initiative modifer from the SQL data base.
        """
        character = await CharacterOperation(user = user).get_active_character()
        return character

    async def add_character(self, tracker : InitiativeTracker, character : Character):
        """
        Adds the character to the tracker's list and sorts the list by initiative roll
        """
        character.initiative_value = loads(RollOperation(character.initiative_expression).execute())['parent_result'][0]['total']

        # Don't allow duplicate characters
        # If a duplicate character is added, we re-roll its initiative
        for c in tracker.characters:
            if c.name == character.name:
                tracker.characters.remove(c)
                break
            
        tracker.characters.append(character)
        tracker.characters.sort(key=lambda c: float(c.initiative_value), reverse=True)

    async def remove_character(self, tracker : InitiativeTracker, character_name : str):
        """
        Removes the specified character from initiative
        """
        
        for i, c in enumerate(tracker.characters):
            if c.name == character_name:
                del tracker.characters[i]
                break
        tracker.characters.sort(key=lambda c: float(c.initiative_value), reverse=True)

    async def get_tracker(self):
        """
        Gets the initiative tracker from Redis, converts it to an InitiativeTracker object

        Returns:
            InitiativeTracker object if present in Redis
            None if not present in Redis
        """
        tracker_json = self.redis_helper.get_initiative_tracker(self.guild, self.channel)
        if tracker_json:
            return InitiativeTracker(it_dict=tracker_json)
        else:
            return None

    async def put_tracker(self, tracker : InitiativeTracker):
        """
        Puts the provided tracker object into Redis after converting it to a JSON string

        Returns:
            IDK, it doesnt really need to return anything... Maybe True/False for Success/Fail?
        """
        tracker_json = dumps(tracker.to_dict())
        return self.redis_helper.put_initiative_tracker(guild = tracker.guild, channel = tracker.channel, tracker = tracker_json)

    async def new_tracker(self, guild : int = None, channel : int = None):
        """
        Creates and returns a new empty tracker object

        Returns:
            An empty tracker
        """
       
        tracker = InitiativeTracker(guild=guild, channel=channel)
        await self.put_tracker(tracker = tracker)
        return tracker