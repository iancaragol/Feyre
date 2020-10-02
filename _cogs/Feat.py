import os
import difflib
import random
import asyncio
import csv
import textwrap
import discord
import whoosh
import bisect
import numpy

from discord.ext import commands
from whoosh.fields import Schema, TEXT
import os.path
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser

class Feat:
    def __init__(self, title, link):
        self.title = title
        self.link = link
        self.feat_msg =  "\n\nFeats are not part of the Standard Reference Document so, due to copyright concerns, I can not display them here."


    def to_embed(self):
        desc = self.link + self.feat_msg
        embed = discord.Embed(title=self.title, description=desc)
        return embed

class FeatLookup:
    def __init__(self):
        self.feat_dictionary = {}
        self.ix = None
        self.setup()

    def setup(self):
        pyDir = os.path.dirname(__file__)
        relPath = "/../_data/_feats/feat_links.csv"
        absRelPath = pyDir + relPath
        with open(absRelPath, encoding='utf-8') as feats:
            feat_reader = csv.reader(feats)
            for row in feat_reader:
                new_feat = Feat(row[0], row[1])
                self.feat_dictionary[new_feat.title] = new_feat
        print("Feats loaded in Feat.py")

        # Fancy searching
        schema = Schema(title=TEXT(stored=True))
        if not os.path.exists("_index/feats"):
            os.mkdir("_index/feats")
        self.ix = create_in("_index/feats", schema)

        self.ix = open_dir("_index/feats")
        writer = self.ix.writer()
        for v in self.feat_dictionary.values():
            title = f"{v.title}"
            writer.add_document(title=title)
        writer.commit()

        print("Setup indexer in Feat.py")

    async def search(self, args):
        qp = QueryParser('title', schema=self.ix.schema)
        q = qp.parse(args, "utf-8")
        r = None
        with self.ix.searcher() as searcher:
            results = searcher.search(q)

            if len(results) > 0:
                abil = self.feat_dictionary[results[0]['title']]
                return abil.to_embed()
        return r

class FeatLookupCog(commands.Cog):
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
        self.cfl = FeatLookup()

    @commands.command(aliases = ['Feat'])
    async def feat(self, ctx, *, args = None):
        self.data.userSet.add(ctx.author.id)
        self.data.statsDict['!feat'] += 1

        if args:
            result = await self.cfl.search(args)
            
            if not result:
                await ctx.send("```I could not find the feat you are looking for.```")

            await ctx.send(embed=result)
        else:
            await ctx.send("```Missing command arguments. You must include the name of the feat you are searching for. Like this: !feat grapper\n\nSee !help feat for details.```")

    