import textwrap

class HelpModels:
    """
    Defines all help messages.
    """

    roll = textwrap.dedent("""
    ```asciidoc
    /roll can be used to roll dice of any size with complicated expressions.

    Dice are represented with the standard [# of dice]d[size of dice] format.

    Ex:
    /roll expression:4d6
    /roll expression:(1d6+2)*2
    
    [Skill Checks]
    [<, >, >=, <=, =]
    Skill checks can be built into the dice expression using the < and > symbols.

        1d20 > 15

    [Conditional Operators]
    [t]
    You can add a condition using the letter 't'. Think of the letter 't' as 'then', if the condition on the left side is True, then the expression on the right side will be evaulated.

        1d20 > 15 t 2d6+3 -> If 1d20 is greater than 15 THEN roll 2d6+3

    [Count Operator]
    [c#]
    You can repeat a dice roll using the count operator, 'c' followed by a number. This needs to be put at the END of an expression, it will roll the expression independently count # of times.

        2d6+3c3 -> Roll 2d6+3 3 times

    [Keep Operator]
    [k#]
    When rolling multiple dice, you can use the keep operator, 'k' follwed by a number, to keep the highest number of dice.

        5d20k3 -> Roll 5d20 keep the highest 3

    [Drop Operator]
    []
    Not implemented yet, will be the inverse of keep

    [Advantage / Disadvantage]
    Not implemented yet, you can acheive this advantage with keep operator.

        2d20k1 -> Roll 2d20, keep the highest

    [Explode Operator]
    [e#]
    To explode dice, you can use the explode operator 'e' followed by a number. If the dice rolled is greater tan or equal to #, then it will explode (rolled again, added to the total).

        3d6e3 -> Roll 3d6, roll an additional d6 for each roll GREATER THAN OR EQUAL to 3

    [Explode On Operator]
    [eo#]
    To explode ON a specific dice, you can use the explode ON operator 'eo' followed by a number. This will roll an additional dice ONLY IF the value is EQUAL to #.

        3d6eo3 -> Roll 3d6, roll an addional dice for each roll EQUAL to 3
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

