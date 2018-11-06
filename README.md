# FeyreBot
##### A Discord bot for D&amp;D and other RPG games

This bot was created to help facilitate RPG games such as D&D and Pathfinder. 
It is written in python and uses the discord.py module. 

All spells, feats, and monsters are taken from the D&D Standard Reference Document.

## Features
#### > Dice Rolling:
##### !roll (dice) (modifier) (skill check)
	This bot has a robust dice rolling functionality that can handle multiple dice, modifiers, and ability checks.
	
    Ex: !roll 1d20 + 1d6 - 6 < 15
      Output: I interperted your input as 1d20+1d6-6<15.
              Rolls: [8]+[4]-6<15
              Ability/Skill Check: Succeeded
    Ex: !roll 1d20 + 5 * 2
      Output: I interperted your input as 1d20+5*2
              Rolls: [20]+5*2
              Total: 30
#### > Initiative Tracking:
##### !start init
##### !add init (player) (initiative)
	The iniative tracker tracks iniative on a per-channel basis. Any player can add themselves to the initiative 
	order or they can be added by the GM. 
	If (player) is left blank the characters name will be the discord users name. 
	If (initiative) is left blank a standard 1d20 will be rolled for that character.
	
	Ex: !start init
	    !add init Gandalf 12
      > Adds a player named Gandalf to the tracker with an iniative of 12
	    !add init Frodo
		  > Adds a player named Frodo to the tracker and rolls 1d20 for their initiative.
	    !add init
      > Adds a player with the users discord name and rolls 1d20 for their initiative.
#### > Feat lookup
##### !feat (name)
	Searches the Players Handbook for a feat.
	
	Ex: !feat Keen Mind
		Output: Keen Mind
            (PH)

            You have a mind that can track time, direction, and detail with uncanny precision. 
						You gain the following benefits:
            - Increase your Intelligence score by 1, to a maximum of 20.
            - You always know which way is north.
            - You always know the number of hours left before the next sunrise or sunset.
            - You can accurately recall anything you have seen or heard within the past month.

#### > Monster Manual
##### !mm (name)
	Searches the monster manual for a monster.
	
	Ex: !mm guard
		Output: Guard
            Armor Class 16 (chain shirt, shield)
            Hit Points 11 (2d8+2)
            Speed 30 ft.

            | STR | DEX | CON | INT | WIS | CHA |
            |:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
            | 13 (+1) | 12 (+1) | 12 (+1) | 10 (0) | 11 (0) | 10 (0) |
						
            Skills Perception +2
            Languages any one language (usually Common)

            Challenge 1/8 (25 XP)

            Actions
            Spear. Melee or Ranged Weapon Attack: +3 to hit, reach 5 ft. or range 20/60 ft., one target. 
            Hit: 4 (1d6 + 1) piercing damage or 5 (1d8 + 1) piercing damage if used with two hands to make a melee attack.
						
#### > Spellbook
##### !spell (name)
	Searches the Players Handbook and Standard Reference Document for a spell.
	
	Ex: !spell message
		Output: Message
            Level: Cantrip
            Casting Time: 1 Action
            Range: 120ft
            Components: V, S, M *
            Duration: 1 Round
            School: Transmutation
            Attack/Save: None

            You point your finger toward a creature within range and whisper a message. The target (and only the target) hears the message and can reply in a whisper that only you can hear.
            You can cast this spell through solid objects if you are familiar with the target and know it is beyond the barrier. Magical silence, 1 foot of stone, 1 inch of common metal, a thin sheet of lead, or 3 feet of wood blocks the spell.
            The spell doesn't have to follow a straight line and can travel freely around corners or through openings.
            * - (a short piece of copper wire)
		
#### All Commands:
	> !help: Displays all commands.
	> !hello: Hi!
	> !start init: Starts initiative tracker in channel
	> !add init (name) (roll): Adds player to initiative tracker. If left blank uses discord username and rolls 1d20.
				Ex: !add init Feyre 20
	> !roll (dice) (modifiers) (check): Rolls any number and types and dice. Supports complicated expressions and ability checks
				Ex: !roll 1d20 + (5 - 1)/2 + 1d6 < 25
	> !stats: Displays number of times each command has been used in the lifetime of the bot

	D&D 5E Specific Commands:
	> !feat (name): Search D&D 5E offical books for a feat (currently only PH). 
			 Ex: !feat Keen Mind
	> !mm (name): Search the D&D 5E Monster Manual for a monster. 
			 Ex: !mm Goblin
	> !spell (name): Search D&D 5E SRD for a spell. 
			 Ex: !spell fireball
	> !randfeat: Gives a random feat from offical 5E books.
	> !randmonster: Gives a random monster from the D&D 5e Monster Manual.

	Book of Tor Specific Commands:
	> !tor horo: Gives a Torian Horoscope.
	> !tor randchar: Gives a random race and class combination from the Book of Tor.
	> !tor styles: Lists all character styles from the Book of Tor.
	> !tor zodiac: Gives a Primidia's Zodiac animal from the Book of Tor.
	
#### Features in the works:
	- Moving all data from .txt files to a database
	- Max and Min roll commands
	- Better search functionality
	- Inline skill checks
