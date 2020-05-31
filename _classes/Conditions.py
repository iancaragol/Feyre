import os
import difflib
import random
import asyncio
import csv

class ConditionLookup():
    def __init__(self):
        self.condition_dictionary = {}
        self.setup()

    def setup(self):
        pyDir = os.path.dirname(__file__)
        relPath = "/../_data/_conditions/conditions.csv"
        absRelPath = pyDir + relPath
        with open(absRelPath) as items:
            item_reader = csv.reader(items)
            for row in item_reader:
                new_item = Condition(row[0], row[1])
                self.condition_dictionary[new_item.name.lower()] = new_item
        print("Condtions loaded in Conditions.py")

    async def search(self, args):
        matches = difflib.get_close_matches(args.strip().lower(), self.condition_dictionary.keys())
        ret_string = ""

        if len(matches) == 1:
            ret_string = self.condition_dictionary[matches[0]].to_string()
        elif len(matches) < 1:
            ret_string = '''```I wasn't able to find the condition you are looking for.```'''
        elif len(matches) > 1:
            ret_string = self.condition_dictionary[matches[0]].to_string_match(self.condition_dictionary[matches[1]].name)

        return ret_string

    

class Condition():
    def __init__(self, name, description):
        self.name = str(name)
        self.description = str(description)

    def to_string(self):
        code_block = '''```asciidoc
[{}]
{}```'''.format(self.name, self.description)

        return code_block
    
    def to_string_match(self, second_closest):
        code_block = '''```asciidoc
[{}]
{}

Did you mean {}?```'''.format(self.name, self.description,  second_closest)

        return code_block
