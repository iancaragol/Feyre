const { EmbedBuilder, ActionRowBuilder, ButtonBuilder, ButtonStyle } = require('discord.js');
const embedColors = require('./embed_colors')

var embedColor = embedColors.helpEmbedColor
var documentationUrl = "https://feyre.io/commands/"
var inviteLink = "https://invite.feyre.io"

// ================================================
//                      HELP
// ================================================
var helpEmbed = new EmbedBuilder()
helpEmbed.setColor(embedColors.helpEmbedColor)
helpEmbed.setTitle("Feyre - Help")

var helpDescription = `All commands use **/**
 
To learn more about a command you can type **/help command:<command>**
**Ex:**
**/help command:roll**`
helpEmbed.setDescription(helpDescription)

helpEmbed.setThumbnail("https://raw.githubusercontent.com/iancaragol/Feyre/main/docs/assets/feyre-icon.png")

// Main body
var commandFieldBody = `**roll** - Roll complicated dice expressions
**init** - Initiative tracking!
**character** - Manage your characters for the initiative tracker

**stats** - Feyre usage statistics
**health** - Feyre service health`

helpEmbed.addFields(
    { name: "Commands", value: commandFieldBody }
)

// Documentation button
var helpRow = new ActionRowBuilder()
helpRow.addComponents(
    new ButtonBuilder()
        .setLabel('Documentation')
        .setStyle(ButtonStyle.Link)
        .setURL(documentationUrl),
    new ButtonBuilder()
        .setLabel('Invite')
        .setStyle(ButtonStyle.Link)
        .setURL(inviteLink)
)

// ================================================
//                COMMAND NOT FOUND
// ================================================
var notfoundEmbed = new EmbedBuilder()
notfoundEmbed.setColor(embedColors.errorEmbedColor)
notfoundEmbed.setTitle("Command not found")

var notfoundEmbedDescription = `I could not find that command. Try /help for a list of commands!`
notfoundEmbed.setDescription(notfoundEmbedDescription)

// ================================================
//                      ROLL
// ================================================
var rollEmbed = new EmbedBuilder()
rollEmbed.setColor(embedColor)
rollEmbed.setTitle("roll")
rollEmbed.setImage("https://raw.githubusercontent.com/iancaragol/Feyre/main/docs/assets/images/dice-expressions.png")

var rollDescription =
    `/roll can be used to roll dice of any size with complicated expressions.

Dice are represented with the standard [# of dice]d[size of dice] format.

Ex:
/roll expression:4d6
/roll expression:(1d6+2)*2`

var skillCheckField =
    `
**[<, >, >=, <=, =]**
Skill checks can be built into the dice expression using the < and > symbols.

    1d20 > 15 -> True if greater than 15, False otherwise`

var conditionalOperatorField =
    `    
**[t]**
You can add a condition using the letter 't'. Think of the letter 't' as 'then', if the condition on the left side is True, then the expression on the right side will be evaulated.

    1d20 > 15 t 2d6+3 -> If 1d20 is greater than 15 THEN roll 2d6+3`

var countOperatorField =
    `
**[c#]**
You can repeat a dice roll using the count operator, 'c' followed by a number. This needs to be put at the END of an expression, it will roll the expression independently count # of times.

    2d6+3c3 -> Roll 2d6+3 3 times`

var keepOperatorField =
    `
**[k#]**
When rolling multiple dice, you can use the keep operator, 'k' follwed by a number, to keep the highest number of dice.

    5d20k3 -> Roll 5d20 keep the highest 3

**[kl#]**
Keep Lowest, Not implemented yet, will be the inverse of keep`

var advantageOperatorField =
    `Not implemented yet, you can acheive this advantage with keep operator.

    2d20k1 -> Roll 2d20, keep the highest`

var explodeOperatorField =
    `**[e#]**
To explode dice, you can use the explode operator 'e' followed by a number. If the dice rolled is greater tan or equal to #, then it will explode (rolled again, added to the total).

    3d6e3 -> Roll 3d6, roll an extra d6 for each roll GREATER THAN OR EQUAL to 3

**[eo#]**
To explode *ON* a specific dice, you can use the explode ON operator 'eo' followed by a number. This will roll an additional dice ONLY IF the value is EQUAL to #.

    3d6eo3 -> Roll 3d6, roll an addional dice for each roll EQUAL to 3`
