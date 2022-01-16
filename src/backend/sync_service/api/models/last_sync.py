from datetime import datetime

class LastSync:
    """
    Holds info on the last sync operation
    """
    def __init__(self):
        self.message = "command_stats has not been synced since service startup."
        self.completed_successfully = False
        self.who_updated = "nobody"
        self.sync_time = datetime.fromtimestamp(0).strftime("%m/%d/%Y, %H:%M:%S")
        self.sync_timestamp = datetime.fromtimestamp(0).timestamp()

    def to_dict(self):
        """
        Returns the object as a dictionary
        """
        d = {}
        d["message"] = self.message
        d["completed_successfully"] = self.completed_successfully
        d["who_updated"] = self.who_updated
        d["sync_time"] = self.sync_time
        d["sync_timestamp"] = self.sync_timestamp