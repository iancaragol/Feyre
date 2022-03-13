import traceback

from json import dumps, loads
from random import randint
from unicodedata import name

from backend_service.api.operation.roll_operation import RollOperation

from backend_service.api.model.character_model import Character
from backend_service.api.model.initiative_tracker_model import InitiativeTracker
from common.redis_helper import RedisHelper

class InitiativeOperation():
    """
    Operation that takes a dice expression, evaluates it, and returns a list of ParentRollModels
    """

    def __init__(self, user : int, guild : int, channel : int, character_name : str = None, initiative_expression : str = None):
        self.user = user
        self.guild = guild
        self.channel = channel
        self.character_name = character_name
        self.initiative_expression = initiative_expression
        self.redis_helper = RedisHelper()


    def execute_get(self):
        """
        Gets the initiative tracker from Redis

        Returns:
            Tracker JSON if present in Redis
            None if not present
        """
        tracker = self.get_tracker()
        if tracker:
            return dumps(tracker.to_dict())
        return None

    def execute_put(self):
        """
        Updates the  initiative tracker with a new character.

        If the tracker does not exist, create a new one

        Returns:
            The updated initiative tracker as a dictionary
        """

        tracker = self.get_tracker()

        # If tracker is not present in Redis then create a new one
        if not tracker:
            tracker = self.new_tracker(guild=self.guild, channel=self.channel)

        # If they provided the character and modifier then just use that!
        if self.character_name and self.initiative_expression:
            character = Character(self.user, self.character_name, self.initiative_expression)
            self.add_character(tracker=tracker, character=character)
        # Otherwise need to query the database
        else:
            print("Query the database and get the user's character!", flush = True)

        # Put the tracker back into Redis
        self.put_tracker(tracker)

        return dumps(tracker.to_dict())
        
    def execute_patch(self):
        """
        Increment's the initiative tracker's turn order

        Returns:
            The update initiative tracker as a dictionary
        """

        # Should probably add some error handling here in case the tracker does not exist
        # Although if the request comes from the frontend the tracker will need to exist
        tracker = self.get_tracker()
        tracker.turn += 1
        self.put_tracker(tracker)
        return dumps(tracker.to_dict())

    def execute_delete(self):
        """
        Deletes the old tracker from Redis

        Returns:
            True/False if the operation was successful
        """

        return self.redis_helper.delete_initiative_tracker(self.guild, self.channel)

    def add_character(self, tracker : InitiativeTracker, character : Character):
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
        tracker.characters.sort(key=lambda c: c.initiative_value, reverse=True)

    def get_tracker(self):
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

    def put_tracker(self, tracker : InitiativeTracker):
        """
        Puts the provided tracker object into Redis after converting it to a JSON string

        Returns:
            IDK, it doesnt really need to return anything... Maybe True/False for Success/Fail?
        """
        tracker_json = dumps(tracker.to_dict())
        return self.redis_helper.put_initiative_tracker(guild = tracker.guild, channel = tracker.channel, tracker = tracker_json)

    def new_tracker(self, guild : int = None, channel : int = None):
        """
        Creates and returns a new empty tracker object

        Returns:
            An empty tracker
        """
       
        tracker = InitiativeTracker(guild=guild, channel=channel)
        return tracker