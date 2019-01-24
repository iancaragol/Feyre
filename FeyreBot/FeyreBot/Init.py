class Initiative():
    """
    Keeps track of iniative on a guild, channel basis.
    """
    def __init__(self):
        self.playerList = []

    def addPlayer(self, Name = None, init = 0):
        """
        Adds a new player to the list of players with the format (Name, Initiative roll)
        """
        updated = False
        for i in range(0, len(self.playerList)):
            if(self.playerList[i][0] == Name):
                self.playerList[i] = (Name, init)
                updated = True       
        if(not updated):
            self.playerList.append((Name, init))

    def removePlayer(self, name):
        toremove = -1
        for i in range(0, len(self.playerList)):
            if(self.playerList[i][0] == name):
                toremove = i;

        if(toremove != -1):
            del(self.playerList[toremove]);
            return True
        else:
            return False

    def displayInit(self):
        """
        Sorts players by their iniative and returns a string for display as an embedded message
        """
        if(len(self.playerList) == 0):
            return ''


        sortedInit = sorted(self.playerList, key=lambda x: int(x[1]))
        sortedInit.reverse()

        displayStr = ""

        for (nu, iq) in sortedInit:
            displayStr += f"\n{nu}: {iq}"

        return displayStr
