@bot.event
async def on_raw_reaction_add(payload):
    cross = '\N{CROSSED SWORDS}'
    if(str(payload.emoji) == cross):
        init_key = str(payload.guild_id) + ":" + str(payload.channel_id)
        if(init_key in data.initDict.keys()):
            channel = bot.get_channel(payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)

            init = data.initDict[init_key]

            reaction = get(msg.reactions, emoji=payload.emoji.name)
            if reaction and reaction.count > 1:
                #init.round_count += 1
                init.marker_count += 1
                await update_init(init_key)
    

async def update_init(key):
    desc = data.initDict[key].displayInit()
    codeBlock = '''```asciidoc
= Initiative =
[Round: {}]'''.format(data.initDict[key].round_count) + desc + '```'

    #delete old message and send new one with updated values
    old_msg = data.initEmbedDict[key]
    data.initEmbedDict[key] = await  data.initEmbedDict[key].delete()
    data.initEmbedDict[key] = await  old_msg.channel.send(codeBlock)

    cross = '\N{CROSSED SWORDS}'
    plus = '➕'
    await data.initEmbedDict[key].add_reaction(cross)
    await data.initEmbedDict[key].add_reaction(plus)

    print("Updated init")
    print("Key" + str(key))
    print("Old msg id: " + str(old_msg.id))
    print("Init Dict Key: " + str(data.initEmbedDict[key].id))
    reaction, u = await bot.wait_for('reaction_add', check=lambda r, u:str(r.emoji) == '➕' and u.id != bot.user.id and r.message.id == data.initEmbedDict[key].id, timeout=21600)
    print(reaction.message.id)

    if reaction != None:
        print("User clicked plus sign")
        selected_character = await data.character_selection_handler.get_selected_character(u.id)
        print(selected_character.character_name)
        print(selected_character.init_mod)
        rolled_init = await data.diceRoller.parse(selected_character.init_mod, total_only=True)
        data.initDict[key].addPlayer(selected_character.character_name, rolled_init)
        await update_init(key)

async def init_helper(ctx, args):
    """
    Starts or adds players to initiative
    """
    if (ctx.author.id not in data.userSet):
        data.userSet.add(ctx.author.id)
    data.statsDict['!init'] += 1

    if (not ctx.guild):
        await ctx.send("""```The initative tracker can only be used in a guild channel at this time. It is not supported when direct messaging Feyre. See !help init for more info.```""")
        return 

    #This command will be moved into its own class
    if (args == 'start'):
        key = str(ctx.guild.id) + ":" + str(ctx.channel.id)
        i = Initiative()
        data.initDict[key] = i
        codeBlock = '''```asciidoc
= Initiative = 
[Round: {}]```'''.format(i.round_count)
        msg = await ctx.send(codeBlock)
        plus = '➕'
        cross = '\N{CROSSED SWORDS}'

        await msg.add_reaction(cross)
        await msg.add_reaction(plus)

        data.initEmbedDict[key] = msg
        await update_init(key)

    elif (args.strip().startswith('reset')):
        argsStr = str(args)
        key = str(ctx.guild.id) + ":" + str(ctx.channel.id)

        if(key in data.initDict):
            name = argsStr.strip()
            mark = data.initDict[key].changeMarker(0)
            ret = data.initDict[key].changeRound(0)

            if(ret):
                await update_init(key)

    elif (args.strip().startswith('round')):
        argsStr = str(args)
        argsStr = argsStr.replace('round', '').strip()
        key = str(ctx.guild.id) + ":" + str(ctx.channel.id)

        if(key in data.initDict):
            name = argsStr.strip()
            try:
                ret = data.initDict[key].changeRound(int(argsStr))
            except:
                 await ctx.send('''```Something went wrong! Make sure the new round is a number. See !help init for more info.```''')
            if(ret):
                await update_init(key)


    elif (args.strip().startswith('remove') or args.strip().startswith('-r')):
        argsStr = str(args)
        argsStr = argsStr.replace('remove', '').strip()
        argsStr = argsStr.replace('-r', '').strip()

        key = str(ctx.guild.id) + ":" + str(ctx.channel.id)

        if(key in data.initDict):
            name = argsStr.strip()
            ret = data.initDict[key].removePlayer(name)

            if(ret):
                await update_init(key)

            elif(not ret):
                await ctx.send('''```I couldnt find the player you were looking for.```''')

             
    else:
        argsStr = str(args)

        data.statsDict['!init'] += 1
        key = str(ctx.guild.id) + ":" + str(ctx.channel.id)

       
        if(key in data.initDict):
            split = argsStr.split(' ')
            name = ""
            init = ""
        #mod = ""        
            if len(split) == 2:
                try:
                    #name mod
                    name = split[0]
                    if split[1].startswith("+") or split[1].startswith("-") or split[1].startswith("/") or split[1].startswith("*"):
                        roll = random.randint(1, 20)
                        init = data.diceRoller.parse(str(roll)+split[1], total_only=True)#aeval(str(roll) + split[1])

                    #name roll
                    elif split[1][0].isdigit():
                        init = float(split[1])

                    else:
                        #mod name
                        name = split[1]
                        if split[0].startswith("+") or split[0].startswith("-") or split[0].startswith("/") or split[0].startswith("*"):
                            roll = random.randint(1, 20)
                            init = aeval(str(roll) + split[0])

                        #roll name
                        elif split[0][0].isdigit():
                            init = float(split[0])

                except Exception as e:
                    print(e)
                    await ctx.send('''```There was something I didnt understand about your input.
Ex: !init [name] [value OR modifier]

Currently I don't support inline dice rolls such as !init Gandalf +1d6```''')

            elif len(split) == 1 and split[0] != '':

                try:
                    if split[0][0].isdigit():
                        name = ctx.author.name
                        init = float(split[0])

                    elif split[0].startswith("+") or split[0].startswith("-") or split[0].startswith("/") or split[0].startswith("*"):
                        name = ctx.author.name
                        roll = random.randint(1, 20)
                        init = aeval(float(roll) + split[0])

                    else:
                        name = split[0]
                        init = random.randint(1, 20)

                except Exception as e:
                    print(e)
                    await ctx.send('''```There was something I didnt understand about your input.
Ex: !init [name] [value OR modifier]

Currently I don't support inline dice rolls such as !init Gandalf +1d6```''')
                    return
          
            elif len(split) == 1 and split[0] == '':
                name = ctx.author.name
                roll = random.randint(1, 20)
                init = float(roll)

            else:
                await ctx.send('''```There was something I didnt understand about your input.
Ex: !init [name] [value OR modifier]
Currently I don't support inline dice rolls such as !init Gandalf +1d6```''')

            try:
                init = float(init)
                name = str(name)

                data.initDict[key].addPlayer(name, init)
                await update_init(key)

            except Exception as e:
                print(e)
                await ctx.send('''```There was something I didnt understand about your input.
Ex: !init [name] [value OR modifier]

Currently I don't support inline dice rolls such as !init Gandalf +1d6```''')
                return

        else:
            await ctx.send('''```Please start initiative with !init start before adding players```''')


@bot.command()
async def init(ctx, *, args = ""):
    await init_helper(ctx, args)

@bot.command()
async def i(ctx, *, args = ""):
    await init_helper(ctx, args)