rollEmbed.setDescription(rollDescription)
rollEmbed.addFields({ name: "Skill Checks", value: skillCheckField })
rollEmbed.addFields({ name: "Conditional Operator - if then", value: conditionalOperatorField })
rollEmbed.addFields({ name: "Count Operator", value: countOperatorField })
rollEmbed.addFields({ name: "Keep / Drop Operator", value: keepOperatorField })
rollEmbed.addFields({ name: "Advantage / Disadvantage", value: advantageOperatorField })
rollEmbed.addFields({ name: "Explode Operator", value: explodeOperatorField })


// Documentation button
var rollRow = new ActionRowBuilder()
rollRow.addComponents(
    new ButtonBuilder()
        .setLabel('Documentation')
        .setStyle(ButtonStyle.Link)
        .setURL(documentationUrl + "#roll"),
    new ButtonBuilder()
        .setLabel('Invite')
        .setStyle(ButtonStyle.Link)
        .setURL(inviteLink)
)

// ================================================
//                      INIT
// ================================================
var initEmbed = new EmbedBuilder()
initEmbed.setColor(embedColor)
initEmbed.setTitle("init")

var initDescription =
    `/init keeps track of initiative (turn order) for each channel!

Change the turn by hitting the **[Next]** button!

Example:
/init reset
/init get
/init join character:Gandalf initiative:1d20-5`

var initCreation =
    `**[ /init get ]**
/init get will get the active tracker for the channel.
`
var initJoin =
    `**[ /init join character:Name initiative:expression ] or [ Join ]**
To join with your active character (see /help command:character) just press the join button.

To add a specific character specify its name and initiative dice expression.

Example:
/init join character:Frodo initiative:1d20+3
`
var initLeave =
    `**[ /init remove character:Name ]**
Removes the character with Name from initiative

Example:
/init remove character:Frodo
`

var initReset =
    `**[ /init reset ]**
Creates a BRAND NEW initiative tracker for the channel

Example:
/init reset
`

initEmbed.setDescription(initDescription)
initEmbed.addFields({ name: "Getting the channel's tracker", value: initCreation })
initEmbed.addFields({ name: "Joining initiative", value: initJoin })
initEmbed.addFields({ name: "Leaving initiative", value: initLeave })
initEmbed.addFields({ name: "Reset initiative", value: initReset })

// Documentation button
var initRow = new ActionRowBuilder()
initRow.addComponents(
    new ButtonBuilder()
        .setLabel('Documentation')
        .setStyle(ButtonStyle.Link)
        .setURL(documentationUrl + "#initiative-tracking"),
    new ButtonBuilder()
        .setLabel('Invite')
        .setStyle(ButtonStyle.Link)
        .setURL(inviteLink)
)

// ================================================
//                    Character
// ================================================
var charEmbed = new EmbedBuilder()
charEmbed.setColor(embedColor)
charEmbed.setTitle("character")

var charDescription =
    `/character allows you to quickly join initiative

Keep track of up to 9 characters and their initiative modifiers. When you click **Join** on an initiative tracker, you will join with your active character!

Example:
/character list
/character add name:Gandalf initiative:1d20-5`

var charList =
    `**[ /character list ]**
Lists all of your characters. Select your active character by clicking the button with its ID!
`
var charAdd =
    `**[ /character add character:Name initiative:expression ]**
Adds a new character with Name to your list. When you join initiative that character's initiative expression will be rolled!

Example:
/character add name:Frodo initiative:1d20+3
`
var charRemove =
    `**[ /character remove id:id ]**
Removes the character with id from initiative. Use /character list to get each character's id

Example:
/character list
/character remove id:3
`

charEmbed.setDescription(charDescription)
charEmbed.addFields({ name: "List your characters", value: charList })
charEmbed.addFields({ name: "Add a new character to your list", value: charAdd })
charEmbed.addFields({ name: "Remove a character from your list", value: charRemove })

// Documentation button
var charRow = new ActionRowBuilder()
charRow.addComponents(
    new ButtonBuilder()
        .setLabel('Documentation')
        .setStyle(ButtonStyle.Link)
        .setURL(documentationUrl + "#character"),
    new ButtonBuilder()
        .setLabel('Invite')
        .setStyle(ButtonStyle.Link)
        .setURL(inviteLink)
)

module.exports = { helpEmbed, helpRow, notfoundEmbed, rollEmbed, rollRow, initEmbed, initRow, charEmbed, charRow };