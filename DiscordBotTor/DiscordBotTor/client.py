#id 500733845856059402
#token NTAwNzMzODQ1ODU2MDU5NDAy.DqPI-g.BBe4LLMfN3QFmrZXOK3mTNwSpws
#permissions 67648
#https://discordapp.com/oauth2/authorize?client_id=500733845856059402&scope=bot&permissions=67648

import discord
import asyncio
import BookOfTor
import DiceRolls
import time

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        ts = time.gmtime()
        t = time.strftime("%Y-%m-%d %H:%M:%S", ts)
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content.lower().startswith('!horo'):
            print(f"Received command: {message.content.lower()} from {message.author} at {t}")       
            await message.channel.send(f"<@{message.author.id}>" + "\n" + bt.horo())

        if message.content.lower().startswith('!zodiac'):
            print(f"Received command: {message.content.lower()} from {message.author} at {t}")       
            await message.channel.send(f"<@{message.author.id}>" + "\n" + bt.zodiac())

        if message.content.lower().startswith('!hello'):
            embed = discord.Embed()
            embed.set_image(url='https://cdn.discordapp.com/attachments/352281669992185866/500780935638155264/kOXnswR.gif')
            print(f"Received command: {message.content.lower()} from {message.author} at {t}")       

            await message.channel.send(embed=embed)

        if message.content.lower().startswith('!styles'):
            print(f"Received command: {message.content.lower()} from {message.author} at {t}")
            await message.channel.send(f"<@{message.author.id}>" + "\n" + bt.styles())

        if message.content.lower().startswith('!randchar'):         
            print(f"Received command: {message.content.lower()} from {message.author} at {t}")
            await message.channel.send(f"<@{message.author.id}>" + "\n" + bt.ranchar())

        if message.content.lower().startswith('!roll'):         
            print(f"Received command: {message.content.lower()} from {message.author} at {t}")
            await message.channel.send(f"<@{message.author.id}>" + "\n" + dr.roll(message.content))

        if message.content.lower().startswith('!uok'):
            print(f"Received command: {message.content.lower()} from {message.author} at {t}")
            await message.channel.send(f"<@{244286371181625344}>" + "\n" + "You okay?")

        if message.content.lower().startswith('!help'):
            print(f"Received command: {message.content.lower()} from {message.author} at {t}")       
            await message.channel.send('''Hello! My name is Feyre and I am the official Book of Tor Bot.

**Commands:**
   > !help: Displays all commands.
   > !hello: Is this even necessary?
   > !horo: Gives a Torian Horoscope
   > !randchar: Gives a random race and class combination
   > !roll #dSize: Rolls a number of dice. Ex: !roll 5d20 (does not accept modifiers at this time)
   > !styles: Lists all character styles
   > !zodiac: Gives a Primidia's Zodiac animal 
   

Please message <@112041042894655488> if you have any questions/issues.''')

global bt 
bt = BookOfTor.BookOfTor()

global dr
dr = DiceRolls.Roller()

client = MyClient()
client.run("NTAwNzMzODQ1ODU2MDU5NDAy.DqPI-g.BBe4LLMfN3QFmrZXOK3mTNwSpws")


