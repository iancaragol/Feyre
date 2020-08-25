import discord
import textwrap
from discord.ext import commands
from operator import attrgetter
from _classes.DiceRolls import Roller
from _classes.CharacterSelection import CharacterSelectionHandler


class PlayerCharacter:
    def __init__(self, user_id, name, init_mod, init_value):
        self.user_id = user_id
        self.character_name = name
        self.init_mod = init_mod
        self.init_value = init_value


class InitiativeTracker:
    def __init__(self): 
        self.add_order = []
        self.character_list = []
        self.init_messages = []
        self.dr = Roller()
        self.content = ""
        self.header = "```asciidoc\n= Initiative ="
        self.footer = "```"
        self.round_count = 0
        self.marker_pos = 0
        self.verbose = False

        self.content = self.header + f"\n[Round: {self.round_count}]\n\nAdd characters to the tracker by pressing the + icon or using the !init command.\n\nEx: !init Gandalf -i 1d20+5```"

    async def add_player(self, user_id, name, init_mod):
        init_value = await self.dr.parse(init_mod, total_only=True) # Roll init_mod to get value
        new_pc = PlayerCharacter(user_id, name, init_mod, init_value)
        self.add_order.append(new_pc)
        self.character_list = list(self.add_order)

        self.character_list.sort(key = attrgetter('init_value'), reverse = True)

        if self.verbose:
            self.init_messages.append(f"{name} was added to initiative.")

    async def remove_player(self, user_id, name = None):
        if len(self.add_order) == 0:
            return

        if name: # If name is provided then remove specific character with that name
            self.add_order = [i for i in self.add_order if i.character_name != name] # Remove that character
            self.character_list = list(self.add_order)
            self.character_list.sort(key = attrgetter('init_value'), reverse = True)

            if self.verbose:
                self.init_messages.append(f"{name} was removed from initiative.")

        else: # If name is not provided then delete the most recent character added by that player
            i = len(self.character_list) - 1
            while(i > 0):
                if self.character_list[i].user_id == user_id:
                    break
                i -= 1

            if self.verbose:
                self.init_messages.append(f"{self.add_order[i].character_name} was removed from initiative.")
            del self.add_order[i]
            self.character_list = sorted(self.add_order, key=lambda x: x.init_value, reverse=True)

    async def update_player(self, user_id, name, init_mod):
        init_value = await self.dr.parse(init_mod, total_only=True)
        for c in self.character_list:
            if c.user_id == user_id and c.character_name == name:
                c.init_mod = init_mod
                c.init_value = init_value

    async def update_contents(self):
        self.content = ""
        self.content += self.header
        self.content += f"\n[Round: {self.round_count}]"
        for i in range(len(self.character_list)):
            if i == self.marker_pos:
                self.content += f"\n> {self.character_list[i].character_name} {self.character_list[i].init_value}"
            else:
                self.content += f"\n{self.character_list[i].character_name} {self.character_list[i].init_value}"

        self.content += "\n"
        count = 0
        for m in self.init_messages[::-1]:
            count += 1
            self.content += "\n" + m
            if count >= 3:
                break
        
        self.content += self.footer

    async def get_contents(self):
        return self.content

    async def parse_args(self, user_id, args):
        name = ""
        init_mod = ""

        # Ex: !init Gandalf -i 1d20
        if '-i' in args.strip().lower():
            name = args[:args.index('-i')].strip()
            init_mod = args[args.index('-i') + 2:].strip()
            await self.add_player(user_id, name, init_mod)


        elif '-r' in args.strip().lower():
            name = args[args.index('-r') + 2:].strip()

            if len(name) > 0:
                await self.remove_player(user_id, name=name) # If name exists then try and remove that name
            else:
                await self.remove_player(user_id) # Otherwise remove the last character added by that player
        else:
            split = args.splt(' ')
            for s in split:
                total = await self.dr.parse(s, total_only=True)
                print(total)

    async def move_marker(self):
        self.marker_pos += 1
        if self.marker_pos == len(self.character_list):
            self.round_count += 1
            self.marker_pos = 0

