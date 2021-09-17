import discord
import textwrap
import asyncio
from discord.ext import commands
from operator import attrgetter
from _cogs.DiceRolls import DiceRoll
from _cogs.CharacterSelection import CharacterSelectionHandler


class PlayerCharacter:
    def __init__(self, user_id, name, init_mod, init_value):
        self.user_id = user_id
        self.character_name = name[:32] + '...' if len(name) > 32 else name
        self.init_value = init_value


class InitiativeTracker:
    def __init__(self, character_selector): 
        self.add_order = []
        self.character_list = []
        self.init_messages = []
        self.dr = DiceRoll()
        self.content = ""
        self.header = "```asciidoc\n= Initiative ="
        self.footer = "```"
        self.round_count = 0
        self.marker_pos = 0
        self.verbose = False

        self.character_selector = character_selector

        self.content = self.header + f"\n[Round: {self.round_count}]\n\n[You will need to update Feyre's permissions to use all of the initiative tracker's features]\nUse !permissions to learn more.\n\nAdd characters to the tracker by pressing the + icon or using the !init command.\n\nEx: !init Gandalf -i 1d20+5```"

    async def add_player(self, user_id, name, init_mod):
        init_value = await self.dr.parse(init_mod, total_only=True) # Roll init_mod to get value
        new_pc = PlayerCharacter(user_id, name, init_mod, init_value)
        updated = False

        for i in range(len(self.add_order)):
            if self.add_order[i].character_name == new_pc.character_name:
                self.add_order[i] = new_pc
                updated = True

        if not updated:
            self.add_order.append(new_pc)
        self.character_list = list(self.add_order)

        self.character_list.sort(key = attrgetter('init_value'), reverse = True)

        if self.verbose:
            self.init_messages.append(f"{name} was added to initiative.")

        return True

    async def remove_player(self, user_id, name = None):
        if len(self.add_order) == 0:
            self.marker_pos = 0
            return

        if name: # If name is provided then remove specific character with that name
            #self.add_order = [i for i in self.add_order if i.character_name != name and i.user_id != user_id] # Remove that character

            del_index = None
            for i in range(len(self.add_order)):
                if self.add_order[i].character_name.strip() == name.strip() and self.add_order[i].user_id == user_id:
                    del_index = i
                    break
            
            if del_index != None:
                # print(f"Deleting {self.add_order[del_index].character_name}")
                del self.add_order[del_index]

                if del_index > 0: # Move the marker up one 
                    self.marker_pos = del_index - 1
                else:
                    self.marker_pos = 0


            self.character_list = list(self.add_order)
            self.character_list.sort(key = attrgetter('init_value'), reverse = True)

            if self.verbose:
                self.init_messages.append(f"{name} was removed from initiative.")

        else: # If name is not provided then delete the most recent character added by that player
            i = len(self.add_order) - 1
            while(i >= 0):
                if self.add_order[i].user_id == user_id:
                    del self.add_order[i]
                    if i > 0: # Move the marker up one 
                        self.marker_pos = i - 1
                    else:
                        self.marker_pos = 0
                    break
                i -= 1

            if self.verbose:
                self.init_messages.append(f"{self.add_order[i].character_name} was removed from initiative.")
            self.character_list = sorted(self.add_order, key=lambda x: x.init_value, reverse=True)

        await self.update_contents()

    async def update_player(self, user_id, name, init_mod):
        # print("Update Player")
        init_value = await self.dr.parse(init_mod, total_only=True)
        for c in self.character_list:
            if c.user_id == user_id and c.character_name == name:
                c.init_mod = init_mod
                c.init_value = init_value

    async def update_contents(self):
        # print("Update Contents")
        self.content = ""
        self.content += self.header
        self.content += f"\n[Round: {self.round_count}]"
        for i in range(len(self.character_list)):
            if i == self.marker_pos:
                self.content += f"\n`> {self.character_list[i].character_name} [{self.character_list[i].init_value}]'"
            else:
                self.content += f"\n {self.character_list[i].character_name} [{self.character_list[i].init_value}]"

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

    async def timeout_tracker(self):
        self.footer = "\nThis initiative tracker has timed out after 3 days of inactivity. You will need to create a new one using !init start.```"
    async def add_error_msg(self, error_msg):
        self.footer = "\n" + error_msg + "```"

    async def reset_footer(self):
        self.footer = "```"

    async def parse_args(self, user_id, args):
        name = ""
        init_mod = ""

        split_args = args.strip().lower().split()
        # Ex: !init Gandalf -i 1d20
        if '-i' in split_args:
            name = args[:args.index('-i')].strip()
            init_mod = args[args.index('-i') + 2:].strip()
            added = await self.add_player(user_id, name, init_mod)

            if added:
                return added


        elif '-r' in split_args:
            name = args[args.index('-r') + 2:].strip()

            if len(name) > 0:
                await self.remove_player(user_id, name=name) # If name exists then try and remove that name
            else:
                await self.remove_player(user_id) # Otherwise remove the last character added by that player
        else:
            split = args.strip().split(' ')
            name = ""
            init_mod = ""
            remove_substring = ""
            for s in split:
                if s == '-b' or s == '-a': # Special case. Parser will parse these because they are dice roll flags
                    break

                total = await self.dr.parse(s, total_only=True) # Try and parse either part of the message. If it parses correctly treat it as an init mod
                if total != "```I'm sorry, there was something I didnt understand about your input. See !help roll for more info```": # TODO Remove this when dice roller is rewritten.
                    # Dice parser will accept things like -, +, /, * as a valid init mod so we need to make sure its not one of these
                    try:
                        float(total)
                        init_mod = s
                        remove_substring = init_mod
                    except:
                        remove_substring = s
                        init_mod = ""
            
            for s in split:
                name += " " + str(s)

            name = name.replace(remove_substring, '').strip()
            
            if init_mod == "": # Default to 1d20
                init_mod = "1d20"
            

            if len(name) == 0: # If name is empty then we need to get it from their active character
                active_character = await self.character_selector.get_selected_character(user_id)
                added = await self.add_player(user_id, active_character.character_name, init_mod)
            else:
                added = await self.add_player(user_id, name, init_mod)

            if added:
                return added

    async def move_marker(self):
        # print("Move Marker")
        self.marker_pos += 1
        if self.marker_pos == len(self.character_list):
            self.round_count += 1
            self.marker_pos = 0
        elif len(self.character_list) == 0:
            self.marker_pos = 0
            
