import os
import difflib
import csv
from discord.ext import commands

class ItemLookup():
    def __init__(self):
        self.item_dictionary = {}
        self.setup()

    def setup(self):
        pyDir = os.path.dirname(__file__)
        relPath = "/../_data/_items/5e magic items.csv"
        absRelPath = pyDir + relPath
        with open(absRelPath) as items:
            item_reader = csv.reader(items)
            for row in item_reader:
                new_item = Item(row[0], row[1], row[2], row[3], row[4], row[5])
                self.item_dictionary[new_item.name.lower()] = new_item
        # print("Items loaded in Items.py")

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

class ItemLookupCog(commands.Cog):
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
        self.item_lookup = ItemLookup()

    @commands.command(aliases = ['Item'])
    async def item(self, ctx, *, args = None):
        self.data.userSet.add(ctx.author.id)
        self.data.statsDict['!item'] += 1

        if not args:
            await ctx.send('''```Missing the search argument! See !help item for more info.```''')
            return

        item = await self.item_lookup.search(args)

        if len(item) >= 1997 and len(item) < 3997:
            item1 = item[0:1990] + '```'
            item2 = '```diff\n' + item[1991:]
            await ctx.send(item1)
            await ctx.send(item2)

        elif len(item) >= 3997 and len(item) < 5980:
            item1 = item[0:1990] + '```'
            item2 = '```diff\n' + item[1990:3979] + '```'
            item3 = '```diff\n' + item[3979:]
            await ctx.send(item1)
            await ctx.send(item2)
            await ctx.send(item3)

        elif len(item) >= 5980:
            item1 = item[0:1990] + '```'
            item2 = '```diff\n' + item[1990:3979] + '```'
            item3 = '```diff\n' + item[3979:5979] + '```'
            item4 = '```diff\n' + item[5979:]
            await ctx.send(item1)
            await ctx.send(item2)
            await ctx.send(item3)
            await ctx.send(item4)
        
        else:
            await ctx.send(item)