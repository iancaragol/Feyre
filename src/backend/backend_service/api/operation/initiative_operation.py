import traceback

from common.redis_helper import RedisHelper
from json import dumps, loads
from random import randint

class InitiativeOperation():
    """
    Operation that takes a dice expression, evaluates it, and returns a list of ParentRollModels
    """

    def __init__(self, user : int, guild : int, channel : int, character = None : str, init_mod = None : str):
        self.user = user
        self.guild = guild
        self.channel = channel
        self.character = None
        self.init_mod = None
        self.redis_helper = RedisHelper()

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
            tracker = self.new_tracker()

        # If they provided the character and modifier then just use that!
        if character and init_mod:
            print("Roll a dice and add the character to the tracker!", flush = True)
        # Otherwise need to query the database
        else:
            print("Query the database and get the user's character!", flush = True)

        # Put the tracker back into Redis
        self.put_tracker(tracker)

        return tracker
        
    def execute_patch(self):
        """
        Increment's the initiative tracker's turn order

        Returns:
            The update initiative tracker as a dictionary
        """
        tracker = self.get_tracker()
        tracker.turns += 1
        return tracker.to_dict()

    def execute_delete(self):
        """
        Deletes the old tracker from Redis

        Returns:
            True/False if the operation was successful
        """

        return self.redis_helper.delete_tracker(self.guild, self.channel)

    def add_character(self, tracker, character):
        """
        Adds the character to the tracker's list and sorts the list by initiative roll
        """
        # Create a new character, sort the list by character's roll?
        print("add_character", flush = True)

    def get_tracker(self):
        """
        Gets the initiative tracker from Redis, converts it to an InitiativeTracker object

        Returns:
            The InitiativeTracker object
        """
        tracker_json = loads(self.redis_helper.get_initiative_tracker(self.guild, self.channel))
        tracker = InitiativeTracker().from_dict(tracker_json)
        return tracker

    def put_tracker(self, tracker)
        """
        Puts the provided tracker object into Redis after converting it to a JSON string

        Returns:
            IDK, it doesnt really need to return anything... Maybe True/False for Success/Fail?
        """
        tracker_json = dumps(tracker.to_dict())
        return self.redis_helper.put_initiative_tracker(self.guild, self.channel, tracker_json)

    def new_tracker(self):
        """
        Creates and returns a new empty tracker object

        Returns:
            An empty tracker
        """
       
        tracker = InitiativeTracker()
        return tracker