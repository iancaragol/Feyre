
# Feyre
##### A Discord bot for D&amp;D and other RPG games

This bot was created to help facilitate RPG games such as D&D and Pathfinder. 
It is written in python and uses the discord.py module. 

All spells, feats, and monsters are taken from the D&D Standard Reference Document or scraped
from the free sections of D&D beyond.

## Features
#### -> Dice Rolling:
This bot has a robust dice rolling functionality that can handle multiple dice, modifiers, ability checks, and rolling with advantage/disadvantage.
##### Rolling with dice expressions
!roll can be used to roll dice of any size with complicated expressions and built in skill checks. Dice are represented with the standard [# of dice]d[size of dice] format. You can also use !r. 

    Ex: !roll 1d20 + 1d6 - 6 < 15
      Output: I interpreted your input as 1d20+1d6-6<15.
		      Rolls: [7]+[4]-6<15 
		      - Ability/Skill Check: Succeeded -
		      
    Ex: !r 1d20/1d50*(1d12/1d6)
      Output: I interpreted your input as 1d20/1d50*(1d12/1d6). 
		      Rolls: [13]/[29]*([8]/[3]) 
		      - Total: 1.2 -

Skill checks can be built into the dice expression using the < and > symbols. 

	Ex: !roll 1d20 > 15 
	  Output: I interpreted your input as 1d20>15. 
			  Rolls: [8]>15 
			  - Ability/Skill Check: Failed -

You can roll with advantage or disadvantage using the -a and -d flags before the dice expression. 

![enter image description here](https://i.imgur.com/J4YAhSI.png)

	Ex: !roll -a 1d20 
		!roll -d 1d20+5
##### Simple dice rolling

If you are only rolling one dice you can use !d [modifier] to roll. The following dice are supported.

	!d4
	!d6
	!d8
	!d10
	!d12
	!d20
	!dp
	
![Simple Dice Rolling](https://i.imgur.com/c9X9PeZ.png)

##### Gamemaster dice rolling
!gm can be used to send dice rolls to the GM without other players being able to see the result. This is useful if a player is trying to do something sneaky, like steal from another player. GM's are set on a per channel basis. 

Commands (can be shortened to !i): 

	!gm > Sets the gamemaster for that channel
	!gm roll [dice expression] > Rolls the dice so that only the player and gamemaster can see the result

![Set GM](https://i.imgur.com/bBzip8b.png)

![GM Roll](https://i.imgur.com/cnvKtHY.png)
#### -> Initiative Tracking:

!init is a per channel based initiative tracker. Click the Crossed Swords icon to move to the change turns! If you need to insert a player into the middle of initiative use decimals. 

Commands (can be shortened to !i): 

	!init start > Starts a new initiative tracker in the same channel 
	
	!init > Adds the player to initiative with their discord username and rolls 1d20 for them 
	
	!init [player name] > Adds a player with [player name] to initiative and rolls 1d20 for them 
	
	!init [player name] [initiative] > Adds a player with [player name] and [initiative] to iniative.
	 
	!init remove [player name] or !init -r [player name] > Removes a player from initiative.
	 
	!init [name] [modifier] or [modifier] [name] > Adds a player to initiative after rolling 1d20 and applying the modifier. 

![Example initiative tracker](https://i.imgur.com/1D4oz9U.png)

#### -> Feat lookup
##### !feat (name)
!feat can be used to lookup feats from the Player's Handbook. 

Commands: 

	!feat [feat name] > Searches for a feat 
	!randfeat > Gives a random feat Ex: !feat Keen Mind

![Feat lookup example](https://i.imgur.com/yIIBBDN.png)

#### -> Monster Manual
##### !mm (name)
!mm can be used to lookup monsters from the Monster Manual. 

Commands: 

	!mm [monster name] > Searches for a monster 
	!randmonster > Gives a random monster 
						
![Monster lookup example](https://i.imgur.com/Bqj6qgy.png)
						
#### -> Spellbook
##### !spell (name)
!spell can be used to lookup spells from the Player's Handbook. 

Command:

	!spell [spell name] 
![Spell lookup example](https://i.imgur.com/oEeuTIY.png)
		
#### -> Weapons
##### !weapon (name)
!weapon is used to lookup simple adventuring weapons, such as a longsword.

Commands:

	!weapon [name] > Search for a weapon
	!w [name] > Search for a weapon

![Weapon lookup example](https://i.imgur.com/3JOHfOw.png)



#### -> Items
##### !item (name)
!item is used to lookup any wondrous items.

Command:

	!item [name] > Search for an item

![Item lookup example](https://i.imgur.com/0xsY43L.png)

#### -> Classes
##### !c (name)
!c is used to lookup class features. The descriptions can be quite long so it is recommended that you DM the bot when using this command.

Command:

	!c [name] > Lookup class features

![Class lookup example](https://i.imgur.com/XJZTP5a.png)

#### -> Deck of Many Things
##### !c (name)
!dom can be used to draw a card from the deck of many things. The -i flag will include an image!

Command:

	!dom > Draws one card from the Deck of Many Things 
	!dom -i > Draws one card form the Deck of Many Things and includes an image of the card

![Drawing a card from the Deck of Many Things](https://i.imgur.com/q28Ecv3.png)

#### -> Help
##### !help
!help gives information on all of the various commands

Command:

	!help > Shows all commands
	!help [command] > Shows how to use a specific command

![Help](https://i.imgur.com/jQ2MmCe.pngg)

![Help Init](https://i.imgur.com/eLvIEa0.png)

#### -> Stats
##### !stats
!stats shows command usage statistics.

Command:

	!stats > Show the most used commands
	!stats all > Shows stats for all commands
	
![!stats](https://i.imgur.com/piCdGOn.png)

#### -> New
##### !new
!new shows updates and bug fixes

Command:

	!new > Show most recent updates and bug fixes
![!new](https://i.imgur.com/krC2ebT.png)

#### -> Admin
##### !admin
!admin shows all commands available to server administrators.

![Admin command](https://i.imgur.com/C29GpYN.png)
##### !set_prefix
!set_prefix is used by guild administrators to change the default prefix (!) used to call Feyre. This is particularly useful when two bots have the same set of commands such as !help. Once a prefix is changed a message will be pinned in the channel in case you forget.

Command:

	!set_prefix [/,!,~,`,#,$,%,^,&,*,,,.,;,:,<, or >] > Sets the default prefix
![set_prefix command](https://i.imgur.com/2gdJckk.png)

## Privacy and Data
#### What kind of data does Feyre store?
Feyre only stores command usage statistics, guild, channel, and player ids.

Guild Ids: 
Guild Ids are a unique integer that represents a guild. They are stored in pairs (id, prefix) by the !set_prefix command. They are also used by the GM roll and initative commands in conjunction with the channel id.
	
Channel Ids: 
These are used by init and gm rolls to keep differentiate initatiave trackers and gms by channel. They are used stored in pairs (guild id: channel id, initative) and (guild id: channel id, gm's user id)
	
User Ids: 
These are a unique integer that represents a discord user. You can find a user's unique id by enabling developer options in the settings, right clicking on a user, and selecting copy id. 
These ids are used for setting a gm on a per channel basis. When a user uses any command, their user id is stored in a list of user ids. This list is used to keep track of the number of users that the bot has.
	