class InitiativeCog(commands.Cog):
    tracker_dict = {}
    msg_dict = {}
    plus = '➕'
    skull = '☠️'
    swords = '⚔️'

    def __init__(self, bot):
        self.bot = bot
        self.character_selector = CharacterSelectionHandler()

    @commands.command()
    async def init_cogs(self, ctx, *, args = None):
        tracker_key = str(ctx.guild.id) + ":" + str(ctx.channel.id)
        if not args and tracker_key not in self.tracker_dict.keys(): # No tracker in this channel
            await ctx.send("```asciidoc\nYou need to start an initiative tracker in this channel before adding a character using [!init start]```")
            return 

        if args:
            if 'start' in args:
                # Create initative tracker
                tracker = InitiativeTracker()

                if '-v' in args or '--verbose'  in args:
                    tracker.verbose = True

                self.tracker_dict[tracker_key] = tracker
                # Dont update contents here, otherwise the init start will be changed

                contents = await self.tracker_dict[tracker_key].get_contents()
                await self.send_msg_helper(ctx, tracker_key, contents, None, False)

            else:
                await self.tracker_dict[tracker_key].parse_args(ctx.author.id, args)
                await self.tracker_dict[tracker_key].update_contents()

                contents = await self.tracker_dict[tracker_key].get_contents()
                await self.send_msg_helper(ctx, tracker_key, contents, None, True)

            
        else:
            await ctx.send("`This doesnt do anything yet but it will add your active character`")

    async def add_reactions_helper(self, msg):     
        await msg.add_reaction(self.swords)
        await msg.add_reaction(self.plus)
        await msg.add_reaction(self.skull)

    async def send_msg_helper(self, ctx, tracker_key, contents, msg, repost):
        if not msg and not repost: # If this was called through a command and not through a reaction
            msg = await ctx.send(contents)
            self.msg_dict[tracker_key] = msg
            await self.add_reactions_helper(msg)

        elif msg and not repost:
            await msg.edit(content=contents)
            self.msg_dict[tracker_key] = msg

        elif not msg and repost:
            await self.msg_dict[tracker_key].delete()
            msg = await ctx.send(contents)
            self.msg_dict[tracker_key] = msg
            await self.add_reactions_helper(msg)
        
        reaction, user = await self.bot.wait_for('reaction_add', check=lambda r, u:u.id != self.bot.user.id and r.message.id == msg.id, timeout=21600) # Times out after 6 hours

        if reaction != None:
            if str(reaction.emoji) == self.plus:
                # Get users active character, add it to tracker, then update tracker contents for display
                new_character = await self.character_selector.get_selected_character(user.id)
                await self.tracker_dict[tracker_key].add_player(user.id, new_character.character_name, new_character.init_mod)
                await self.tracker_dict[tracker_key].update_contents()
                content = await self.tracker_dict[tracker_key].get_contents()

                await reaction.remove(user) # Remove users reaction
                await self.send_msg_helper(ctx, tracker_key, content, msg, False)

            elif str(reaction.emoji) == self.skull:
                # Get users active character, add it to tracker, then update tracker contents for display
                await self.tracker_dict[tracker_key].remove_player(user.id)
                await self.tracker_dict[tracker_key].update_contents()
                content = await self.tracker_dict[tracker_key].get_contents()

                await reaction.remove(user) # Remove users reaction
                await self.send_msg_helper(ctx, tracker_key, content, msg, False)

            elif str(reaction.emoji) == self.swords:
                await self.tracker_dict[tracker_key].move_marker()
                await self.tracker_dict[tracker_key].update_contents()
                content = await self.tracker_dict[tracker_key].get_contents()

                await reaction.remove(user)
                await self.send_msg_helper(ctx, tracker_key, content, msg, False)
