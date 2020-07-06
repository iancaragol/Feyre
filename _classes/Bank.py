import pyodbc
import textwrap
import asyncio

from itertools import count, filterfalse
from os import path

class Character():
    def __init__(self, user_id, character_name, character_id, pp, gp, ep, sp, cp):
        self.user_id = user_id
        self.character_name = character_name
        self.character_id = character_id
        self.pp = pp
        self.gp = gp
        self.ep = ep
        self.sp = sp
        self.cp = cp

class Bank():
    def __init__(self):
        self.uid = ""
        self.pw = ""

        pyDir = path.dirname(path.dirname(__file__))
        with open(path.join(pyDir, 'db_user.txt'), 'r') as file:
            self.uid = file.readline().strip()
            self.pw = file.readline().strip()

    async def connect(self):
        uid = "ian"
        pw = "S1n0nChan<3!"
        driver = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:feyre-db-server.database.windows.net,1433;Database=FeyreDB;"+"Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(uid, pw)
        cnxn = pyodbc.connect(driver)

        return cnxn

    async def deposit(self, user_id, character_name, character_id, pp, gp, ep, sp, cp):
        cnxn = self.connect()
        cursor = cnxn.cursor()

        # Select current values
        # Lets do only user_id and char_id for now
        current_character = self.get_character(user_id, character_name, character_id)

        if current_character: # If this character exists
            if character_id:
                update_string = textwrap.dedent("""
                UPDATE Banks SET pp = ?, gp = ?, ep = ?, sp = ?, cp = ? WHERE user_id = ? AND character_id = ?""")
                cursor.execute(update_string,
                               current_character.pp + pp,
                               current_character.gp + gp,
                               current_character.ep + ep,
                               current_character.sp + sp,
                               current_character.cp + cp,
                               user_id, 
                               character_id)

                cnxn.commit()

                return """```Deposited {pp}pp, {gp}gp, {ep}ep, {sp}sp, {cp}cp into {current_character.character_name}'s account.```"""
            
            if character_name:
                update_string = textwrap.dedent("""
                UPDATE Bank SET pp = ?, gp = ?, ep = ?, sp = ?, cp = ? WHERE user_id = ? AND character_name = ?""")
                cursor.execute(update_string,
                               current_character.pp + pp,
                               current_character.gp + gp,
                               current_character.ep + ep,
                               current_character.sp + sp,
                               current_character.cp + cp,
                               user_id, 
                               character_name)

                cnxn.commit()

                return """```Deposited {pp}pp, {gp}gp, {ep}ep, {sp}sp, {cp}cp into {current_character.character_name}'s account.```"""
        
        else:
            return """```I couldn't find a character by that name or id. Try !bank to see your characters.```"""

    async def get_character(self, user_id, character_name, character_id):
        cnxn = self.connect()
        cursor = cnxn.cursor()

        if character_id:
            selection_string = textwrap.dedent(""" 
                SELECT * From Bank WHERE user_id = ?  AND character_id = ?""")
            cursor.execute(selection_string, user_id, character_id)
            results = cursor.fetchall()

            if results:
                return Character(user_id, results[0].character_name, results[0].character_id, results[0].pp, results[0].gp, results[0].ep, results[0].sp, results[0].cp)
            else:
                return None

        elif character_name:
            selection_string = textwrap.dedent(""" 
                SELECT * From Bank WHERE user_id = ?  AND character_name = ?""")
            cursor.execute(selection_string, user_id, character_name)
            results = cursor.fetchall()

            if results:
                return Character(user_id, results[0].character_name, results[0].character_id, results[0].pp, results[0].gp, results[0].ep, results[0].sp, results[0].cp)
            else:
                return None

    async def get_characters(self, user_id):
        cnxn = self.connect()
        cursor = cnxn.cursor()

        selection_string = textwrap.dedent(""" 
            SELECT * From Bank WHERE user_id = ?""")

        cursor.execute(selection_string, user_id)
        results = cursor.fetchall()

        characters = []

        if results:
            for result in results:
                character = Character(user_id, result.character_name, result.character_id, result.pp, result.gp, result.ep, result.sp, result.cp)
                characters.append(character)

        return characters
    
    async def get_characters_formatted(self, user_id):
        code_block = textwrap.dedent("""
        ```asciidoc
        = $ Bank $ =
        [Character | ID]""")

        for c in await self.get_characters(user_id):
            code_block += c.character_name
            code_block += " | "
            code_block += str(c.character_id)

        code_block += "```"
        return str(code_block)


    async def add_character(self, user_id, character_name):
        cnxn = self.connect()
        cursor = cnxn.cursor()

        characters = self.get_characters(user_id)

        insert_string = textwrap.dedent("""
            INSERT INTO Bank(user_id, character_name, character_id, pp, gp, ep, sp, cp) VALUES(?,?,?,?,?,?,?,?)""")

        # Wizardry to get the smallest id not already taken
        ids = [c.character_id for c in characters]
        character_id = next(filterfalse(set(ids).__contains__, count(1)))

        try:
            cursor.execute(insert_string, user_id, character_name, character_id, 0, 0, 0, 0, 0)
            cnxn.commit()

        except pyodbc.IntegrityError:
            return """```You already have a character by that name. Try !bank to see your characters.```"""

    async def remove_character(self, user_id, character_name, character_id):
        cnxn = self.connect()
        cursor = cnxn.cursor()

        delete_character = self.get_character(user_id, character_name, character_id)

        if delete_character:
            if character_name:
                delete_string = textwrap.dedent("""
                DELETE FROM Bank WHERE user_id = ? and character_name = ?""")
                cursor.execute(delete_string, user_id, character_name)
                cnxn.commit()
                return """```{delete_character.character_name} was removed from your bank.```"""
            
            elif character_id:
                delete_string = textwrap.dedent("""
                DELETE FROM Bank WHERE user_id = ? and character_id = ?""")
                cursor.execute(delete_string, user_id, character_id)
                cnxn.commit()
                return """```{delete_character.character_name} was removed from your bank.```"""

        else:
            return """```{delete_character.character_name} does not have a bank account. Try !bank to see your characters.```"""
            
        

# def main():
#     b = Bank()
#     b.add_character(0, "Test Character")
#     b.deposit(0, "Test Character", 0, 1, 2, 3, 4, 5)

#     b.remove_character(0, "Test Character", 0)

# if __name__ == "__main__":
#     main()