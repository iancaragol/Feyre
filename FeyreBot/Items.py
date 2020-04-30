import os
import difflib
import random
import asyncio
import csv

class ItemLookup():
    def __init__(self):
        self.item_dictionary = {}
        self.setup()

    def setup(self):
        item_filepath = "/FeyreBot/_data/_items/5e magic items.csv"
        with open(os.getcwd() + item_filepath) as items:
            item_reader = csv.reader(items)
            for row in item_reader:
                new_item = Item(row[0], row[1], row[2], row[3], row[4], row[5])
                self.item_dictionary[new_item.name.lower()] = new_item
        print("Items loaded in Items.py")

    async def search(self, args):
        matches = difflib.get_close_matches(args.strip().lower(), self.item_dictionary.keys())
        ret_string = ""

        if len(matches) == 1:
            ret_string = self.item_dictionary[matches[0]].to_string()
        elif len(matches) < 1:
            ret_string = '''```I wasn't able to find the item you are looking for.```'''
        elif len(matches) > 1:
            ret_string = self.item_dictionary[matches[0]].to_string_match(self.item_dictionary[matches[1]].name)

        return ret_string

    

class Item():
    def __init__(self, name, rarity, item_type, attunement, description, pg_number):
        self.name = str(name)
        self.rarity = str(rarity)
        self.item_type = str(item_type)
        if len(attunement) == 0:
            attunement = "attunement not required"
        self.attunement = str(attunement)
        self.description = str(description)
        self.pg_number = pg_number

    def to_string(self):
        if len(self.pg_number) > 1:
            code_block = '''```asciidoc
[{}]
- {}, {}
- {}
- pg# {}

{}```'''.format(self.name, self.rarity, self.item_type, self.attunement, self.pg_number, self.description)

            return code_block
        
        else: 
            code_block = '''```asciidoc
[{}]
- {}, {}
- {}

{}```'''.format(self.name, self.rarity, self.item_type, self.attunement, self.description)

            return code_block

    def to_string_match(self, second_closest):
        if len(self.pg_number) > 1:
            code_block = '''```asciidoc
[{}]
- {}, {}
- {}
- pg# {}

{}

Did you mean {}?```'''.format(self.name, self.rarity, self.item_type, self.attunement, self.pg_number, self.description,  second_closest)
        else:
            code_block = '''```asciidoc
[{}]
- {}, {}
- {}

{}

Did you mean {}?```'''.format(self.name, self.rarity, self.item_type, self.attunement, self.description,  second_closest)


        return code_block
