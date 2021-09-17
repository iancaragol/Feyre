.. _Privacy-Data:

##############
Privacy & Data
##############

.. _Privacy:

Privacy
=======

Feyre only reads the arguments of an existing command from :ref:`Commands`. Feyre *can not* read messages in your discord server that are not on that list. It will only see and process messages that start with the prefix for your server and the command. Furthermore, all data feyre stores is anonymous.

What can Feyre see?
-------------------

Feyre only sees messages that start with the server prefix and a command.

For example, this message will be seen and proccessed by Feyre::

    !roll Oh boy I hope I didnt put anything incriminating here

But, this message will not be seen by Feyre::

    roll Oh boy good thing Feyre cant see this message

Are the arguments to a command stored anywhere?
-----------------------------------------------

No, arguments are not stored or logged anywhere. In the above example Feyre would fail to understand the input to !roll and respond with an error message.

Any other questions or concerns?
--------------------------------

Hop in the `support server <https://discord.gg/zjyrtWZ>`_ and ask the developer!

.. _Data:

Data
====

What kind of data does Feyre store?
-----------------------------------

**User Id's**

These are a unique integer that represents a discord user. You can find a user's unique id by enabling developer options in the settings, right clicking on a user, and selecting copy id. These ids are used for setting a gm on a per channel basis. When a user uses any command, their user id is stored in a list of user ids. This list is used to keep track of the number of users that the bot has and in any command that is tied to a specific user (character, gm, bank, init).

**Channel Id's**

These are used by init and gm rolls to keep differentiate initatiave trackers and gms by channel. They are used stored in pairs (guild id: channel id, initative) and (guild id: channel id, gm's user id)

**Guild Ids**

Guild Ids are a unique integer that represents a guild. They are stored in pairs (id, prefix) by the !set_prefix command. They are also used by the GM roll and initative commands in conjunction with the channel id.

**Character Information**

Character names, bank accounts, and initatiave are stored along with a user's id. 

Where is this data stored?
--------------------------

Feyre runs on a VM on Microsoft's Azure. All data is stored in an SQL database also running on Azure.