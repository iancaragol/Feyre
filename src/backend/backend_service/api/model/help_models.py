import textwrap

class HelpModels:
    """
    Defines all help messages.
    """

    roll = textwrap.dedent("""
    ```asciidoc
    /roll can be used to roll dice of any size with complicated expressions and built in skill checks

    Dice are represented with the standard [# of dice]d[size of dice] format.

    Ex: !roll 4d6
    !roll 1d6*2
    !r 1d20 + 5
    !r 1d1000 + 2d2000 * 3 / 3 - 1

    Skill checks can be built into the dice expression using the < and > symbols.
    Ex: !roll 1d20 > 15

    You can roll with advantage or disadvantage using the -a and -d flags before the dice expression.
    Ex: !roll -a 1d20
        !roll -d 1d20+5
    ```
    """)

    default = textwrap.dedent("""
    ```asciidoc
    Hello! My name is Feyre. You can use chat or DM's to summon me. 
    ===============================================================

    [Read the Documentation]
    feyre.readthedocs.io

    [Join the Support Server]
    /support [NOT IMPLEMENTED]

    To learn more about a command type /help [command].
    Like this: /help roll

    [Commands]
    > hello - Hi! [NOT IMPLEMENTED]
   
    > roll - Dice rolling with complicated expressions
    > stats - Command usage statistics
    > health - Backend service health

    Like Feyre?
    ===========
    Use /invite to add Feyre to your server!
    Also consider voting for Feyre on top.gg using the `/vote' command :)
    ```
    """)

