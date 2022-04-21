# Commands

**Feyre uses slash commands (/)**

---

## Help

**Syntax**

`/help`

`/help command:roll`


< Help Gif >

Returns documentation for all commands.


---

## Roll

**Syntax**

`/roll expression:DICE EXPRESSION`

**/roll can be used to roll dice of any size with complicated expressions.**

![type:video](./assets/videos/roll demo.mp4)

### Dice Expression

A specific roll can be represented with a dice expression. Dice expressions can be thought of as formula. They consist of **Dice**, **Operations** and **Arithmetic Operators**. You can combine these to create a dice expression that suites any scenario!

Here is an example, imagine you (the GM) need to roll an attack from 3 different archers. The PC who is being attacked has an AC of 13, and if the attacks are succssful you want to roll 2 6-sided dice. The archer's attack roll is 1 20-sided die plus 3. You can do this in one roll!

    1d20+3>13t2d6c3 -> If 1d20+3 is greater than 13 then roll 2d6, repeat 3 times independently

### Dice

Dice are represented by the standard [# of dice]d[size of dice] format

    [# of dice]d[size of dice] -> 1d20 -> One twenty-sided dice

### Arithmetic Operators

Arithmetic Operators are just your standard math operations like +, -, /, *

Feyre also supports order of operations using parenthesis ()

    (1d20+5)*2 -> 1d20 plus 5 then multiplied by 2

### Operations

#### Skill Check
`<, >, >=, <=, =`

Skill checks can be built into the dice expression using the < and > symbols.

    1d20 > 15 -> True if greater than 15, False otherwise

#### Conditional (if then)
`t`

You can add a condition using the letter 't'. Think of the letter 't' as 'then', if the condition on the left side is True, then the expression on the right side will be evaulated.

    1d20 > 15 t 2d6+3 -> If 1d20 is greater than 15 THEN roll 2d6+3

#### Count
`c#`

You can repeat a dice roll using the count operator, 'c' followed by a number. This needs to be put at the END of an expression, it will roll the expression independently count # of times.

    2d6+3c3 -> Roll 2d6+3 3 times

#### Keep
`k#`

When rolling multiple dice, you can use the keep operator, 'k' follwed by a number, to keep the highest number of dice.

    5d20k3 -> Roll 5d20 keep the highest 3

`kl#`

Keep Lowest, Not implemented yet, will be the inverse of keep

#### Advantage

Not implemented yet, you can acheive this advantage with keep operator.

    2d20k1 -> Roll 2d20, keep the highest

#### Explode
`e#`

To explode dice, you can use the explode operator 'e' followed by a number. If the dice rolled is greater tan or equal to #, then it will explode (rolled again, added to the total).

    3d6e3 -> Roll 3d6, roll an extra d6 for each roll GREATER THAN OR EQUAL to 3

`eo#`

To explode *ON* a specific dice, you can use the explode ON operator 'eo' followed by a number. This will roll an additional dice ONLY IF the value is EQUAL to #.

    3d6eo3 -> Roll 3d6, roll an addional dice for each roll EQUAL to 3

---

## Initiative Tracking

**Syntax**

```
/init reset
/init get
/init join character:NAME initiative:DICE EXPRESSION
/init remove character:NAME
```

**/init keeps track of initiative (turn order) for each channel.**

#### Starting Initiative
```
/init get
/init reset
```

`/init get` will post the current tracker for that channel (if it exists). If it does not exist it will create a new one.

`/init reset` will __reset the channels tracker__ so that it is completely empty.

#### Joining Initiative
```
/init join character:Gandalf initiative:1d20-5
/init join
```

If you want to join with a specific character, use:

    /init join character:NAME initiative:DICE EXPRESSION

For example, if I want to join with my character, `Sir Oliver the Timid`, who has an initiative of `1d20+3` I would do this:

    /init join character:Sir Oliver the Timid initiative:1d20+3

If you have a character selected with the `/char` command you can join with that character by pressing the **+** button or `/init join`

**GIF GOES HERE**

#### Next Turn

Press the **⚔️ Next** button to move to the next turn

**GIF GOES HERE**

#### Leaving Initiative (dying)
```
/init remove character:Gandalf
```

Oops, looks like you died! You can leave initiative like this:

    /init remove character:NAME

---

## Character
```
/character list
/character add character:NAME initiative:EXPRESSION
/character remove id:ID
```

Keep track of up to 9 characters and their initiative modifiers. When you click Join on an initiative tracker, you will join with your active character!

#### Select your active character
```
/character list
```

List all of your characters with `/character list` then make your character active by clicking on the corresponding button!

### Add a new character
```
/character add name:NAME initiative:DICE EXPRESSION
```

Add a new character by specifiying its name and its initiative with a dice expression. For example, if my character `Sir Oliver the Timid` has an initiative of `1d20+3` then I can add him to my list with:

    /character add:Sir Oliver The Timid initiative:1d20+3

### Remove a character
```
/character list
/character remove id:ID
```

First list your characters with `/character list` then remove that character using its ID.

For example if `Sir Oliver The Timid` was given an `ID` of `3` I could remove him from my list with:

    /character remove id:3