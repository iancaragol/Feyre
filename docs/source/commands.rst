.. _Commands:

########
Commands
########

Feyre has a rich set of commands to help you play role-playing games in discord.

.. _Help:

Help
====

``!help``

!help lists all of Feyre's commands and any important updates or information. Instead of referring to this page you can always use the !help command.

**Learn More About a Command**

``!help [command]``

If you need more information on how a command works you can use !help like this::

    !help init

.. _Dice-Rolling:

Dice Rolls
==========

``!roll [dice expression]`` *or* ``!r [dice expression]``

!roll can be used to roll dice of any size with complicated expressions and built in skill checks.

Dice are represented with the standard [# of dice]d[size of dice] format. You can also use !r::

    !roll 4d6
    !roll 1d6*2
    !r 1d20 + 5
    !r 1d1000 + 2d2000 * 3 / 3 - 1

**Skill Checks**

Skill checks can be built into the dice expression using the < and > symbols::

    !roll 1d20 > 15

**Advantage & Disadvantage**

You can roll with advantage or disadvantage using the -a and -d flags before the dice expression::

    !roll -a 1d20
    !roll -d 1d20+5

Finally, you can reroll any dice roll by clicing the reroll emoji.

**Rolling a single die**

``!d[size] [expression]``

!d[size] [expression] can be used if you only want to roll one dice. If you only need to roll one dice this command is quicker than typing !roll.

This command supports standard dice sizes [4,6,8,10,12,20] and expressions. A space is neccessary between the dice and any modifiers.

You can also use !dp to roll for percentile::

    !d20
    !d6 +2
    !dp

.. _GM-Rolling:

Secret Dice Rolls
=================

``!gm``
``!gm roll [expression]``

!gm can be used to send dice rolls to the GM without other players being able to see the result. This is helpful in cases where a player needs to make a roll without the rest of the parties knowing.
GM's are set on a per channel basis.

**Setting the GM**

``!gm``

!gm sets the channels GM to the user. Any further rolls using the !gm command will be DM'd to the roller and the GM.

``!gm roll [dice expression]``

If the channel has a GM then this will roll [dice expression] and direct message the result to the user and the GM for that channel.

Example::

    !gm
    !gm roll 1d20-5




.. _Initiative-Tracker:

Initiative Tracker
==================

``!init`` *or* ``!i``


!init is a streamlined, per channel based initative tracker.

**Buttons**

To make using the tracker easier users can use these buttons instead of typing

* Crossed Swords: Moves the turn icon (>).
* Plus Sign: Add's the user's active character to initiative, see :ref:`Character`.
* Skull and Crossbones: Removes the user's most recently added character from initative. 
* Down Arrow: Brings the initiative tracker to the bottom of the channel

**Starting Initiative**

``!init start``

Starts an initaive tracker in the same channel, also used to reset an existing initiative tracker.

``!init start -v``

Starts an initiative tracker with verbosity.

**Adding a Character to Initiative**

``!init``

Adds the user's active character to initiative. You can also press the Plus Sign instead.

``!init [character name]``

Adds a character with [character name] to initiative and rolls 1d20 for them.

``!init [character name] [initiative]``

Adds a character with [character name] to initiative with an initiative of [initiative]. Including a decimal can be used to easily insert a character anywhere in the turn order.

If a character with [character name] already exists, their initiative value will be updated instead.

``!init [character name] -i [dice expression]``

Adds a character with [character name] to initiative and rolls [dice expression] for them.

If a character with [character name] already exists, their initiative value will be updated instead.

**Removing a Character from Initiative**

``!init -r``

Removes the most recent character added by the user from initiative. You can press the Skull and Crossbones isntead.

``!init -r [character name]``

Removes [character name] from initiative.

**Moving the Initiative Tracker to the Bottom of the Channel**

``!init bottom`` *or* ``!init -b``

Moves the initiative tracker to the bottom of the channel in case it gets lost in users' messages.

**Example**

The GM starts initiative::

    !init start

Player A adds their active character to initiative::

    !init

Player B adds a character to initiative and rolls 1d20+5::

    !init Frodo -i 1d20+5

Player C rolls a physical set of dice and adds their character to initiative manually::

    !init Legolas 17

Player B removes Frodo from initiative::

    !init -r Frodo

At the end of combat, the GM resets the tracker::

    !init start

.. _Character:

Character Management
====================

``!character`` *or* ``!char``

!character is used to set your active character which is used by the initiative tracker. You can create up to 9 characters and set a character as active using emojis or the command argument [id]. Characters follow you across servers and are persistent.


This command can also be shortened to !char

**Select Your Active Character**

``!character``

Shows your character list and lets you select your active character using the emoji buttons.

``character [ID]``

Sets your active character to the character with an id of [ID].

**Create a New Character**

``!character -a [character name] -i [initiative dice expression]``

Adds a character with [character name] to your character list. [initiative dice expression] will be rolled whenever this charater is added to initiative.

The ``-i [initiative dice expression]`` tag is optional. If it is not inlucded that character's default to rolling 1d20.

**Removing a Character**

``!character -r [ID]``

Removes the character with [ID] from your character list. You can find your character's IDs using ``!character``.

**Example**

Player A's last character died a tragic death so they create a new one::

    !character -a Galloway the Snail -i 1d2-1

Player A removes their dead character from their character list::

    !character -r 1

Player B creates a generic character with a default initiative of 1d20::

    !character -a Generic Character No1 

Player B doesn't like their character so they set their active character to someone else::

    !character 7

.. _DOM:

Deck of Many Things
===================

``!dom``

!dom can be used to draw a card from the deck of many things. The -i flag will include an image!

Draw one card from the Deck of Many Things::

    !dom

Draw one card from the Deck of Many Things and include an image of the card::

    !dom -i


.. _Currency:

Currency Conversion
===================

``!currency`` *or* ``!convert`` *or* ``!cur``

!currency can be used to convert any denomination of platinum, gold, electrum, silver, and copper to gold, silver and copper.
It can also be used to evenly divide an amount of currency between any number of players by including a /x at the end where x is the number of players.

* pp = Platinum
* gp = Gold
* ep = Electrum
* sp = Silver
* cp = Copper

When providing the amounts there is no need to worry about capitlization or spacing.

**Convert Currency to GP, SP, CP**

``!currency [amount][abbreviation]``

For example, convert 177 ep, 112 sp, 43 cp to gp, sp, cp::

    !currency 117ep112sp43cp

**Divide Currency Amongst Players**

``!currency [amount][abbreviation] / [number of players]``

For example, divide 111 gp, 37 sp, 4 cp amongst 4 players::

    !currency 111gp37sp4cp/4


.. _Bank:

Bank
====

``!bank``

You can use Feyre to manage all of your character's wallets. Your bank is tied to your Discord ID and can be accessed from any server/channel or by direct messaging Feyre.

Interacting with your bank requires the use of argument flags (-a, -r, -d, -w). If you have any suggestions on how this experience can be streamlined please use the !request command and let me know!

[currency values] have the same format as the :ref:`Currency` command. For example you can represent 10 platinum, 9 gold, 8 electrum, 7 silver, and 6 copper like this: 10pp9gp8ep7sp6cp

*This feature will eventually be combined with* :ref:`Character`.

**See Your Characters**

``!bank``

Shows all of your characters and their unique IDs. The character's id (a unique number representing that character) can be used instead of [character name].

**Add a Character**

``!bank -a [character name]``

Adds a new character to your bank with [character name]. This character will also be assigned a unique ID which can be used to access its account.

**Remove a Character**

``!bank -r [character name]`` *or* ``!bank -r [character id]``

Deletes the account associated with [character name] or [character id]

**Make a Deposit**

``!bank -d [character name] [currency values]``

Deposits the specified [currency values] into the account associated with [character name] or [character id]

**Make a Withdrawal**

``!bank -w [character name] [currency values]``

Withdraws the specified [currency values] into the account associated with [character name] or [character id]

**Example**

Add a character with the name Bilbo to your bank::

    !bank -a Bilbo

Deposit (-d) 10 silver and 5 copper into Bilbo's account::

    !bank -d Bilbo 10sp5cp

See all of your characters and their unique IDs::

    !bank

Withdraw 3 copper from Bilbo's account. In this example Bilbo has been assigned the unique ID 1 because he is the first character associated with the example user::

    !bank -w 1 3cp

Delete Bilbo's bank account::

    !bank -r Bilbo





.. _Feat-Lookup:

Feat Lookup
===========

``!feat [feat name]``

!feat can be used to lookup feats from the Player's Handbook::

    !feat Keen Mind

``!randfeat``

Gives a random feat

.. _Condition-Lookup:

Condition Lookup
================

``!condition``

!condition lists all of the conditions from the Player's Handbook::

    !condition 

``!condition [condition name]``

!condition [condition name] gives more information on the specified condition::

    !condition prone

.. _Weapon-Lookup:

Weapon Lookup
=============

``!weapon [weapon name]`` *or* ``!w [weapon name]``

!weapon is used to look up the stats on a weapon::

    !w Longsword

.. _Item-Lookup:

Item Lookup
===========

``!item [item name]``

!item is used to lookup items from the Dungeon Master's Guide::

    !item Portable Hole


.. _Monster-Lookup:

Monster Lookup
==============

``!mm [monster name]``

!mm is used to lookup monsters from the Monster Manual::

    !mm Young Black Dragon

``!randmonster``

Gives a random monster.

.. _Spell-Lookup:

Spell Lookup
============

``!spell [spell name]``

!spell is used to lookup spells from the Player's Handbook::

    !spell Firebolt

.. _Class-Lookup:

Class Lookup
============

``!c [class name]``

!c is used to look up all of the features of a class. This can be a lot of text::

    !c wizard

Why is the command !c and not !class? Thats because class is a python keyword.

.. _Ability-Lookup:

Ability Lookup
==============

``!ability [ability name]``

!ability can be used to lookup class abilities such as Barbarian's Danger Sense. All abilities from the PHB are supported. If you think an ability is missing or incorrect please report it with the !request command.

Some classes have abilities with the same names. To specify which class you are interested in include the name of the class.

Example::

    !ability Danger Sense
    !ability spellcasting wizard

.. _Stats:

Usage Statistics
================

`!stats`

Shows command usage statistics the most popular commands. Feyre keeps track of the number of times each command has been used and the total user count.

`!stats all`

Shows command usage statistics for all commands.

.. _Request:

Request New Features & Bug Reports
==================================

``!request [feature or bug]``

Please help improve the bot by request features you would find useful! This is also used to report bugs

For example, a user recently requested ability lookup because they found it cumbersome to use the !c command::

    !request Ability lookup for class abilities

.. _New

New
===

``!new``

!new shows any new features, bug fixes, etc...

.. _Set-Prefix

Set Feyre's Prefix
==================

``!admin``

!admin is for server administrators. Currently the only command available to adminstrators is !set_prefix.

**Set Prefix**

``!set_prefix [prefix]``

Sets the server wide prefix to [prefix]. Prefix must be ?, !, ~, `, #, $, %, ^, &, *, ,, ., ;, :, <, or >::

    !set_prefix ?

*NOTE: If you forget the prefix you will no longer be able to summon Feyre! (For now)*

.. _Vote

Vote for Feyre
==============

``!vote``

top.gg ranks discord bots based on the number of votes that they have. Please vote for Feyre using !vote. Thanks!