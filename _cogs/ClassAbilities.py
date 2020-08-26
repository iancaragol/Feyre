import os
import difflib
import random
import asyncio
import csv
import textwrap
import discord
import whoosh
from discord.ext import commands
from whoosh.fields import Schema, TEXT
import os.path
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser

class Ability:
    def __init__(self, character_class, ability_name, ability_description):
        self.character_class = character_class
        self.ability_name = ability_name
        self.ability_description = ability_description

    def to_string(self):
        s = f"```asciidoc\n" \
            f"[{self.character_class} - {self.ability_name}]\n\n" \
            f"{self.ability_description}```"

        return s

    def to_string_matches(self, match):
        s = f"```asciidoc\n" \
            f"[{self.character_class} - {self.ability_name}]\n\n" \
            f"{self.ability_description}\n\n" \
            f"Did you mean {match}?```"

        return s

class ClassAbilityLookup:
    def __init__(self):
        self.ability_dictionary = {}
        self.ix = None
        self.setup()

    def setup(self):
        pyDir = os.path.dirname(__file__)
        relPath = "/../_data/_class_abilities/class_abilities.csv"
        absRelPath = pyDir + relPath
        with open(absRelPath) as abilitys:
            ability_reader = csv.reader(abilitys)
            for row in ability_reader:
                new_ability = Ability(row[0], row[1], row[2])
                self.ability_dictionary[f"{new_ability.character_class} - {new_ability.ability_name}"] = new_ability
        print("Abilities loaded in ClassAbilities.py")

        # Fancy searching
        schema = Schema(title=TEXT(stored=True))
        if not os.path.exists("_index"):
            os.mkdir("_index")
        self.ix = create_in("_index", schema)

        self.ix = open_dir("_index")
        writer = self.ix.writer()
        for v in self.ability_dictionary.values():
            title = f"{v.character_class} - {v.ability_name}"
            writer.add_document(title=title)
        writer.commit()

        print("Setup indexer.")

    async def search(self, args):
        qp = QueryParser('title', schema=self.ix.schema)
        q = qp.parse(args, "utf-8")
        r = None
        with self.ix.searcher() as searcher:
            results = searcher.search(q)

            if len(results) > 0:
                abil = self.ability_dictionary[results[0]['title']]
                return abil.to_string()
        return r

class ClassAbilityLookupCog(commands.Cog):
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
        self.cal = ClassAbilityLookup()

    @commands.command()
    async def ability(self, ctx, *, args = None):
        if args:
            result = await self.cal.search(args)
            if result:
                await ctx.send(result)
            else:
                await ctx.send("```I could not find what you are looking for. If it isn't in the PHB I cannot support it for copyright reasons.\n\nThink this is a bug? Please report it with the !request command.```")
        else:
            await ctx.send("`Missing command arguments. See !help ability for examples.`")