class InitiativeCog(commands.Cog):
    tracker_dict = {}
    msg_dict = {}
    plus = '🎲'
    skull = '☠️'
    swords = '⚔️'
    down_arrow = '⬇️'

    dm_error_msg = "```An initiative tracker cannot be started in DM's. Try creating one in a guild channel instead.```"
    start_msg = "```You need to start an initiative tracker in this channel before adding a character using [!init start]```"

    def __init__(self, bot, data):
        self.bot = bot
        self.character_selector = CharacterSelectionHandler()
        self.data = data

    @commands.command(aliases = ['Init', 'I', 'i'])
    async def init(self, ctx, *, args = None):
        self.data.userSet.add(ctx.author.id)
        self.data.statsDict['!init'] += 1

        if ctx.channel.type is discord.ChannelType.private: # If user has DM'd the bot
            await ctx.send(self.dm_error_msg)
            return

        tracker_key = str(ctx.guild.id) + ":" + str(ctx.channel.id)

        if not args and tracker_key not in self.tracker_dict.keys(): # No tracker in this channel
            await ctx.send(self.start_msg)
            return 

        if args:
            split_args = args.split(' ')
            if 'start' in split_args:
                # Create initative tracker
                tracker = InitiativeTracker(self.character_selector)

                if '-v' in args or '--verbose'  in args:
                    tracker.verbose = True

                self.tracker_dict[tracker_key] = tracker
                # Dont update contents here, otherwise the init start will be changed

                contents = await self.tracker_dict[tracker_key].get_contents()
                timeout = await self.send_msg_helper(ctx, tracker_key, contents, None, False)

                if timeout:
                    return
                

            elif 'bottom' in split_args or '-b' in split_args:
                # self.tracker_dict[tracker_key] = tracker
                # Dont update contents here, otherwise the init start will be changed

                if tracker_key not in self.tracker_dict.keys(): # No tracker in this channel
                    await ctx.send(self.start_msg)
                    return 

                contents = await self.tracker_dict[tracker_key].get_contents()
                timeout = await self.send_msg_helper(ctx, tracker_key, contents, None, True)
                if timeout:
                    return

            elif 'start' not in split_args and 'bottom' not in split_args and '-b' not in split_args:
                if tracker_key not in self.tracker_dict.keys():
                    await ctx.send(self.start_msg)

                added = await self.tracker_dict[tracker_key].parse_args(ctx.author.id, args)
                await self.tracker_dict[tracker_key].update_contents()

                if added:
                    self.data.statsDict['chars_added'] += 1
                    

                contents = await self.tracker_dict[tracker_key].get_contents()
                timeout = await self.send_msg_helper(ctx, tracker_key, contents, None, True)
                if timeout:
                    return

            
        else:
            # await ctx.send("`This doesnt do anything yet but it will add your active character`")
            new_character = await self.character_selector.get_selected_character(ctx.author.id)

            if new_character == None:
                await self.tracker_dict[tracker_key].add_error_msg("No character selected! Select a character using the !char command.")
                await self.tracker_dict[tracker_key].update_contents()
            else:
                await self.tracker_dict[tracker_key].add_player(ctx.author.id, new_character.character_name, new_character.init_mod)
                await self.tracker_dict[tracker_key].update_contents()
                self.data.statsDict['chars_added'] += 1

            contents = await self.tracker_dict[tracker_key].get_contents()
            timeout = await self.send_msg_helper(ctx, tracker_key, contents, None, True)
            if timeout:
                return

    async def add_reactions_helper(self, msg):     
        await msg.add_reaction(self.swords)
        await msg.add_reaction(self.plus)
        await msg.add_reaction(self.skull)
        await msg.add_reaction(self.down_arrow)

    async def remove_reactions_helper(self, msg):
        await msg.clear_reaction(self.skull)
        await msg.clear_reaction(self.plus)
        await msg.clear_reaction(self.swords)
        await msg.clear_reaction(self.down_arrow)

    async def send_msg_helper(self, ctx, tracker_key, contents, msg, repost):
        if not msg and not repost: # If this was called through a command and not through a reaction
            msg = await ctx.send(contents)
            self.msg_dict[tracker_key] = msg
            await self.add_reactions_helper(msg)

        elif msg and not repost:
            await msg.edit(content=contents)
            msg = await ctx.channel.fetch_message(msg.id)
            self.msg_dict[tracker_key] = msg

        elif not msg and repost:
            await self.msg_dict[tracker_key].delete()
            msg = await ctx.send(contents)
            self.msg_dict[tracker_key] = msg
            await self.add_reactions_helper(msg)

        await self.tracker_dict[tracker_key].reset_footer()
           
        try:           
            reaction = None
            user = None
            reactions = [r for r in msg.reactions if r.count > 1]

            if len(reactions) > 0:
                reaction = reactions.pop(0)
                user = None
                async for u in reaction.users():
                    if u.id != self.bot.user.id:
                        user = u
            else:
                reaction, user = await self.bot.wait_for('reaction_add', check=lambda r, u:u.id != self.bot.user.id and r.message.id == msg.id, timeout=259200) # Times out after 3 days

            if reaction != None and user != None:
                if str(reaction.emoji) == self.plus:

                    # Get users active character, add it to tracker, then update tracker contents for display
                    new_character = await self.character_selector.get_selected_character(user.id)

                    if new_character == None:
                        await self.tracker_dict[tracker_key].add_error_msg("No character selected! Select a character using the !char command.")
                        await self.tracker_dict[tracker_key].update_contents()

                    else:
                        await self.tracker_dict[tracker_key].add_player(user.id, new_character.character_name, new_character.init_mod)
                        await self.tracker_dict[tracker_key].update_contents()
                        self.data.statsDict['chars_added'] += 1

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

                elif str(reaction.emoji) == self.down_arrow:
                    content = await self.tracker_dict[tracker_key].get_contents()
                    # await msg.delete()
                    await self.send_msg_helper(ctx, tracker_key, content, None, True)

            
        except Exception as e:
            print(e)
            if type(e) is asyncio.TimeoutError:
                print("Time out")
                await self.tracker_dict[tracker_key].timeout_tracker()
                await self.tracker_dict[tracker_key].update_contents()
                content = await self.tracker_dict[tracker_key].get_contents()
                await self.msg_dict[tracker_key].edit(content=content)
                await self.remove_reactions_helper(msg)
                del self.tracker_dict[tracker_key]
                del self.msg_dict[tracker_key]
                return True# Now that this has timed out there is no need to wait on it

            elif type(e) is discord.errors.Forbidden:
                print("Missing permissions")
                await self.tracker_dict[tracker_key].add_error_msg("Feyre now requires the Manage Messages permission to use emojis as buttons. See !permissions for details on how to do this. You can still use the commands such as !init Gandalf to use the initiative tracker but button functionality is limited. Once you have added the required permissions restart the initiative tracker with !init start.")
                await self.tracker_dict[tracker_key].update_contents()
                content = await self.tracker_dict[tracker_key].get_contents()
                await self.msg_dict[tracker_key].edit(content=content)
                await self.remove_reactions_helper(msg)
                return True